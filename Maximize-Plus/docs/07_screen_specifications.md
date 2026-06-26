# 7. UI/UX Screen Specifications & Validation Matrices

> **Cross-References:** UI blueprint for **Maximize-Plus**. Consumes API endpoints in [03 — Architecture](./03_technical_architecture.md). Implements behavioral user stories in [04 — Stories](./04_user_stories.md). Enforces UI validation rules in [08 — Rules](./08_business_rules_and_rbac.md).

---

## 7.1 Screen Inventory Index (16 Core Screens)

| Screen ID | Screen Name | Route Path | Primary API consumed | Target User Role |
|:---|:---|:---|:---|:---|
| **SCR-01** | Homepage Stacking Calculator Widget | `/` | `POST /api/v1/stack/calculate`| Consumer Shopper |
| **SCR-02** | Stacking Breakdown & Checkout Modal | `/checkout/stack` | `POST /api/v1/stack/checkout` | Consumer Shopper |
| **SCR-03** | Universal Cart Comparison Screen | `/compare` | `GET /api/v1/compare` | Consumer Shopper |
| **SCR-04** | Gift Card Storefront & PIN Reveal Modal| `/gift-cards` | `POST /api/v1/giftcards/decrypt`| Consumer Shopper |
| **SCR-05** | MaxCoins Vault & Ledger Screen | `/max-coins` | `GET /api/v1/coins/ledger` | Consumer Shopper |
| **SCR-06** | Airline Miles Conversion Hub | `/convert` | `POST /api/v1/coins/convert` | Consumer Shopper |
| **SCR-07** | Smart Assistant Overlay Popup | *System Window* | `GET /api/v1/overlay/check` | Consumer Shopper |
| **SCR-08** | Earn-Max Streak Hub | `/earn-max` | `GET /api/v1/streaks` | Consumer Shopper |
| **SCR-09** | User Profile & PAN KYC Screen | `/settings/kyc` | `POST /api/v1/kyc/pan` | Consumer Shopper |
| **SCR-10** | Saved Payment Cards Hub | `/settings/cards` | `GET /api/v1/cards` | Consumer Shopper |
| **SCR-11** | Missing Cashback Claim Portal | `/cashback/claim` | `POST /api/v1/cashback/claim` | Consumer Shopper |
| **SCR-12** | Verified Brand Promo Code Hub | `/coupons` | `GET /api/v1/coupons` | Consumer Shopper |
| **SCR-13** | Max-Hotels Travel Stacking Storefront| `/max-hotels` | `GET /api/v1/hotels` | Consumer Shopper |
| **SCR-14** | Merchant Brand Affiliate Portal | `/merchant/settings`| `PUT /api/v1/brands/:id` | Brand Merchant |
| **SCR-15** | SuperAdmin Treasury Audit Dashboard | `/admin/ledger` | `GET /api/v1/admin/ledger` | Treasury SuperAdmin|
| **SCR-16** | Authentication & Mobile OTP Modal | `/login` | `POST /api/v1/auth/otp` | Unauthenticated |

---

## 7.2 Field-Level Specifications & Validation Matrices

### SCR-01: Homepage Stacking Calculator Widget

#### Purpose
Allows shoppers to input cart details and instantly compute 4-layer stacked savings.

#### UI Wireframe Structure & Component Hierarchy
*   **Header Section:** Hero banner displaying *"Average 15% savings per order across 1500+ brands"*.
*   **Input Box 1:** Brand Selector Dropdown (`SearchBrandInput`).
*   **Input Box 2:** Cart Gross Amount Input (`CartAmountInput`).
*   **CTA Button:** "Calculate Max Savings" (`CalculateStackBtn`).

#### Field Validation & Constraints
| UI Field Name | UI Component Type | Mandatory | Validation Regex / Rule | Error Prompt Text |
|:---|:---|:---:|:---|:---|
| `Brand Selector` | Searchable Dropdown | YES | Must match valid slug in `partner_brands` | *"Please select a supported brand."* |
| `Cart Amount` | Numeric Currency Input | YES | `^[1-9][0-9]{1,6}$` (₹10 to ₹9,99,999) | *"Enter cart value between ₹10 and ₹10,00,000."* |

#### State Render Matrix
| UI State | Trigger Condition | Display Rendering Component |
|:---|:---|:---|
| **Loading** | User clicks CTA button | Disable inputs; render shimmering 4-layer stack skeleton animation. |
| **Empty** | Initial page load | Render default demonstration stack for ₹5,000 Adidas order. |
| **Error** | API returns `ERR_BRAND_MAINTENANCE`| Display red toast banner: *"Myntra stacking is temporarily undergoing API maintenance."* |
| **Success**| API returns `200 OK` | Smoothly slide open SCR-02 Breakdown Modal. |

---

### SCR-04: Gift Card Storefront & PIN Reveal Modal

#### Purpose
Facilitates instant purchasing of discounted prepaid brand vouchers and volatile memory PIN revelation.

#### Field Validation & Constraints
| UI Field Name | UI Component Type | Mandatory | Validation Regex / Rule | Error Prompt Text |
|:---|:---|:---:|:---|:---|
| `Denomination Tier`| Pill Radio Group | YES | Selected value must exist in `gift_card_catalog`| *"Selected denomination is out of stock."* |
| `Security PIN` | 4-Digit Password Box| YES | `^[0-9]{4}$` (Must match user account PIN) | *"Incorrect 4-digit security PIN."* |

#### State Render Matrix
| UI State | Trigger Condition | Display Rendering Component |
|:---|:---|:---|
| **Loading** | User clicks "Reveal PIN" | Display spinning lock icon with subtitle *"Decrypting PIN via secure HSM..."* |
| **Success** | API returns decrypted PIN | Render high-contrast monospace text box displaying PIN with 1-tap "Copy" button. |

---

### SCR-06: Airline Miles Conversion Hub

#### Purpose
Converts non-expiring Available MaxCoins into Air India Maharaja Club or Marriott Bonvoy points.

#### Field Validation & Constraints
| UI Field Name | UI Component Type | Mandatory | Validation Regex / Rule | Error Prompt Text |
|:---|:---|:---:|:---|:---|
| `Loyalty Partner`| Partner Card Selector| YES | Must match valid partner in `miles_conversion_rates`| *"Select a loyalty partner."* |
| `Membership ID` | Alphanumeric Text Box | YES | `^[A-Z0-9]{6,12}$` | *"Enter a valid frequent flyer ID."* |
| `Coins to Convert`| Numeric Slider / Box | YES | Must be $\ge 500$ and $\le \text{Available Balance}$| *"Minimum conversion is 500 MaxCoins."* |

---

### SCR-07: Smart Assistant Overlay Popup

#### Purpose
System accessibility overlay pill alerting mobile/desktop users on merchant checkout screens.

#### UI Component Specifications
*   **Floating Pill Widget:** High-priority accessibility window (`TYPE_APPLICATION_OVERLAY` on Android).
*   **Dimensions:** Width: 90% of screen width, Height: 64dp, Position: Top margin 24dp.
*   **Content:** Brand logo + dynamic savings string + lightning CTA button.
*   **Dismissal:** Top-right `X` close button triggering `POST /api/v1/overlay/dismiss`.

---

### SCR-09: User Profile & PAN KYC Screen

#### Purpose
Enforces regulatory compliance by capturing verified Indian Permanent Account Number (PAN) details before permitting wallet withdrawals.

#### Field Validation & Constraints
| UI Field Name | UI Component Type | Mandatory | Validation Regex / Rule | Error Prompt Text |
|:---|:---|:---:|:---|:---|
| `Full Name` | Text Input Box | YES | Must exactly match name printed on PAN card | *"Name must match PAN card."* |
| `PAN Number` | Uppercase Text Box | YES | `^[A-Z]{5}[0-9]{4}[A-Z]{1}$` | *"Enter a valid 10-character PAN number."* |
| `Date of Birth` | Datepicker | YES | Must verify user age $\ge 18$ years | *"You must be 18+ to withdraw funds."* |

---

### SCR-15: SuperAdmin Treasury Audit Dashboard

#### Purpose
Double-entry accounting dashboard restricted to RBAC SuperAdmins for escrow float reconciliation.

#### Data Display Columns
1.  **Ledger Master Sum:** Total gross consumer liabilities recorded in `maxcoins_ledger` + `wallet_balances`.
2.  **Escrow Bank Balance:** Live liquid cash balance queried via Razorpay Escrow API.
3.  **Delta Variance:** Must mathematically equal `₹0.00`. If $> ₹1.00$, render blinking crimson warning header.
