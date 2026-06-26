# 2. Core Platform Features & Mechanics

> **Cross-References:** Defines feature mechanics for **Maximize-Plus**. UI implementation traces to [07 — Screens](./07_screen_specifications.md). Business validation logic traces to [08 — Rules](./08_business_rules_and_rbac.md). Database tables and API routes trace to [03 — Architecture](./03_technical_architecture.md).

## 2.1 Algorithmic Deal Stacking Calculator Engine

### Feature Overview
The Stacking Engine is the centerpiece mathematical engine of Maximize-Plus. When a shopper selects a brand product (e.g., Apple AirPods on Tata Cliq or sneakers on Myntra), the engine evaluates millions of permutations across four distinct financial layers to construct the optimal payment combination.

### Mathematical Stacking Mechanics (The 4 Layers)
1.  **Layer 1: Instant Gift Card Discount ($D_{gc}$):** Platform checks real-time inventory in `gift_card_catalog` for active discounted brand vouchers.
2.  **Layer 2: Affiliate Network Commission ($C_{aff}$):** Platform queries active EPC and rake rules in `partner_brands` to calculate user cashback pass-through.
3.  **Layer 3: Brand Promotional Coupons ($P_{coup}$):** Engine evaluates active promo codes in `brand_coupons` against cart minimum order value criteria.
4.  **Layer 4: Payment Gateway & Card Offers ($B_{card}$):** System matches user linked cards (`user_linked_cards`) against active bank instant discounts and MCC reward multipliers.

$$\text{Effective Cart Price} = \text{MRP} - (D_{gc} + C_{aff} + P_{coup} + B_{card})$$

### Backend Logic & Execution Flow
*   **Trigger:** Shopper enters cart value or URL on Screen 01 (`POST /api/v1/stack/calculate`).
*   **Processing:** Engine retrieves active rules from Redis cache (`CACHE_BRAND_RULES:*`). Evaluates mutually exclusive coupon constraints.
*   **Output:** Returns a detailed `StackBreakdownPayload` with itemized savings and a 1-click execution CTA.

### Edge Cases & Failure Handling
| Edge Case ID | Scenario Description | System Handling Logic |
|:---|:---|:---|
| **EC-STACK-01** | Brand coupon expires or becomes invalid while user is reviewing calculation | Engine re-validates coupon via merchant API during checkout initiation. If failed, recalculates stack with next best coupon and displays amber alert banner. |
| **EC-STACK-02** | Gift card inventory depletes before user completes payment | `SELECT ... FOR UPDATE` row lock placed on voucher inventory for 300 seconds (5 mins) during checkout. If lock expires, inventory returns to pool. |
| **EC-STACK-03** | User cart contains items excluded from affiliate commission (e.g., gold coins) | Regex matching on cart item SKUs flags excluded categories. Excludes Layer 2 cashback from effective price calculation while maintaining Layers 1, 3, and 4. |

---

## 2.2 MaxCoins Currency & Rewards Vault

### Feature Overview
MaxCoins represent the permanent ecosystem rewards currency of Maximize-Plus. Unlike traditional bank credit card reward points that expire or undergo arbitrary devaluations, MaxCoins are hard-pegged at **1 MaxCoin = ₹1 INR** and never expire.

### Earning & Minting Triggers
*   **Checkout Cashback:** Affiliate cashback earned from brand shopping credited initially as `Pending MaxCoins`. Transitions to `Available MaxCoins` after merchant return window (30-60 days).
*   **Direct Card/UPI Spend:** Users routing daily UPI transactions via the Maximize Pay app earn 0.5% to 1.5% instant MaxCoins.
*   **Streak Bonuses:** Completing 5 consecutive stacked transactions unlocks gamified mystery coin drops (`/earn-max`).

### Redemption & Airline Miles Conversion Matrix
Users can spend Available MaxCoins directly like cash to purchase brand gift vouchers at full face value, or convert them into premium travel loyalty points during exclusive transfer windows (`POST /api/v1/coins/convert`).

| Partner Loyalty Program | Base Conversion Ratio | VIP Bonus Transfer Ratio | Minimum Conversion Quota | Sync SLA |
|:---|:---|:---|:---|:---|
| **Air India Maharaja Club** | 5 MaxCoins = 3 Points | **5 MaxCoins = 4 Points** | 500 MaxCoins | Real-time API (< 5s) |
| **Marriott Bonvoy Points** | 2 MaxCoins = 1 Point | **3 MaxCoins = 2 Points** | 1,000 MaxCoins | Batch cron (Every 6 hrs) |
| **Accor Live Limitless (ALL)**| 3 MaxCoins = 1 Point | **2 MaxCoins = 1 Point** | 1,500 MaxCoins | Batch cron (Daily) |
| **Amazon Pay Balance Vouchers**| 1 MaxCoin = ₹1 INR | **1 MaxCoin = ₹1.05 INR** | 100 MaxCoins | Instant voucher generation |

### Edge Cases & Failure Handling
| Edge Case ID | Scenario Description | System Handling Logic |
|:---|:---|:---|
| **EC-COIN-01** | Airline partner loyalty API times out during miles transfer | Transaction recorded as `PROCESSING` in `maxcoins_ledger`. Background retry worker (`cron_miles_sync`) retries with exponential backoff up to 5 times. If unresolved, auto-refunds coins to user balance. |
| **EC-COIN-02** | Concurrent coin spend attempts exceeding balance across web and mobile | All coin ledger modifications execute via PostgreSQL atomic transactions (`UPDATE maxcoins_ledger ... WHERE balance >= :spend`). Prevents double-spending race conditions. |

---

## 2.3 Smart Shopping Assistant Overlay

### Feature Overview
The Smart Overlay is an unobtrusive background assistant (Android Accessibility Service / iOS Safari Extension / Chrome Desktop Extension) that automatically activates when a user opens a supported external shopping app or website (e.g., Amazon, Swiggy, Uber).

### Behavioral Mechanics & DOM Parsing
*   **Detection:** Overlay monitors active window package name or URL domain against whitelist (`partner_brands`).
*   **Checkout Wakeup:** When user navigates to a checkout or payment screen (`/checkout`, `/payment`, `/cart`), overlay parses total payable amount via DOM selectors or view tree inspection.
*   **Instant Alert:** Displays a sleek floating pill notification: *"⚡ Maximize-Plus found ₹180 savings for this Swiggy order. Tap to apply."*

### Edge Cases & Failure Handling
| Edge Case ID | Scenario Description | System Handling Logic |
|:---|:---|:---|
| **EC-OVL-01** | Merchant app updates UI layout, breaking DOM view tree parsing | Overlay falls back to generic brand prompt: *"Ready to pay on Swiggy? Buy a discounted Swiggy Money voucher first."* Background ML model flags layout change for engineering review. |
| **EC-OVL-02** | User dismisses overlay alert repeatedly on same brand | Frequency capping rule triggered (`redis_overlay_caps`). Suppresses overlay popup for that merchant brand for 24 hours to prevent annoyance churn. |

---

## 2.4 Universal Price Comparison & Checkout Cart

### Feature Overview
The Universal Compare Cart (`/compare`) allows shoppers to search for any product (e.g., "iPhone 15 Pro 128GB") and instantly view side-by-side total stacked checkout prices across major e-commerce platforms (Amazon, Flipkart, Croma, Reliance Digital).

### Affiliate Routing & Attribution Mechanics
When a shopper selects the cheapest cart provider, Maximize-Plus generates a cryptographic redirect link (`/go/:token`).
1.  **Session Logging:** Inserts click record into `affiliate_clicks` with user ID, target brand, timestamp, and unique `subid`.
2.  **Network Redirect:** Appends `subid` to Admitad/Cuelinks destination URL and redirects browser.
3.  **Webhook Reconciliation:** When sale executes, affiliate network fires webhook with matching `subid`, confirming cashback tracking.

---

## 2.5 Instant Brand & Offline Voucher Hub

### Feature Overview
The Voucher Hub (`/gift-cards`) provides real-time access to digital prepaid gift cards across 1500+ brands. Vouchers are delivered instantly upon successful PG payment authorization.

### Cryptographic PIN Security & Fulfillment
*   **Procurement:** Platform integrates with aggregator APIs (Qwix, Woohoo) to mint vouchers on demand.
*   **At-Rest Encryption:** Raw voucher codes and PINs received from aggregators are immediately encrypted using AWS KMS (`AES-256-GCM`) before insertion into `orders` table.
*   **Delivery:** Decrypted strictly in volatile memory when user views Order Confirmation screen or triggers email/WhatsApp delivery.

---

## 2.6 Affiliate Cashback Tracking & Dispute Engine

### Feature Overview
Provides transparent lifecycle tracking for all affiliate purchases. If an affiliate network fails to attribute a purchase automatically, shoppers can submit a missing cashback claim (`/cashback/claim`).

### Dispute Lifecycle Mechanics
1.  **Submission:** Shopper inputs order ID, transaction date, brand, and invoice PDF upload.
2.  **Validation:** System checks `affiliate_clicks` to verify user clicked brand link within 24 hours prior to order date.
3.  **Network Ticket:** Automated API call opens tracking inquiry ticket with Admitad/Impact aggregator.
4.  **Resolution:** Upon merchant confirmation, system credits `Confirmed MaxCoins` directly to user ledger.
