# 1. Product Requirements Document (PRD) & Market Analysis

> **Cross-References:** Features → [02 — Features](./02_core_features_and_roadmap.md) · Architecture → [03 — Architecture](./03_technical_architecture.md) · Monetization → [04 — Monetization](./04_monetization_and_metrics.md) · Scraping → [10 — Scraping](./10_data_aggregation_and_scraping.md).

## 1.1 Document Control
| Field | Value |
|:---|:---|
| **Document Version** | 2.0 |
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
| **MAL** | MyAnimeList | The largest legacy database and tracker for anime with 15M+ monthly users. |
| **AniList** | — | A modern, developer-friendly competitor to MAL with a public GraphQL API and superior UI. |
| **R2** | Cloudflare R2 | Zero-egress-fee object storage used for static JSON delivery in this architecture. |
| **DAU / WAU / MAU** | Daily / Weekly / Monthly Active Users | Key engagement metrics. WAU is the north-star metric for AniPulse. |
| **PV** | Promotional Video | A "trailer" for an upcoming anime or new season, typically 1-2 minutes, hosted on YouTube. |
| **Cour** | — | A 3-month block of Japanese TV broadcasting (~12-13 episodes). Winter (Jan-Mar), Spring (Apr-Jun), Summer (Jul-Sep), Fall (Oct-Dec). |
| **Key Visual (KV)** | — | The official marketing poster/artwork released by a studio to announce or promote an anime. |
| **OVA / ONA** | Original Video/Net Animation | Anime produced directly for home video or streaming, not traditional TV broadcast. |
| **Supabase** | — | Open-source Firebase alternative providing PostgreSQL, Auth, Edge Functions, and Storage. |
| **FCM** | Firebase Cloud Messaging | Google's free push notification service for iOS and Android. |
| **ASO** | App Store Optimization | The process of optimizing a mobile app's listing to rank higher in App Store / Play Store search results. |
| **ARPU** | Average Revenue Per User | Monthly revenue divided by active users; key unit economics metric. |
| **CPI** | Cost Per Install | Marketing spend required to acquire one app download. |
| **D1 / D7 / D30** | Day-1 / Day-7 / Day-30 Retention | Percentage of users returning to the app after 1, 7, or 30 days. |

---

## 1.3 Executive Summary & Vision Statement

**AniPulse** is a blazing-fast, visually stunning mobile application (built in Flutter for iOS & Android) designed for the modern anime watcher.

**The Vision:** To become the default "daily driver" app for anime fans globally by eliminating the friction of tracking what is airing today, when it drops, where to watch it, and what's happening in the anime world—delivered through an interface that feels premium, native, and free from the database bloat of legacy platforms.

**The One-Liner:** *"Your anime drops. Instantly."*

### What AniPulse Is:
*   A hyper-fast **daily schedule calendar** with live countdown timers.
*   A curated **anime news feed** with embedded trailers and key visuals.
*   A **unified "Where to Watch"** directory across Crunchyroll, Netflix, HIDIVE, Amazon, and Disney+.
*   An **offline-capable**, ad-supported free app with an optional Pro tier.

### What AniPulse Is NOT:
*   Not a streaming service (we don't host video content).
*   Not a full database/wiki (we don't attempt to replicate MAL's 60,000+ entries).
*   Not a social media platform (community features are Phase 3, not MVP).

---

## 1.4 Market Opportunity

### 1.4.1 Global Anime Industry Size
The global anime market is valued at approximately **$31-38 Billion USD in 2025** and is projected to reach **$68-77 Billion by 2033** (CAGR of 7-10%). This represents one of the fastest-growing entertainment sectors globally.

### 1.4.2 Target Audience Demographics
| Demographic Factor | Data Point | Source Year |
|:---|:---|:---|
| Primary Age Group | **Gen Z (18-29)** holds 37.86% market share | 2025 |
| Gender Split | 55% Male / 45% Female (up from 65/35 in 2020) | 2023 |
| Weekly Engagement | 3 in 10 global consumers watch anime *at least once per week* | 2024 |
| Device Preference | Mobile captures **65% of total anime viewership hours** | 2023 |
| Completion Rate | 70% of fans complete full seasons (high retention behavior) | 2023 |
| Average Viewer Age | **24 years** (down from 28 in 2019 — audience is getting younger) | 2023 |

### 1.4.3 The Addressable Market for a Tracker App
*   MAL has **~15 million active users**. AniList has **~8 million active users**.
*   Reddit's `r/anime` has **~8.5 million subscribers**.
*   Even capturing **1%** of the combined MAL/AniList user base = **230,000 users**, which is a viable business at our cost structure.

---

## 1.5 The Problem Space (Micro-Level Friction Points)

| # | Friction Point | Current Workaround | Cost of Inaction | AniPulse Solution |
|:--|:---|:---|:---|:---|
| 1 | **"What time does my episode air in MY timezone?"** | Googling "JJK Episode 14 release time EST" every single week | Fans miss drops, get spoiled on X/Twitter within minutes | Live countdown timers auto-localized to device timezone |
| 2 | **"Which platform has this show?"** | Checking 3-4 streaming apps manually | Users pay for subscriptions they forget to cancel for shows that moved platforms | Unified "Where to Watch" with deep links to every platform |
| 3 | **"I can't find simple airing info without wading through forums"** | Opening MAL, waiting 8-10s for a bloated page to load | High bounce rate; users give up and just Google it | Ultra-fast static JSON rendering; entire schedule loads in <500ms |
| 4 | **"MAL/AniList separates seasons of the same show"** | Manually linking Part 1, Part 2, Movie entries | Users lose track of which "entry" they were on | Grouped show hierarchy: Series → Seasons → Episodes in a single view |
| 5 | **"I want a tracker, not a news agency with forums"** | Using MAL/AniList despite disliking the clutter | Feature fatigue; users stop engaging with the tracker portion | Clean, focused MVP: Calendar + News only. No forums, no wiki bloat |
| 6 | **"No automatic sync with my streaming app"** | Manually marking episodes as watched | Users stop tracking because it's too much effort | Phase 2: Auto-detect via deep link return + manual quick-tap "Watched" |

---

## 1.6 Stakeholder Map
| Stakeholder | Role in the Platform | Primary KPI | Phase |
|:---|:---|:---|:---|
| **System Admin (SuperAdmin)** | Manages database, approves scraped data, curates news, controls CDN cache | Data Accuracy (0 missed episode drops per week) | MVP |
| **Content Editor** | Writes news articles, manages editorial calendar | News freshness (articles published within 2h of announcement) | MVP |
| **Mobile User (Free Tier)** | Browses schedules, reads news, uses local watchlist | D7 Retention & Push Notification CTR | MVP |
| **Mobile User (Pro Tier)** | Pays subscription for ad-free experience and custom themes | LTV (Lifetime Value) & Churn Rate | Phase 2 |

---

## 1.7 Detailed Buyer Personas

### Persona A: Kazuo — The Seasonal Veteran
*   **Demographic:** 24M, Software Engineer, Tokyo → relocated to London.
*   **Anime Consumption:** Watches 8-12 airing shows per season (heavy seasonal watcher).
*   **Current Tools:** AniList (web), LiveChart.me (for schedule only).
*   **Technical Proficiency:** High. Uses custom CSS on AniList. Has tried building his own tracker bot.
*   **Device:** iPhone 15 Pro (appreciates 120Hz smooth scrolling).
*   **Key Frustration:** *"I don't need a wiki page with all 40 voice actors. I just need to know if the new Solo Leveling episode drops at 9:30 AM or 10:00 AM GMT on Crunchyroll."*
*   **Willingness to Pay:** Would pay $1.99/mo for ad-free + custom themes.
*   **Success Metric:** Opens the app every morning during his commute to check "Today" tab. Replaces his LiveChart bookmark.

### Persona B: Chloe — The Casual Binger
*   **Demographic:** 19F, College Student, Austin TX.
*   **Anime Consumption:** Watches 2-3 mega-hit shows only (Demon Slayer, One Piece, JJK).
*   **Current Tools:** None. Finds out about episodes from TikTok edits.
*   **Technical Proficiency:** Low. Mobile-only. Heavy TikTok and Instagram user.
*   **Device:** Samsung Galaxy S23 (Android).
*   **Key Frustration:** *"I just saw a TikTok edit of a new anime and I want to watch it, but I don't know what day it airs or where it's streaming legally."*
*   **Willingness to Pay:** Unlikely. Ad-tolerant.
*   **Success Metric:** She relies on AniPulse push notifications ("Episode 5 is live on Netflix!") rather than opening the app proactively.

### Persona C: Raj — The Manga-to-Anime Crossover
*   **Demographic:** 21M, CS Student, Bangalore, India.
*   **Anime Consumption:** Reads manga chapters weekly, watches 4-5 anime adaptations per season to compare.
*   **Current Tools:** MAL (manga tracking), Reddit (anime news).
*   **Technical Proficiency:** Moderate. Comfortable with apps but not technical tools.
*   **Device:** OnePlus 12 (Android). Data-conscious (wants offline mode).
*   **Key Frustration:** *"I want to know when the anime adaptation of a manga I'm reading is getting announced or airing. I always find out late from random Reddit posts."*
*   **Willingness to Pay:** Yes, if the Pro tier includes offline features (he has limited mobile data).
*   **Success Metric:** Uses AniPulse news feed as his primary source for adaptation announcements.

### Persona D: Sofia — The Event-Going Superfan
*   **Demographic:** 27F, Graphic Designer, São Paulo, Brazil.
*   **Anime Consumption:** Watches 5+ shows, attends anime conventions, collects figures.
*   **Current Tools:** Crunchyroll app + Twitter for news.
*   **Technical Proficiency:** Moderate.
*   **Device:** iPhone 14.
*   **Key Frustration:** *"I wish there was one app that told me about upcoming anime events, new figure pre-orders, and when my shows air. I check 5 different sources daily."*
*   **Willingness to Pay:** Yes. Active spender on anime merchandise.
*   **Success Metric:** Uses AniPulse as her single anime information hub alongside Crunchyroll for watching.

---

## 1.8 Competitive Landscape Analysis

### 1.8.1 Feature Comparison Matrix

| Feature | **MyAnimeList** | **AniList** | **LiveChart.me** | **Crunchyroll** | **AniPulse** |
|:---|:---|:---|:---|:---|:---|
| **Primary Focus** | Giant Database + Wiki | Modern Database + Social | Calendar + Details | Streaming Platform | **Hyper-Fast Calendar + News** |
| **Platform Independent** | ✅ | ✅ | ✅ | ❌ CR-only | ✅ |
| **Native Mobile App** | ✅ (Poor UX) | ❌ (3rd-party only) | ❌ (Web only) | ✅ (Premium) | ✅ **Native Flutter** |
| **Live Countdown Timers** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **"Where to Watch" Links** | ❌ | ❌ | ✅ | ❌ | ✅ **Deep Links** |
| **Push Notifications** | ❌ | ❌ (3rd party) | ❌ | CR shows only | ✅ **Per-Show Granular** |
| **News Feed** | ❌ | ❌ | Minimal | ✅ CR-only news | ✅ **Curated + Embedded PVs** |
| **Offline Mode** | ❌ | ❌ | ❌ | ✅ (Premium DL) | ✅ **Cached JSON** |
| **Mobile Load Speed** | 🔴 8-12s | 🟡 3-5s | 🟡 4-6s | 🟡 3-5s | 🟢 **<500ms (Static Edge)** |
| **Season Grouping** | ❌ Separate entries | ❌ Separate entries | ✅ | ❌ | ✅ **Grouped View** |
| **Pricing** | Free (Ads) | Free | Free | $7.99/mo | **Free (Ads) / $1.99 Pro** |

### 1.8.2 Competitive SWOT

| | Strengths | Weaknesses |
|:---|:---|:---|
| **AniPulse** | Ultra-fast, focused UX. $0 server costs. Push notifications. Offline. | No existing user base. Small data team. No community features at launch. |

| | Opportunities | Threats |
|:---|:---|:---|
| **AniPulse** | No major competitor offers a fast, dedicated *mobile* schedule app. Gen Z mobile-first behavior. TikTok viral marketing. | MAL/AniList could build a better mobile app. Crunchyroll could add cross-platform schedule features. |

---

## 1.9 Risk Register

| Risk ID | Category | Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|:---|:---|
| R-001 | Data | Manual data entry via Chrome Extension becomes too time-consuming as the catalog grows beyond 100 shows/season | HIGH | HIGH | Build configurable DOM selectors in the extension so new sites can be added without code changes. Use Anikoto.me as primary source + AniList API as fallback. |
| R-002 | Legal | Apple/Google rejects app citing "copyright" for displaying anime cover art/posters | MEDIUM | HIGH | Use only publicly available metadata and images from official press kits. Mark app as "Unofficial Fan Tool." Do not host any video content. |
| R-003 | Market | MAL or AniList launches a high-quality mobile schedule app with push notifications, eliminating our USP | LOW | CRITICAL | Execute rapidly. Ship MVP in 8 weeks. Build brand loyalty before incumbents react. Differentiate on "Where to Watch" cross-platform links which MAL/AniList historically refuse to implement. |
| R-004 | Technical | Anikoto.me or target scraping sites change their HTML structure, breaking the Chrome Extension | HIGH | MEDIUM | Extension uses configurable CSS selectors stored in a JSON config file. When a site changes, update the config—no code deployment needed. |
| R-005 | Financial | AdMob eCPM drops below $1 CPM for anime demographics, making the ad model unsustainable | LOW | MEDIUM | Diversify revenue: affiliate links (Crunchyroll, Amazon), merchandise affiliates (Good Smile Company), and Pro subscriptions. |

---

## 1.10 Compliance & Privacy Framework

### 1.10.1 COPPA (Children's Online Privacy Protection)
*   The app targets users 13+. If a user enters a birth year indicating they are under 13, the app must:
    *   Block account creation entirely.
    *   Serve only non-personalized AdMob ads (via `tagForChildDirectedTreatment` flag).

### 1.10.2 GDPR (EU Users)
*   Users must consent to data collection via a clear in-app prompt on first launch.
*   A "Delete My Account" button in Settings must cascade-delete all PII (email, watchlist, FCM tokens) from Supabase within 72 hours.
*   The privacy policy must clearly state: what data is collected, why, and how long it is retained.

### 1.10.3 CCPA (California Users)
*   "Do Not Sell My Personal Information" link must be accessible in Settings.
*   Annual data processing disclosures.

### 1.10.4 App Store Compliance
*   **Apple App Store:** Must include a privacy nutrition label. In-app purchases (Pro tier) must use Apple's native StoreKit API (no third-party payment processors).
*   **Google Play Store:** Must comply with Google's Families Policy if any content is flagged as "for children."
