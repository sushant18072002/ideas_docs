# 4. Monetization, Growth & Metrics

> **Cross-References:** Pricing tiers → [08 — RBAC](./08_business_rules_and_rbac.md) · Push notification strategy → [09 — Notifications](./09_notifications_and_cron.md) · Market demographics → [01 — PRD](./01_project_overview_and_market.md#14-market-opportunity).

## 4.1 Revenue Streams

### 4.1.1 Stream A: AdMob Native Ads (Free Tier Users)
*   **Placement:** Native ad units injected into the News Feed every 5th card, styled identically to news cards with a subtle "Sponsored" label.
*   **Ad Format:** Google AdMob Native Advanced. No banners. No interstitials. No pop-ups. User experience is sacred.
*   **Expected eCPM:** $2-5 CPM for anime/entertainment demographics (US/EU). $0.50-1.50 for India/SEA.
*   **Revenue Model:** `Monthly Ad Revenue = DAU × Sessions/Day × Ads/Session × eCPM / 1000`

### 4.1.2 Stream B: Affiliate Revenue
*   **"Where to Watch" Links:** Every streaming platform button (Crunchyroll, Netflix, Amazon) can be wrapped in an affiliate tracking URL via networks like **Impact, ShareASale**, or direct partner programs.
*   **Payout:** $2-10 per new subscription generated. At 10,000 MAU with 1% conversion = 100 signups/month × $5 = **$500/mo passive.**
*   **Merchandise:** Occasional curated cards in the News Feed linking to official merch (Good Smile Company, RightStuf/Crunchyroll Store) with affiliate tags. Commission: 5-10%.

### 4.1.3 Stream C: AniPulse PRO Subscription
*   **Pricing:** $1.99/month or $14.99/year (25% annual discount).
*   **Payment Processor:** Apple StoreKit + Google Play Billing via **RevenueCat** (free under 2,500 MAU revenue).

| PRO Feature | Description |
|:---|:---|
| **Ad-Free** | Removes all AdMob native ad units from News Feed and Schedule. |
| **Custom Themes** | Unlock accent color picker + premium dark/light themes. |
| **Custom App Icons** | Alternate app icons featuring anime aesthetic styles. |
| **Offline Plus** | Auto-downloads high-res cover art and PV thumbnails for offline viewing. |
| **Early Access** | Beta access to upcoming features (Social, Community). |

---

## 4.2 Growth & Go-To-Market (GTM) Strategy

### 4.2.1 Phase 1: Pre-Launch Hype (Weeks -4 to 0)
*   Create a landing page (`anipulse.app`) with an email waitlist + App Store pre-order link.
*   Post 3-4 TikTok/Reels showing the app UI with trending anime audio. Target: 100K organic views.
*   Post a detailed announcement thread on `r/anime` subreddit with screenshots.
*   **Goal:** 2,000 email signups before launch day.

### 4.2.2 Phase 2: Launch Week (Week 1)
*   Coordinate launch with the start of a new Anime Season (April 2026 = Spring Season).
*   Reach out to 5-10 mid-tier anime TikTok editors (50K-150K followers). Pay $50-100 per video for a 3-second outro: *"Track every anime drop on AniPulse — link in bio."*
*   Cross-post the season schedule graphic (watermarked "AniPulse") to `r/anime`, `r/animemes`, MyAnimeList forums.
*   **Goal:** 5,000 installs in Week 1.

### 4.2.3 Phase 3: Ongoing Growth Engine
*   **Season Calendar Virality:** Every 3 months, a new anime season starts. AniPulse publishes a beautifully designed, shareable season calendar graphic. This becomes a recurring viral moment.
*   **Discord Bot Integration:** Build a simple Discord bot that posts "Episode Dropped!" alerts to anime servers, with a "Powered by AniPulse" attribution and download link.
*   **ASO (App Store Optimization):**
    *   Primary Keywords: `anime schedule`, `anime calendar`, `anime episode tracker`, `anime countdown timer`
    *   Screenshots: Dark mode UI, countdown timers, "Where to Watch" buttons
    *   A/B test app icon (generic anime aesthetic vs. AniPulse branded)

---

## 4.3 Key Performance Indicators (KPIs)

| Metric | Definition | Golden Target | Danger Zone | How to Track |
|:---|:---|:---|:---|:---|
| **D1 Retention** | % of users opening app 1 day after install | > 45% | < 30% | Firebase Analytics |
| **D7 Retention** | % of users opening app 7 days later | > 25% | < 15% | Firebase Analytics |
| **D30 Retention** | % of users opening app 30 days later | > 12% | < 8% | Firebase Analytics |
| **WAU (Weekly Active Users)** | Unique users per week | Growth: +10% WoW | Decline: -5% WoW | Firebase Analytics |
| **WAU/MAU Ratio (Stickiness)** | WAU divided by MAU | > 40% | < 25% | Calculated |
| **Push Notification CTR** | % of pushes tapped | > 8% | < 3% | FCM Analytics |
| **CPI (Cost Per Install)** | Paid acquisition cost per download | < $0.40 | > $1.00 | TikTok Ads Manager |
| **ARPU (Avg Revenue Per User)** | Monthly revenue / Active users | > $0.10 | < $0.03 | RevenueCat + AdMob |
| **PRO Conversion Rate** | Free users who upgrade to PRO | > 3% | < 1% | RevenueCat |
| **App Store Rating** | Average star rating | > 4.5 ★ | < 4.0 ★ | App Store Connect / Play Console |

---

## 4.4 Unit Economics & Break-Even Analysis

### 4.4.1 Cost Structure (Monthly)
| Cost Item | Amount | Notes |
|:---|:---|:---|
| Apple Developer Account | $8.25/mo ($99/yr) | Required for iOS distribution |
| Google Play Developer | $2.08/mo ($25 one-time, amortized) | Required for Android |
| Domain (anipulse.app) | $1/mo ($12/yr) | Landing page + email |
| Supabase | $0 | Free tier: 500MB, 50K MAU |
| Cloudflare R2 | $0 | Free tier: 10M reads/mo, $0 egress |
| Vercel (Admin Dashboard) | $0 | Hobby tier |
| Firebase (FCM + Analytics) | $0 | Free |
| **Total Fixed OPEX** | **~$12/month** | |

### 4.4.2 Revenue Projection (Conservative)
| Milestone | MAU | Ad Revenue | Affiliate | PRO Subs | Total MRR |
|:---|:---|:---|:---|:---|:---|
| Month 3 | 5,000 | $50 | $25 | $20 (10 users) | $95 |
| Month 6 | 15,000 | $200 | $100 | $120 (60 users) | $420 |
| Month 12 | 50,000 | $750 | $300 | $600 (300 users) | $1,650 |
| Month 24 | 150,000 | $2,500 | $1,000 | $3,000 (1,500 users) | $6,500 |

### 4.4.3 Break-Even Point
With $12/mo fixed costs and near-zero variable costs (R2 egress is free), the app reaches operational break-even at **~500 MAU** (ad revenue alone). The paid acquisition investment ($3,500 for 10,000 users via TikTok) pays back within **5-7 months** from combined ad + affiliate revenue.
