# 1. Product Requirements Document (PRD) & Market Analysis

> **Cross-References:** This is the foundational document. All features are detailed in [02 — Features](./02_core_features.md). Technical implementation in [03 — Architecture](./03_technical_architecture.md). User stories in [04 — Stories](./04_user_stories.md). Development plan in [05 — Roadmap](./05_project_roadmap.md).

## 1.1 Document Control
| Field | Value |
|:---|:---|
| **Document Version** | 4.0 |
| **Project Code Name** | Euka-Plus |
| **Author** | Business Analyst |
| **Last Updated** | 2026-03-20 |
| **Status** | DRAFT — Pending Stakeholder Review |
| **Audience** | CTO, Lead Engineers, Product Managers, QA Leads |

---

## 1.2 Glossary of Terms
Every term used repeatedly in the documentation is defined here to prevent ambiguity.

| Abbreviation | Full Form | Definition |
|:---|:---|:---|
| **GMV** | Gross Merchandise Value | Total dollar value of all products sold through a creator's affiliate link |
| **ROAS** | Return on Ad Spend | Revenue generated divided by the cost of the campaign (samples + payouts) |
| **COGS** | Cost of Goods Sold | The cost of manufacturing/purchasing the product sample sent to a creator |
| **CAC** | Customer Acquisition Cost | The total marketing spend required to acquire one paying brand customer |
| **LTV** | Lifetime Value | The total revenue a single brand customer is expected to generate over their subscription lifetime |
| **UGC** | User-Generated Content | Content (photos, videos) created by individuals rather than brands |
| **CRM** | Customer Relationship Management | The software module tracking all brand-to-creator interactions |
| **DM** | Direct Message | A private message sent on a social media platform |
| **KYC** | Know Your Customer | Regulatory process of verifying the identity of individuals before financial transactions |
| **AML** | Anti-Money Laundering | Regulations to prevent illegal financial activity through platforms |
| **PII** | Personally Identifiable Information | Any data that could identify a specific individual (name, address, SSN, etc.) |
| **RBAC** | Role-Based Access Control | Security model restricting system access to authorized roles only |
| **3PL** | Third-Party Logistics | A fulfillment warehouse that ships products on behalf of the brand (e.g., ShipBob) |
| **NFR** | Non-Functional Requirement | A system requirement specifying criteria like performance, security, and uptime |
| **Retainer** | — | A recurring monthly deal where a creator produces X videos/month for a fixed salary |
| **Collab** | — | A one-time promotional deal between a brand and a creator |
| **Usage Rights** | — | A legal license allowing the brand to redistribute a creator's video as their own paid advertisement |
| **Spark Ad / Partnership Ad** | — | Instagram's Branded Content ("Partnership Ad") mechanism allowing brands to boost an organic creator post/Reel as a paid ad |

---

## 1.3 Executive Summary & Vision Statement
The **Euka-Plus** platform is a B2B2C (Business-to-Business-to-Creator) SaaS ecosystem. It automates every operational step of affiliate marketing on short-form video platforms (Instagram Reels, YouTube Shorts, Amazon Influencer Program).

**The Vision:** A world where any DTC brand, regardless of team size, can scale a 1,000-creator affiliate army with the click of a button, and where every creator has a single, reliable financial home base for all their brand deals.

---

## 1.4 The Problem Space (Micro-Level Friction Points)

### For Brands:
| # | Friction Point | Current Workaround | Cost of Inaction |
|:--|:---|:---|:---|
| 1 | Finding creators who can *sell*, not just post | Manually scrolling Instagram for hours | 8-12 hrs / week wasted per team member |
| 2 | Crafting unique DMs for each creator | Copy-pasting a template, getting flagged as spam | <5% reply rate; risk of account shadowban |
| 3 | Tracking if a product sample was received | Manually pasting tracking numbers into Google Sheets | 30% of samples go untracked; creators ghost |
| 4 | Knowing which creator drove which sale | Instagram Shops attribution is delayed and limited | Cannot make real-time investment decisions |
| 5 | Paying creators on time | Wiring PayPal manually per creator, per video | Accounting errors; tax compliance risk |
| 6 | Legally licensing a creator's video for paid ads | Emailing Word docs back and forth | No enforceable IP trail; legal exposure |

### For Creators:
| # | Friction Point | Current Workaround | Cost of Inaction |
|:--|:---|:---|:---|
| 1 | Finding high-converting products to promote | Browsing Instagram Shop marketplace randomly | Wasted time promoting products nobody buys |
| 2 | Unstable, unpredictable income | Accepting any deal, regardless of fit | Burnout, low conversion, brand mismatch |
| 3 | Tracking earnings across multiple brands | Spreadsheets, memory, DM threads | Lost income; cannot invoice accurately |
| 4 | Signing contracts for every brand deal | Adobe Sign, DocuSign, or worse—screenshot of a DM | No legal protection for either party |
| 5 | Getting paid late or not at all | Chasing brands via DM after 30+ days | Cash flow crises |

---

## 1.5 Stakeholder Map
| Stakeholder | Role in the Platform | Primary KPI |
|:---|:---|:---|
| **Brand SuperAdmin** | Creates the workspace, manages billing, sets team permissions | Monthly Active Campaigns |
| **Brand Member** | Operates the CRM daily, configures drip campaigns, reviews analytics | ROAS per Creator |
| **Brand Viewer** | Read-only access to dashboards for reporting to leadership | Export CSV accuracy |
| **Creator (Free Tier)** | Browses deals, applies to Collabs/Retainers/Contests, withdraws earnings | Monthly Earnings |
| **Creator (VIP Tier)** | Top performers granted early access to exclusive high-ticket Retainers | Lifetime GMV |
| **Platform Admin (Internal)** | Manages marketplace curation, resolves disputes, monitors fraud | Churn Rate, Fraud Incidents |

---

## 1.6 Detailed Buyer Personas

### Persona A: Sarah — The Bootstrapped DTC Founder
*   **Demographic:** 29F, Austin TX. Runs a $2M ARR clean beauty brand on Shopify. Team of 3.
*   **Technical Proficiency:** Moderate. Comfortable with Shopify but not APIs.
*   **Device Usage:** MacBook Air (primary), iPhone 15 (checking notifications).
*   **Monthly Budget for Affiliate Tools:** $200-$300.
*   **Key Frustration Quote:** *"I spend my entire Monday just sending DMs to creators. By Friday, 90% haven't replied, and I've already forgotten who I need to follow up with."*
*   **Success Metric:** If the tool can autonomously recruit 20 new affiliates per week, she considers it a success.

### Persona B: Marcus — The Enterprise Performance Manager
*   **Demographic:** 35M, NYC. Manages affiliate programs for a $100M+ supplement brand. Team of 12.
*   **Technical Proficiency:** High. Uses Postman, understands APIs, exports CSV for Tableau dashboards.
*   **Device Usage:** Windows Desktop (dual monitors), company iPad for presentations.
*   **Monthly Budget for Affiliate Tools:** $1,500-$3,000.
*   **Key Frustration Quote:** *"I manage 800 affiliates. I literally cannot track who received their sample, who posted, and who needs to be paid without a dedicated full-time employee just for logistics."*
*   **Success Metric:** A single dashboard that shows ROAS per creator with 1-click CSV export for his CFO.

### Persona C: Jasmine — The Full-Time UGC Creator
*   **Demographic:** 23F, Miami FL. 85k Instagram followers. Creates 3-5 brand Reels per week.
*   **Technical Proficiency:** Low. Mobile-only.
*   **Device Usage:** iPhone 15 Pro exclusively.
*   **Monthly Income from UGC:** $2,000-$5,000 (highly variable).
*   **Key Frustration Quote:** *"I got paid for a brand deal in January but the money didn't hit my PayPal until March. I need something where I can see my balance and cash out instantly."*
*   **Success Metric:** A single app that shows her all available deals, lets her tap to apply, and withdraw earnings with one button.

---

## 1.7 Competitive Landscape Analysis

| Feature | **EUKA** (Current) | **Grin** | **CreatorIQ** | **Euka-Plus** (Our Clone) |
|:---|:---|:---|:---|:---|
| Instagram Reels/Shop Native | ❌ | ✅ | ✅ | ✅ Deep (Primary) |
| TikTok Shop | ✅ Deep | ❌ | ❌ | 🔜 Future Phase |
| Amazon Affiliate | ✅ | ❌ | ❌ | ✅ |
| YouTube Shorts | ❌ | ✅ | ✅ | ✅ (Omnichannel) |
| Native Mobile App for Creators | ✅ iOS Only | ❌ | ❌ | ✅ iOS + Android (Flutter) |
| Automated DM Outreach | ✅ | ❌ | ❌ | ✅ (With AI Personalization) |
| In-App Contract Signing | ✅ | ✅ | ✅ | ✅ |
| Gamified Contests | ✅ | ❌ | ❌ | ✅ (Enhanced Leaderboards) |
| Predictive ROI Scoring | ❌ | ❌ | Partial | ✅ (ML Model) |
| PayPal Instant Payouts | ✅ | ✅ | ❌ | ✅ |
| Trend AI Analysis Tool | ✅ | ❌ | ❌ | ✅ (LLM-Powered) |
| Retainer Management | ✅ | ❌ | ✅ | ✅ |
| Pricing (Entry) | ~$299/mo | ~$999/mo | Enterprise | $149/mo (undercut) |

---

## 1.8 Revenue Model & Unit Economics

### SaaS Pricing Tiers (Brand Side)
| Tier | Monthly Price | DM Quota/mo | Active Campaigns | Seats | Support |
|:---|:---|:---|:---|:---|:---|
| **Starter** | $149/mo | 200 DMs | 3 | 2 | Email |
| **Growth** | $499/mo | 1,000 DMs | 10 | 5 | Priority Email + Chat |
| **Enterprise** | $1,999/mo | Unlimited (BYOP*) | Unlimited | Unlimited | Dedicated AM + API |

*BYOP = Bring Your Own Proxies. Enterprise clients provide their own residential proxy credentials.*

### Platform Revenue from Creator Transactions
*   **Transaction Rake:** 5% on all Collab/Retainer payouts processed through the platform. If a brand pays a creator $500, the platform retains $25 and routes $475 to the creator's PayPal.
*   **Usage Rights Marketplace Fee:** 10% on all IP licensing transactions (higher margin due to legal liability the platform assumes).

### Key Financial Metrics to Track (Internal Dashboard)
| Metric | Target | Calculation |
|:---|:---|:---|
| **MRR (Monthly Recurring Revenue)** | $50k by Month 6 | Sum of all active Brand subscriptions |
| **CAC** | < $500 per brand | Total Sales & Marketing Spend / New Brands |
| **LTV:CAC Ratio** | > 3:1 | LTV / CAC |
| **Creator Churn Rate** | < 8% monthly | Creators who stopped using app / Total active |
| **GMV Processed** | $1M/mo by Month 9 | Total affiliate sales tracked through platform |

---

## 1.9 Risk Register

| Risk ID | Category | Risk Description | Likelihood | Impact | Mitigation Strategy |
|:---|:---|:---|:---|:---|:---|
| R-001 | Technical | Instagram aggressively updates anti-bot protection or Graph API rate limits, breaking scrapers | HIGH | CRITICAL | Maintain 3 independent scraper strategies (Graph API-first, Playwright fallback, manual CSV import). Dedicate 1 engineer to "scraper health" monitoring. |
| R-002 | Legal | GDPR violation from scraping EU creator data | MEDIUM | CRITICAL | Geo-fence all scraping to US/UK IPs only. Implement "Right to Erasure" endpoint. |
| R-003 | Financial | Creator disputes payout amounts (ledger disagreement) | MEDIUM | HIGH | Immutable `ledger_transactions` table with append-only design. No `UPDATE` or `DELETE` allowed; only corrective `INSERT` entries. |
| R-004 | Operational | Residential proxy provider rate-limits or terminates service | MEDIUM | HIGH | Maintain contracts with 2+ proxy providers (BrightData + Smartproxy) and implement automatic failover. |
| R-005 | Market | Instagram launches a native, free affiliate CRM | LOW | CRITICAL | Differentiate on omnichannel value proposition — no single platform will build tools for their competitors. |

---

## 1.10 Go-To-Market Strategy & Viral Loop

### Phase 1: Seed the Supply (Creators)
*   Run Instagram ads targeting `#UGC`, `#InfluencerMarketing`, and `#InstagramAffiliate` hashtags.
*   Promise: "Get paid faster. 1-tap PayPal withdrawal. Join the waitlist."
*   **Goal:** 5,000 waitlisted creators in 60 days.

### Phase 2: Onboard the Demand (Brands)
*   Direct LinkedIn outbound to Shopify/DTC brand founders selling via Instagram Shop.
*   Offer: "We already have 5,000 vetted creators waiting. Here's a 14-day free trial."
*   **Goal:** 50 paying brands in 90 days.

### Phase 3: The Automated Viral Loop
*   **Trigger:** Brand uses the Automated Outreach tool to DM a creator *not yet on the platform*.
*   **DM Content:** "Hey [Creator]! [Brand] wants to send you a free [Product]. Accept here: [MagicLink]"
*   **Result:** When the cold creator clicks the MagicLink, they are auto-onboarded into the Creator App, expanding the supply side for $0 CAC.

---

## 1.11 Compliance & Legal Framework

### GDPR (EU)
*   All scraping must geo-exclude EU IPs.
*   `DELETE /api/v1/me` endpoint must cascade-delete all PII within 30 days.
*   Cookie consent banner required on all web properties.

### CCPA (California)
*   "Do Not Sell My Information" link in footer.
*   Annual data processing disclosures.

### US Tax Compliance (IRS)
*   Any creator earning > $600/year must submit a W-9 form.
*   Platform must auto-generate and file 1099-NEC forms for all qualifying creators by January 31 of the following year.
*   PayPal Payouts provides payout data via API; a cron job queries annual totals from the `ledger_transactions` table (see [CRON-10](./11_developer_operations.md#112-scheduled-cron-jobs)) to generate filings.

### FTC Endorsement Guidelines
*   All automated DM templates must never impersonate a human without disclosure.
*   All creator briefs generated by AI must include the mandatory `#ad` or `#sponsored` disclosure reminder.

---
