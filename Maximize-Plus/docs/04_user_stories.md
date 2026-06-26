# 4. Agile User Stories & Behavioral Specifications

> **Cross-References:** Behavioral requirements for **Maximize-Plus**. UI interactions trace to [07 — Screens](./07_screen_specifications.md). Financial validation rules trace to [08 — Rules](./08_business_rules_and_rbac.md). Triggered alerts trace to [09 — Notifications](./09_notifications_and_emails.md). Sprint assignments map to [05 — Roadmap](./05_project_roadmap.md).

---

## Epic 1: Algorithmic Deal Stacking & Cart Calculation

### US-101: Calculate Multi-Layer Stacking Savings
*   **As a** Deal-Savvy Consumer,
*   **I want** to enter a target e-commerce cart value and merchant brand into the Stacking Calculator,
*   **So that** I can instantly see the exact mathematical minimum checkout price combining Gift Cards, Affiliate Cashback, Brand Coupons, and Card Offers.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I am an authenticated shopper on the Homepage Calculator (Screen 01), **When** I select "Myntra" and enter cart amount `₹5,000`, **Then** the system queries `POST /api/v1/stack/calculate` within 150ms.
2.  **Given** active inventory exists in `gift_card_catalog`, **When** the stack calculation returns, **Then** I see an itemized breakdown: Gift Card discount (-₹200), Affiliate Cashback (-₹250), Promo Code `SAVE10` (-₹500), and Bank Offer (-₹225), displaying a final effective price of `₹3,825`.
3.  **Given** no applicable coupons exist for that brand, **When** the calculation completes, **Then** Layer 3 (Coupons) displays `₹0` while the remaining layers calculate normally.

#### Error & Alternative Paths
*   **ERR-101-A:** If the entered cart value falls below the merchant's minimum gift card denomination (e.g., ₹100), display inline validation error: *"Minimum order value for Myntra stacking is ₹250."*
*   **Sprint Assignment:** Sprint 2 (Core Calculation Engine)

---

### US-102: 1-Click Stack Execution & Cart Checkout
*   **As a** Purchasing Consumer,
*   **I want** to click "Execute Stack" on a calculated breakdown,
*   **So that** the platform automatically redirects me through the affiliate link, issues the discounted gift card, and copies the promo code to my clipboard.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I am viewing a calculated stack payload on Screen 02, **When** I tap "Execute Stack Now", **Then** the platform initiates `POST /api/v1/stack/checkout` and places a 300-second reservation lock on the target gift voucher in `gift_card_catalog`.
2.  **Given** the checkout sequence executes, **When** PG authorization succeeds, **Then** the system triggers automated background browser redirect to `GET /go/:token` (logging session in `affiliate_clicks`) and injects the decrypted gift card code and coupon into a persistent floating overlay widget.

#### Error & Alternative Paths
*   **ERR-102-A:** If PG payment fails or is declined by user bank, release the voucher reservation lock immediately and trigger Notification `NOTIF_PG_FAIL`.
*   **Sprint Assignment:** Sprint 3 (Checkout Stacking Flow)

---

## Epic 2: MaxCoins Minting, Vault & Airline Miles Conversion

### US-201: Automated Earning of Pegged MaxCoins
*   **As an** Active Consumer Shopper,
*   **I want** my shopping cashback and daily UPI payments to accumulate as non-expiring MaxCoins,
*   **So that** I build permanent digital value pegged hard at 1 MaxCoin = ₹1 INR.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I complete a stacked order routing via an Admitad affiliate link, **When** Admitad fires transaction confirmation webhook `POST /webhooks/admitad`, **Then** the system inserts a credit entry into `maxcoins_ledger` with status `PENDING` and displays *"Expected by Feb 2026"* on my Vault Dashboard (Screen 05).
2.  **Given** the merchant return window passes (e.g., 45 days), **When** Admitad fires settlement confirmation webhook, **Then** a background cron job updates the ledger status to `AVAILABLE` and triggers Push Notification `NOTIF_COINS_AVAILABLE`.

#### Sprint Assignment: Sprint 4 (Ledger & Payouts Engine)

---

### US-202: Instant Conversion to Air India Maharaja Points
*   **As a** Frequent Flyer & Travel Hacker,
*   **I want** to convert my Available MaxCoins into Air India Maharaja Club points during a 5:4 bonus window,
*   **So that** I redeem flight upgrades at an industry-leading exchange ratio.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I have an Available Balance of `10,000 MaxCoins` on Screen 05, **When** I select "Air India Maharaja Club", enter my frequent flyer membership ID `AI-982341`, and input quota `5,000 Coins`, **Then** the UI displays the calculated yield: `4,000 Maharaja Points`.
2.  **Given** I confirm conversion with my 4-digit security PIN, **When** `POST /api/v1/coins/convert` executes, **Then** the system atomically debits `5,000 Coins` from `maxcoins_ledger`, calls the Air India OAuth2 API, and delivers confirmation email `EMAIL_MILES_SENT`.

#### Error & Alternative Paths
*   **ERR-202-A:** If the entered frequent flyer ID fails Air India name match validation, reject transaction synchronously: *"Membership ID name does not match KYC verified account name."*
*   **Sprint Assignment:** Sprint 6 (Travel & Airline Integrations)

---

## Epic 3: Smart Shopping Assistant Overlay & Price Comparison

### US-301: Automatic Checkout Overlay Wakeup
*   **As a** Mobile Shopper,
*   **I want** the Maximize-Plus overlay pill to pop up automatically when I reach the payment screen on Swiggy or Amazon,
*   **So that** I never forget to buy a discounted gift voucher before paying.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I have granted Android Accessibility / iOS Extension permission, **When** I open the Swiggy app and proceed to the final payment summary screen with cart payable `₹850`, **Then** the background service detects package `in.swiggy.android` and queries `GET /api/v1/overlay/check`.
2.  **Given** an 8% wholesale Swiggy Money voucher discount exists, **When** the check returns, **Then** a sleek floating pill slides in at the top of my screen: *"⚡ Save ₹68 on this order with Maximize-Plus. Tap to buy instant voucher."*

#### Error & Alternative Paths
*   **ERR-301-A:** If user taps "Dismiss" on the floating pill, insert log into `overlay_cap_events` suppressing overlay wakeups for Swiggy for 24 hours.
*   **Sprint Assignment:** Sprint 5 (Smart Assistant Mobile Service)

---

### US-302: Universal Cross-Platform Cart Comparison
*   **As an** Omnichannel Shopper,
*   **I want** to search for "Sony WH-1000XM5 Headphones" in the Universal Compare Cart,
*   **So that** I see side-by-side total stacked checkout prices across Amazon, Flipkart, Croma, and Reliance Digital.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I enter query `Sony WH-1000XM5` on Screen 03 (`GET /api/v1/compare`), **When** the real-time scraper pipeline aggregates merchant pricing, **Then** the UI renders a sorted comparative matrix highlighting the lowest effective price after applying brand gift cards and credit card cashbacks.

#### Sprint Assignment: Sprint 7 (Scraper Comparison Cart)

---

## Epic 4: Instant Gift Card Storefront & KMS Decryption

### US-401: Instant Purchase & Volatile Memory Decryption
*   **As a** Corporate or Personal Gifter,
*   **I want** to buy a ₹10,000 Taj Hotels gift voucher using UPI and receive the uncompromised PIN instantly,
*   **So that** I complete my hotel booking without fulfillment delays.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I complete payment authorization for a ₹10,000 Taj voucher on Screen 04, **When** `POST /api/v1/giftcards/purchase` executes, **Then** the platform calls the Qwix aggregator API, receives the encrypted ciphertext, and stores it in `orders` under AWS KMS Envelope Encryption.
2.  **Given** I tap "Reveal PIN & Voucher Code", **When** `POST /api/v1/giftcards/decrypt` executes, **Then** the system decrypts the PIN strictly in volatile server RAM, transmits it over TLS 1.3 to my screen, and logs security audit event `AUDIT_PIN_REVEAL`.

#### Sprint Assignment: Sprint 3 (Gift Card Marketplace Hub)

---

## Epic 5: Affiliate Cashback Tracking & Claims

### US-501: Submit Missing Cashback Dispute Ticket
*   **As an** Affiliate Shopper,
*   **I want** to upload my merchant invoice to claim untracked shopping cashback,
*   **So that** I recover earnings lost due to browser ad-blockers or dropped cookies.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** my Nykaa shopping purchase did not auto-track within 48 hours, **When** I submit order ID `NYK-8812` and invoice PDF on Screen 11 (`POST /api/v1/cashback/claim`), **Then** the system validates matching redirect session in `affiliate_clicks` and creates dispute ticket `SUBMITTED`.

#### Sprint Assignment: Sprint 8 (Disputes & Customer Support Hub)

---

## Epic 6: Platform SuperAdmin & Treasury Operations

### US-601: Financial Double-Entry Audit Reconciliation
*   **As a** Platform Treasury Controller,
*   **I want** to generate a double-entry ledger reconciliation report across all PG settlements and MaxCoin balances,
*   **So that** I guarantee absolute zero financial discrepancy across escrow accounts.

#### Acceptance Criteria (Given / When / Then)
1.  **Given** I am an RBAC SuperAdmin on Admin Screen 15, **When** I trigger `GET /api/v1/admin/ledger`, **Then** the system queries `ledger_transactions` and `maxcoins_ledger` to verify that sum of all user balances matches liquid cash held in Razorpay Escrow Float.

#### Sprint Assignment: Sprint 10 (Admin Treasury & RBAC Controls)
