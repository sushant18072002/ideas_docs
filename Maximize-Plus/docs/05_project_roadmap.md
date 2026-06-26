# 5. Master Engineering Roadmap & Sprint Execution Plan

> **Cross-References:** Execution plan for **Maximize-Plus**. Implements requirements in [04 — Stories](./04_user_stories.md). Builds UI screens in [07 — Screens](./07_screen_specifications.md). Adheres to SLAs in [10 — Compliance](./10_nfr_and_compliance.md) and DevOps cron schedules in [11 — DevOps](./11_developer_operations.md).

---

## 5.1 High-Level Execution Timeline (6-Month Gantt Chart)

```mermaid
gantt
    title Maximize-Plus 6-Month Master Engineering Execution Plan
    dateFormat  YYYY-MM-DD
    axisFormat  Month %m
    
    section Foundation Layer
    Sprint 1: Architecture, Kong API Gateway & DB Init     :active, s1, 2026-07-01, 14d
    Sprint 2: Algorithmic Stacking Calculation Engine      :s2, after s1, 14d
    
    section Commerce & Ledger
    Sprint 3: Gift Card Marketplace Hub & KMS Decryption   :s3, after s2, 14d
    Sprint 4: MaxCoins Pegged Ledger & Webhook Engine      :s4, after s3, 14d
    
    section Smart Assistant & Travel
    Sprint 5: Smart Overlay Accessibility Mobile Service   :s5, after s4, 14d
    Sprint 6: Air India / Marriott Airline Miles Hub       :s6, after s5, 14d
    
    section Omnichannel & Disputes
    Sprint 7: Universal Scraper Comparison Cart Engine     :s7, after s6, 14d
    Sprint 8: Missing Cashback Dispute & Support Hub       :s8, after s7, 14d
    Sprint 9: Omnichannel Notifications & Messaging Bus    :s9, after s8, 14d
    
    section Enterprise & Polish
    Sprint 10: Admin RBAC, Wholesale Sync & Treasury Float :s10, after s9, 14d
    Sprint 11: RBI / PCI-DSS Security Audit & Load Testing :s11, after s10, 14d
    Sprint 12: Production Go-Live & GTM Observability      :crit, s12, after s11, 14d
```

---

## 5.2 Itemized 12-Sprint Execution Plan

### Standard Definition of Done (DoD) Applicable to All Tasks
*   Code reviewed and approved by at least 2 Senior Engineers.
*   Unit test coverage exceeding 85% verified via SonarQube.
*   Zero P0/P1 static security analysis vulnerabilities reported.
*   OpenAPI / Swagger documentation updated and verified against Mock servers.
*   Performance calculation latency verified below SLA thresholds (< 150ms).

---

### Sprint 1: Architecture, Kong API Gateway & DB Initialization
*   **Goal:** Provision AWS ECS infrastructure, initialize Kong API Gateway, and deploy 18 Aurora PostgreSQL schema tables.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-101** | Provision VPC, Private Subnets, Multi-AZ Aurora PostgreSQL & Redis Clusters | Cloud DevOps | 8 | Lead DevOps Eng | Terraform scripts applied cleanly in staging environment |
| **DEV-102** | Execute DDL migrations for 18 relational tables with integer `paisa` types | Backend Eng | 5 | Principal Eng | Tables verified via pgAdmin with correct foreign key constraints |
| **DEV-103** | Configure Kong API Gateway JWT authentication and rate-limiting plugins | Backend Eng | 5 | Security Lead | Kong successfully blocks unauthenticated requests with 401 Unauthorized |

---

### Sprint 2: Algorithmic Stacking Engine & Rules Caching
*   **Goal:** Build the core 4-layer calculation engine (`POST /api/v1/stack/calculate`) and Redis brand rules caching layer.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-201** | Implement Layer 1 (Gift Card) + Layer 2 (Affiliate) calculation mechanics | Backend Eng | 8 | Sr Backend Eng | Calculation returns correct effective price matching manual Excel proof |
| **DEV-202** | Implement Layer 3 (Promo Coupon) + Layer 4 (Card Offer) calculation logic | Backend Eng | 8 | Sr Backend Eng | Mutually exclusive coupon rules validated correctly |
| **DEV-203** | Build Redis cache sync worker (`CACHE_BRAND_RULES:*`) with 5-min TTL | Backend Eng | 3 | Backend Eng | Cache hit ratio > 95% under simulated load |

---

### Sprint 3: Gift Card Marketplace Storefront & KMS Decryption Hub
*   **Goal:** Integrate Qwix/Woohoo wholesale APIs, build gift card checkout UI, and implement KMS Envelope Decryption.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-301** | Integrate Qwix/Woohoo wholesale voucher purchasing APIs | Backend Eng | 8 | Lead Integration Eng | Live Sandbox voucher generated upon payment confirmation |
| **DEV-302** | Implement AWS KMS AES-256-GCM encryption of purchased voucher PINs | Security Eng | 5 | Security Lead | Cyphertext stored in DB; zero raw plaintext PINs persisted |
| **DEV-303** | Build Gift Card Storefront UI & PIN Reveal Modal (Screen 04) | Web + Mobile | 5 | Lead UI Eng | Modal reveals decrypted PIN strictly via TLS 1.3 volatile RAM |

---

### Sprint 4: MaxCoins Pegged Ledger & Affiliate Webhook Engine
*   **Goal:** Implement immutable double-entry `maxcoins_ledger` and reconcile Admitad/Cuelinks transaction webhooks.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-401** | Build immutable append-only `maxcoins_ledger` with integer coin pegging | Backend Eng | 8 | Principal Eng | DB trigger blocks any `UPDATE` or `DELETE` queries on ledger |
| **DEV-402** | Implement Admitad/Cuelinks HMAC webhook handlers (`/webhooks/*`) | Backend Eng | 5 | Sr Backend Eng | Webhook correctly attributes user `subid` and credits Pending Coins |
| **DEV-403** | Build MaxCoins Vault & Transaction History UI (Screen 05) | Web + Mobile | 5 | Sr Frontend Eng | Ledger list paginates cleanly displaying coin status |

---

### Sprint 5: Smart Shopping Assistant Mobile Overlay
*   **Goal:** Build Android Accessibility Service and iOS Extension alerting shoppers on merchant checkouts.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-501** | Develop Android Accessibility Service detecting merchant checkout packages | Mobile Eng | 13 | Lead Android Eng | Service reliably detects `in.swiggy.android` checkout screen |
| **DEV-502** | Develop iOS Safari Extension parsing active merchant checkout URLs | Mobile Eng | 8 | Lead iOS Eng | Extension detects Amazon checkout URL and fetches stack rules |
| **DEV-503** | Implement floating savings alert pill UI & dismissal frequency capping | Mobile Eng | 5 | Mobile UI Eng | Tapping pill opens instant gift card purchase overlay |

---

### Sprint 6: Travel Hub & Airline Miles OAuth API Sync
*   **Goal:** Build flight/hotel stacking storefront (`/max-hotels`) and Air India Maharaja / Marriott loyalty conversion APIs.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-601** | Integrate Air India Maharaja Club OAuth2 conversion API | Backend Eng | 8 | Lead Backend Eng | 5:4 bonus transfer executes in real-time crediting user frequent flyer account |
| **DEV-602** | Build batch cron worker (`cron_miles_sync`) reconciling Marriott Bonvoy transfers | Backend Eng | 5 | Backend Eng | Cron correctly batches daily transfers with automatic failure retry |
| **DEV-603** | Build Miles Conversion Screen & Frequent Flyer Name Match UI (Screen 06) | Web + Mobile | 5 | Frontend Eng | UI displays real-time calculated miles yield before submission |

---

### Sprint 7: Universal Price Comparison Scraper Engine
*   **Goal:** Build omnichannel price comparison cart (`/compare`) and cryptographic affiliate redirect routing (`/go/:token`).

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-701** | Build distributed headless scraper aggregation engine for e-commerce carts | Backend Eng | 13 | Lead Scraper Eng | Scraper returns sorted comparative pricing across Amazon/Flipkart < 3s |
| **DEV-702** | Implement `/go/:token` affiliate redirect handler logging `affiliate_clicks` | Backend Eng | 3 | Backend Eng | Redirect injects unique cryptographic `subid` cleanly |
| **DEV-703** | Build Universal Compare Cart UI & Shareable `MaxCart` Viral Link (Screen 03) | Web + Mobile | 5 | Frontend Eng | Shareable link generates preview card with dynamic savings text |

---

### Sprint 8: Affiliate Cashback Claims & Dispute Management
*   **Goal:** Build missing cashback dispute portal (`/cashback/claim`) and automated inquiry ticketing with networks.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-801** | Build missing cashback dispute submission API with invoice PDF S3 upload | Backend Eng | 5 | Backend Eng | API validates user click session prior to ticket creation |
| **DEV-802** | Build automated network inquiry ticket dispatcher with Admitad/Impact APIs | Backend Eng | 8 | Integration Eng | Ticket auto-submits to aggregator portal with transaction details |
| **DEV-803** | Build Customer Dispute Tracking Dashboard UI (Screen 11) | Web + Mobile | 3 | Frontend Eng | Shopper can view real-time dispute resolution status |

---

### Sprint 9: Omnichannel Notifications Engine
*   **Goal:** Implement Firebase Push, Twilio SMS, WhatsApp Webhooks, and AWS SES transactional email templates.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-901** | Implement Firebase Cloud Messaging (FCM) push notification dispatcher | Backend Eng | 5 | Mobile Eng | Instant delivery push fires upon gift card purchase |
| **DEV-902** | Implement Twilio / MSG91 SMS and WhatsApp OTP/delivery notification service | Backend Eng | 5 | Backend Eng | WhatsApp message delivers voucher code with copy CTA |
| **DEV-903** | Create responsive AWS SES HTML email templates for miles conversion confirmations | Frontend Eng | 3 | UI Eng | Templates render cleanly across Gmail, Outlook, and Apple Mail |

---

### Sprint 10: Platform Admin RBAC, Wholesale Sync & Treasury Float
*   **Goal:** Build SuperAdmin audit portal (`/admin/ledger`), RBAC permission matrices, and wholesale inventory sync cron.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-1001**| Implement strict role-based access control (RBAC) middleware across `/api/v1/admin/*` | Security Eng | 5 | Security Lead | Unauthorized staff roles blocked from accessing treasury routes |
| **DEV-1002**| Build Double-Entry Audit Reconciliation Engine & Ledger UI (Screen 15) | Backend Eng | 8 | Principal Eng | Engine flags any mismatch between DB ledger sum and Razorpay escrow float |
| **DEV-1003**| Build wholesale inventory sync cron job (`cron_wholesale_sync`) | Backend Eng | 5 | DevOps Eng | Cron automatically purchases wholesale vouchers when pool drops below threshold |

---

### Sprint 11: RBI / PCI-DSS Security Audit & Load Testing
*   **Goal:** Conduct third-party penetration testing, verify RBI PPI closed-loop compliance, and execute JMeter load benchmarks.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-1101**| Execute automated JMeter load testing simulating 10,000 concurrent stack calculations | QA Eng | 8 | Lead QA Eng | Stacking calculation maintains 99th percentile latency < 180ms under peak load |
| **DEV-1102**| Conduct static code security audit and remediate all reported SonarQube hot spots | Security Eng | 5 | Security Lead | Codebase achieves Grade A security rating |
| **DEV-1103**| Verify Card-on-File network tokenization vault adherence with RBI master directions | Compliance Eng| 5 | Compliance Officer| Zero plaintext PAN data identified across entire AWS RDS infrastructure |

---

### Sprint 12: Production Go-Live & Post-Launch Observability
*   **Goal:** Execute blue-green production deployment, enable Datadog/Grafana observability dashboards, and launch GTM loop.

| Task ID | Task Description | Assigned Team | Story Points | Task Owner | Specific DoD Criteria |
|:---|:---|:---|:---:|:---|:---|
| **DEV-1201**| Execute blue-green production deployment to AWS ECS Fargate Cluster | DevOps Eng | 5 | Lead DevOps Eng | Production deployment completes with zero user downtime |
| **DEV-1202**| Configure Datadog APM tracing, Aurora database monitors, and PagerDuty alert hooks | DevOps Eng | 5 | Sr DevOps Eng | Alert hooks fire instantly upon simulated payment gateway latency spike |
| **DEV-1203**| Launch promotional GTM welcome coin campaign and viral shareable cart tracking | Product Eng | 3 | Product Manager | Welcome campaign auto-mints ₹100 MaxCoins to verified new waitlist users |

---

## 5.3 Sprint-by-Sprint Monetary Budget & Resource Burn Rate (in ₹ INR)

Each agile sprint spans exactly 14 calendar days (0.5 months). The following matrix details the allocated monetary budget per sprint combining active engineering human resource payroll (CapEx) and runtime cloud infrastructure consumption (OpEx).

| Sprint # | Primary Milestone Deliverable | Active Team Headcount | Bi-Weekly Payroll Burn (₹) | Bi-Weekly OpEx Burn (₹) | Total Sprint Budget (₹ INR) | Blended Cumulative Burn (₹) |
|:---:|:---|:---:|:---|:---|:---|:---|
| **Sprint 1** | AWS Topology & DB Schema Init | 6 (Arch + DevOps + Backend)| ₹8,40,000 | ₹1,05,000 | **₹9,45,000** | ₹9,45,000 |
| **Sprint 2** | Algorithmic Stacking Engine | 8 (+ Fullstack + QA) | ₹11,15,000 | ₹1,15,000 | **₹12,30,000** | ₹21,75,000 |
| **Sprint 3** | Gift Card Hub & KMS Vault | 10 (+ Mobile + Security)| ₹12,65,000 | ₹1,45,000 | **₹14,10,000** | ₹35,85,000 |
| **Sprint 4** | MaxCoins Pegged Ledger | 10 | ₹12,65,000 | ₹1,55,000 | **₹14,20,000** | ₹50,05,000 |
| **Sprint 5** | Smart Assistant Mobile Overlay| 12 (Full Squad Active) | ₹12,65,000 | ₹1,75,000 | **₹14,40,000** | ₹64,45,000 |
| **Sprint 6** | Travel & Airline Miles OAuth | 12 | ₹12,65,000 | ₹1,85,000 | **₹14,50,000** | ₹78,95,000 |
| **Sprint 7** | Headless Scraper Compare Cart | 12 (+ Stealth Proxies) | ₹12,65,000 | ₹2,35,000 | **₹15,00,000** | ₹93,95,000 |
| **Sprint 8** | Cashback Claims Dispute Portal | 12 | ₹12,65,000 | ₹2,15,000 | **₹14,80,000** | ₹1,08,75,000|
| **Sprint 9** | Omnichannel Notifications Bus | 12 (+ WhatsApp API) | ₹12,65,000 | ₹2,14,726 | **₹14,79,726** | ₹1,23,54,726|
| **Sprint 10**| Admin RBAC & Wholesale Cron | 12 | ₹12,65,000 | ₹2,14,726 | **₹14,79,726** | ₹1,38,34,452|
| **Sprint 11**| Pen-Testing & JMeter Benchmarks| 12 | ₹12,65,000 | ₹2,14,726 | **₹14,79,726** | ₹1,53,14,178|
| **Sprint 12**| Production Launch & Observability| 12 | ₹12,65,000 | ₹2,14,726 | **₹14,79,726** | **₹1,67,93,904**|

*(Note: Minor contingency reserves bring final executed 6-month capital expenditure baseline to ₹1.78 Crores).*

