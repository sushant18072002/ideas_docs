# 2. Core Features & Roadmap

> **Cross-References:** User stories for each feature → [05 — App Stories](./05_user_stories_app.md) · Screen specifications → [07 — Screens](./07_screen_specifications.md).

## 2.1 Feature ID Convention
Every feature is assigned a unique ID: `F-XX`. User Stories in Documents 05 and 06 reference these IDs to maintain traceability.

---

## 2.2 Epic: The Daily Pulse (Home Screen)

The core landing experience. This is the first thing users see. It must answer one question instantly: *"What's happening in anime today?"*

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-01 | **Today's Schedule List** | A vertical list of all anime airing *today*, sorted chronologically by air time. Each card shows title, poster, studio, streaming platform, and a live countdown timer that ticks every second. | P1 (Must) | MVP |
| F-02 | **Day Selector** | Horizontal pill-shaped tab bar (`Mon` thru `Sun`). Swiping left/right or tapping a day changes the schedule. The current day is pre-selected and highlighted. Supports "Yesterday" and "Tomorrow" edge navigation. | P1 (Must) | MVP |
| F-03 | **Quick-Add to Watchlist** | A circular `+` button on every schedule card. Single tap toggles the anime into the user's local "Watching" list. Visual feedback: icon morphs into a checkmark with a micro-animation. | P1 (Must) | MVP |

---

## 2.3 Epic: The Comprehensive Calendar

For users who want to plan their entire week or discover the full seasonal lineup.

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-04 | **Weekly Grid View** | A 7-column grid (Mon-Sun) showing small poster thumbnails for each day. Tapping a day drills into that day's full schedule list (S-01). | P2 (Should) | MVP |
| F-05 | **Seasonal Overview** | A macro grid view displaying *every* anime airing in the current Cour (e.g., "Spring 2026"). Clustered by genre or sorted by popularity. Shows 2:3 poster art in a responsive `GridView`. | P1 (Must) | MVP |
| F-06 | **Timezone Auto-Localization** | All times stored in the JSON are strictly UTC. The Flutter app converts them to the user's device locale timezone (e.g., `JST → EST`). Users never see UTC. A "Timezone" label in Settings confirms the detected zone. | P1 (Must) | MVP |

---

## 2.4 Epic: Anime Details Page

The deep-dive view for a specific anime. Opened from any schedule card or seasonal grid item.

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-07 | **Unified Detail Sheet** | A draggable bottom modal (covers 85% of screen) showing: hero banner image, title (EN + JP), synopsis (expandable), genre pills, studio, episode count, MAL score, and air day/time. | P1 (Must) | MVP |
| F-08 | **"Where to Watch" Deep Links** | Actionable rectangular buttons with platform logos (Crunchyroll, Netflix, HIDIVE, Amazon, Disney+, Hulu). Tapping opens the respective app via URI deep link (`crunchyroll://series/...`). Falls back to web URL if app not installed. | P1 (Must) | MVP |
| F-09 | **Episode Tracker** | Horizontal scrollable row of episode numbers (Ep 1, Ep 2, ...). Each episode has a status: `Aired` (tappable to mark as watched), `Upcoming` (countdown), `Delayed` (red tag), `Cancelled` (greyed). | P2 (Should) | MVP |
| F-10 | **Embedded PV/Trailer Player** | If a YouTube PV URL exists in the data, an inline video player renders below the synopsis. Auto-pauses when scrolled away. Uses `youtube_player_iframe` Flutter package. | P2 (Should) | MVP |

---

## 2.5 Epic: News Feed ("What's New in Anime")

A curated editorial stream of anime-world announcements.

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-11 | **Infinite Scroll News Feed** | Vertical feed of news cards. Each card: headline, source attribution, timestamp ("2h ago"), and a 16:9 cover image or embedded YouTube iframe. Paginated — loads 20 cards at a time, fetches next batch on scroll. | P1 (Must) | MVP |
| F-12 | **Share to Social** | A share icon on each news card triggers the native iOS/Android share sheet, sending a formatted deep link or text summary to WhatsApp, Instagram, X, etc. | P2 (Should) | MVP |
| F-13 | **News Category Chips** | Filter chips at the top of the feed: `[All] [Announcements] [Trailers] [Season Renewals] [Events]`. Default: "All". | P3 (Could) | Phase 2 |

---

## 2.6 Epic: User Watchlist & Profiles

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-14 | **Local-First Watchlist** | Users can organize anime into: "Watching" (with episode progress), "Plan to Watch", "Completed", "Dropped". Data stored in `SQFlite` on device. No account required. | P1 (Must) | MVP |
| F-15 | **Cloud Sync** | If a user logs in via Supabase Auth (Google/Apple OAuth), their local `SQFlite` watchlist merges with the cloud `user_watchlists` table. Enables cross-device sync. | P2 (Should) | Phase 2 |
| F-16 | **Profile Page** | Shows username, avatar, and watchlist stats: "X shows watching, Y completed, Z total episodes." No social features in MVP. | P3 (Could) | Phase 2 |

---

## 2.7 Epic: Push Notifications

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-17 | **Per-Show Episode Alert** | The instant an episode's `air_datetime_utc` arrives, a push notification fires to all users subscribed to that anime's FCM Topic. Payload: "Jujutsu Kaisen Ep 14 is now live on Crunchyroll!" | P1 (Must) | Phase 2 |
| F-18 | **Granular Notification Settings** | Users can toggle: (1) All Notifications ON/OFF, (2) Per-show bell icon ON/OFF on the detail page. Settings persisted in local storage and FCM topic subscriptions. | P2 (Should) | Phase 2 |
| F-19 | **Weekly Recap Push** | Every Sunday at 10:00 AM user-local-time, a single batch notification: "This week's top drops: [Show A] ★9.1, [Show B] ★8.7, [Show C] ★8.5." | P3 (Could) | Phase 2 |

---

## 2.8 Epic: Settings & Preferences

| ID | Feature | Description | Priority | Phase |
|:---|:---|:---|:---|:---|
| F-20 | **Theme Toggle** | Dark Mode (default, OLED black `#000000`) / Light Mode. Pro users get custom accent color pickers. | P2 (Should) | MVP |
| F-21 | **Language Preference** | Anime titles can display in English, Romaji, or Native Japanese. User selects preference in Settings; affects all cards globally. | P3 (Could) | Phase 2 |
| F-22 | **Delete Account** | One-tap button that calls a Supabase Edge Function to cascade-delete all PII, watchlists, and FCM tokens. Required for GDPR compliance. | P1 (Must) | Phase 2 |

---

## 2.9 Phase Rollout Roadmap

### Phase 1: MVP — "The Static Edge" (Weeks 1-8)
*   **Goal:** Launch a zero-server-cost app that proves the UI/UX and validates demand.
*   **Features:** F-01 through F-14, F-20.
*   **Architecture:** Admin curates data via Chrome Extension → Local Admin Dashboard (localhost) → Supabase DB → Cloudflare Worker generates static JSON → R2 bucket. Flutter app does HTTP GET on launch.
*   **No user accounts.** No push notifications. Pure read-only experience.
*   **Success Gate:** 1,000 organic installs within 30 days of launch. D7 retention > 20%.

### Phase 2: Engagement — "The Personalization Layer" (Weeks 9-16)
*   **Goal:** Increase D7 retention from 20% to 35% through personalization and notifications.
*   **Features:** F-15 through F-22.
*   **Architecture:** Introduce Supabase Auth (Google/Apple). User watchlists sync to `user_watchlists` table. Supabase Edge Function triggers FCM when `air_datetime_utc` fires.
*   **Success Gate:** 10,000 WAU. Push Notification CTR > 8%.

### Phase 3: Community — "The Social Moat" (Weeks 17-24)
*   **Goal:** Build a competitive moat by adding social features no other schedule app offers.
*   **Features:** Episode discussion threads, user ratings/reviews, "Share My Schedule" cards to Instagram Stories, dark social referral tracking.
*   **Success Gate:** User-generated content (reviews) contributing to D30 retention > 15%.
