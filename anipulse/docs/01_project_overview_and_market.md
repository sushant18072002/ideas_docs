# 1. Product Requirements Document (PRD) & Market Analysis

> **Cross-References:** This is the foundational Business Analysis document. All technical implementation details are in [03 — Architecture](./03_technical_architecture.md). Monetization and growth strategies are in [04 — Monetization](./04_monetization_and_metrics.md).

## 1.1 Document Control
| Field | Value |
|:---|:---|
| **Document Version** | 1.0 (Enterprise Standard) |
| **Project Code Name** | AniPulse |
| **Author** | Business Analyst / R&D Expert |
| **Last Updated** | 2026-03-21 |
| **Status** | DRAFT — Pending Stakeholder Review |
| **Audience** | Product Managers, Lead Engineers, Marketing Leads |

---

## 1.2 Glossary of Terms
| Abbreviation | Full Form | Definition |
|:---|:---|:---|
| **Simulcast** | Simultaneous Broadcast | Anime episodes broadcasting in Western regions within hours of their Japanese TV release. |
| **MAL** | MyAnimeList | The largest competitor and database for anime tracking. |
| **R2** | Cloudflare R2 | Zero-egress fee object storage used for CDN delivery in this architecture. |
| **DAU / WAU** | Daily/Weekly Active Users | Key metrics tracking user engagement. |
| **PV** | Promotional Video | Essentially a "trailer" for an upcoming anime or season. |
| **Cour** | — | A three-month block of television broadcasting (approx 12-13 episodes). The year is divided into Winter, Spring, Summer, and Fall cours. |
| **Supabase** | — | The open-source Firebase alternative providing the PostgreSQL database for the Admin system. |

---

## 1.3 Executive Summary & Vision Statement
**AniPulse** is a blazing-fast, visually stunning mobile application (built in Flutter) designed for the modern anime watcher. 

**The Vision:** To become the default "daily driver" app for anime fans globally by completely eliminating the friction of tracking what is airing today, when it drops, and breaking news—delivered through an interface that feels like a premium iOS/Android native experience, free from the database bloat of legacy platforms like MAL.

---

## 1.4 The Problem Space (Micro-Level Friction Points)

| # | Friction Point | Current Workaround | Cost of Inaction |
|:--|:---|:---|:---|
| 1 | Finding out precisely what time an episode airs | Googling "Jujutsu Kaisen Episode 14 release time timezone" | Frustrated fans miss drops, get spoiled on X/Twitter. |
| 2 | Tracking across multiple subscriptions (Netflix, CR, HIDIVE) | Using 3 different apps just to see what is available where | Users forget what shows they were watching on niche platforms. |
| 3 | Legacy trackers are incredibly slow on mobile | Waiting 10 seconds for MAL's mobile site to load a heavy database page | High bounce rate; users prefer speed over comprehensive wiki data for daily use. |
| 4 | News is fragmented across X/Twitter and Reddit | Scrolling Reddit manually to find PVs and cast announcements | The casual fan misses major industry announcements. |

---

## 1.5 Stakeholder Map
| Stakeholder | Role in the Platform | Primary KPI |
|:---|:---|:---|
| **System Admin** | Manages the Supabase backend, approves schedule updates, curates news | Data Accuracy (0 missed episode drops) |
| **Mobile User (Free Tier)** | Browses daily schedules, reads news, adds items to local watchlist | D7 Retention & Push Notification CTR |
| **Mobile User (Pro Tier)** | Pays subscription for ad-free experience and custom themes | LTV (Lifetime Value) |

---

## 1.6 Detailed Buyer Personas

### Persona A: Kazuo — The Seasonal Veteran
*   **Demographic:** 24M, Software Engineer. Watches 8-10 airing shows per season.
*   **Technical Proficiency:** High. Frequently uses MAL but hates the mobile app.
*   **Device Usage:** iPhone 15 Pro. Appreciates 120Hz smooth scrolling.
*   **Key Frustration Quote:** *"I don't need a wiki page with all 40 voice actors. I just need to know if the new Solo Leveling episode drops at 9:30 AM or 10:00 AM on Crunchyroll."*
*   **Success Metric:** He opens the app every morning while commuting just to check the "Today" tab.

### Persona B: Chloe — The Casual Binger
*   **Demographic:** 19F, College Student. Watches 2-3 massive hits simultaneously.
*   **Technical Proficiency:** Moderate. Heavy TikTok user.
*   **Device Usage:** Android (Samsung S23). 
*   **Key Frustration Quote:** *"I just saw a TikTok edit of a new anime and I want to watch it, but I don't know what day it airs or where it's streaming legally."*
*   **Success Metric:** She relies on AniPulse push notifications ("Episode 5 is live!") rather than opening the app proactively.

---

## 1.7 Competitive Landscape Analysis

| Feature | **MyAnimeList** | **LiveChart.me** | **Crunchyroll App** | **AniPulse (Our App)** |
|:---|:---|:---|:---|:---|
| Focus | Giant Database | Calendar & Details | Streaming Only | **Hyper-Fast Calendar & News** |
| Platform Independent | ✅ Yes | ✅ Yes | ❌ CR only | ✅ Yes |
| UI/UX Quality | Clunky, Web-first | Basic, Utility-focused | Premium but restricted | **Premium, Native 120Hz Flutter** |
| Push Notifications | Partial | ✅ Yes | CR shows only | ✅ **Smart & Granular** |
| Mobile Speed | 🔴 Slow (Database heavy) | 🟡 Medium | 🟡 Medium | 🟢 **Ultra-Fast (Edge JSON)** |
| Community Features | Massive Forums | None | Comments | Future Phase |

---

## 1.8 Risk Register

| Risk ID | Category | Risk Description | Likelihood | Impact | Mitigation Strategy |
|:---|:---|:---|:---|:---|:---|
| R-001 | Data Sourcing | Manual data entry becomes too time-consuming for admins. | HIGH | CRITICAL | Implement backend scrapers (Python + Supabase Cron) to auto-fetch times from the AniList GraphQL API, only requiring admin *approval* rather than manual typing. |
| R-002 | Platform | Cloudflare R2 free limits exceeded if app goes viral. | LOW | LOW | R2 charges $0 for egress. Overages on read operations ($0.36 per million) are exceptionally cheap and easily covered by Admob revenue. |
| R-003 | App Store | Apple rejects the app citing "copyright infringement" for showing anime posters. | MEDIUM | HIGH | Comply with "Fair Use". Use official API metadata, do not host video content. State clearly "Unofficial Tracker Tracker" in description. |

---

## 1.9 Compliance & Privacy
*   **COPPA Compliance:** The app must ask for age via a standard birth year dial if handling user data, or simply serve non-personalized ads to users who opt out of tracking.
*   **GDPR/CCPA:** Users must be able to delete their Supabase Auth account and purge all watchlist data via a single button in settings.
