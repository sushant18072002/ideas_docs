# 5. User Stories: Flutter App (End User)

> **Format:** As a [Role], I want to [Action] so that [Benefit/Outcome].
> **Priority:** P1 = Must Have (MVP), P2 = Should Have, P3 = Could Have, P4 = Won't Have (this version).
> **Traceability:** Each story maps to a Feature ID from [02 — Features](./02_core_features_and_roadmap.md).

---

## 5.1 Epic: First Launch & Onboarding

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-01 | As a new user, I want the app to open instantly to today's schedule without requiring any login or setup, so I get immediate value. | P1 | F-01 | 1. No login screen on first launch. 2. Schedule renders from cached/default data within 1 second. 3. Data fetches silently in background. |
| APP-02 | As a first-time user, I want a 3-screen onboarding carousel explaining the app's core features (Schedule, News, Watchlist), so I understand the value before I start browsing. | P2 | — | 1. Shows only once. 2. Dismissible via "Skip". 3. Final screen has CTA: "Get Started". |

## 5.2 Epic: Daily Schedule (The Core Pulse)

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-03 | As a fan, I want to see a localized countdown timer for each anime airing today, so I know exactly when to tune in. | P1 | F-01 | 1. Timer ticks every second via `Timer.periodic`. 2. Auto-converts from UTC to device timezone. 3. Card transitions from "Upcoming" → "Aired ✓" when timer expires. |
| APP-04 | As a user, I want to swipe between days (Mon-Sun) or tap a day pill, so I can see what aired yesterday or what's coming tomorrow. | P1 | F-02 | 1. `PageView` or `TabBar` navigation. 2. Active day has a highlighted pill. 3. Animates smoothly at 60fps. |
| APP-05 | As a power user, I want to tap a "+" button on any schedule card to instantly add it to my Watchlist, so I can build my personal roster without leaving the schedule. | P1 | F-03 | 1. `+` icon toggles to `✓` with a micro-animation (scale bounce). 2. Writes to local `SQFlite`. 3. Haptic feedback on iOS. |
| APP-06 | As a user, I want to see the streaming platform logo (e.g., Crunchyroll icon) directly on the schedule card, so I know at a glance where to watch without tapping into details. | P1 | F-08 | 1. Small 24×24 platform logos rendered beside the countdown timer. 2. Max 2 logos shown; "…" if more. |

## 5.3 Epic: The Comprehensive Calendar

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-07 | As a planner, I want a weekly grid view (Mon-Sun) showing thumbnail posters, so I can visualize my entire anime week at a glance. | P2 | F-04 | 1. 7-column responsive grid. 2. Tapping a day scrolls to the detailed schedule list for that day. |
| APP-08 | As a seasonal explorer, I want to browse all shows airing in the current season (e.g., "Spring 2026") in a poster grid, sorted by popularity. | P1 | F-05 | 1. 2-3 column `GridView` with 2:3 ratio poster cards. 2. Genre filter chips at top. 3. Tap opens detail sheet. |

## 5.4 Epic: Anime Details & "Where to Watch"

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-09 | As a curious viewer, I want to see the synopsis, genres, studio, MAL score, and episode count when I tap on any anime, so I can decide if it's worth watching. | P1 | F-07 | 1. Bottom modal sheet covers 85% of screen. 2. Hero banner image with parallax scroll. 3. Synopsis expandable ("Read More" toggle). |
| APP-10 | As a subscriber, I want to tap a streaming platform button and be deep-linked directly to that show in the Crunchyroll/Netflix/HIDIVE app, so I can start watching in one tap. | P1 | F-08 | 1. Uses platform-specific URI schemes (`crunchyroll://`). 2. Falls back to web URL if app not installed. 3. Tracks tap for affiliate attribution. |
| APP-11 | As an organized viewer, I want to see a horizontal episode tracker with per-episode status (Aired/Upcoming/Delayed), so I can see my progress. | P2 | F-09 | 1. Horizontal scrollable `ListView`. 2. Aired episodes tappable to mark as "Watched" (filled circle). 3. Upcoming episodes show mini countdown. |
| APP-12 | As a hype-driven fan, I want to watch the official trailer/PV inside the detail page without leaving the app. | P2 | F-10 | 1. YouTube iframe embedded below synopsis. 2. Auto-pauses when scrolled away. 3. Graceful fallback if no PV URL exists. |

## 5.5 Epic: News Feed

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-13 | As an engaged fan, I want a vertical infinite-scroll feed of anime news with cover images and embedded trailers. | P1 | F-11 | 1. Loads 20 cards initially. 2. Fetches next 20 on scroll-to-bottom. 3. Pull-to-refresh fetches latest `news.json`. |
| APP-14 | As a social user, I want to share a news article to WhatsApp/Instagram/X via the native share sheet. | P2 | F-12 | 1. Share icon on each card. 2. Shares formatted text: "📺 [Headline] — Read more on AniPulse". |

## 5.6 Epic: Watchlist & Profile

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-15 | As a tracker, I want to organize my anime into tabs: "Watching", "Plan to Watch", "Completed", "Dropped". | P1 | F-14 | 1. Tabbed view with counts. 2. Swipe-to-delete with undo snackbar. 3. Data persists in local `SQFlite`. |
| APP-16 | As a returning user on a new phone, I want to sign in with Google/Apple and have my entire watchlist restored from the cloud. | P2 | F-15 | 1. OAuth via Supabase Auth. 2. On first login, merges local data to cloud (conflict resolution: cloud wins for duplicates). |
| APP-17 | As a privacy-conscious user, I want a "Delete My Account" button that permanently removes all my data. | P1 | F-22 | 1. Confirmation dialog. 2. Calls Supabase Edge Function. 3. Cascade-deletes auth, watchlist, FCM tokens within 72 hours. |

## 5.7 Epic: Push Notifications

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-18 | As a tracker, I want a push notification the instant an episode I'm tracking is released, so I can watch before spoilers hit social media. | P1 | F-17 | 1. FCM Topic subscription on anime ID. 2. Notification payload: title, episode number, platform. 3. Tapping opens detail page. |
| APP-19 | As a casual user, I want to toggle notifications on/off per individual show, so I'm not spammed by shows I casually track. | P2 | F-18 | 1. Bell icon toggle on detail page. 2. Persists subscription state in `SharedPreferences` + FCM Topic. |
| APP-20 | As a weekend warrior, I want a single "Weekly Recap" push on Sunday summarizing the best drops of the week. | P3 | F-19 | 1. Sent at 10:00 AM user-local-time. 2. Lists top 3 highest-rated episodes. |

## 5.8 Epic: Settings & Customization

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-21 | As a Pro user, I want to change the app's accent color to match my favorite character aesthetic. | P3 | F-20 | 1. Color picker in Settings (PRO only). 2. Changes propagate instantly to all UI elements. |
| APP-22 | As a bilingual fan, I want to choose whether anime titles display in English, Romaji, or Japanese across the entire app. | P3 | F-21 | 1. Dropdown in Settings. 2. Affects all cards, detail pages, and search results. |

## 5.9 Epic: Error States & Edge Cases

| ID | User Story | Priority | Feature | Acceptance Criteria |
|:---|:---|:---|:---|:---|
| APP-23 | As a user with no internet, I want the app to still display the last cached schedule and news, so it's useful on the subway. | P1 | — | 1. Loads from `SharedPreferences` cache. 2. Amber banner: "Offline Mode — Showing cached data." 3. Images fallback to `cached_network_image` disk cache. |
| APP-24 | As a user, I want clear error messages (not blank screens) if the data fails to load, with a "Retry" button. | P1 | — | 1. Error illustration + message: "Something went wrong." 2. "Retry" button re-fetches from R2. |
| APP-25 | As a user on a very slow connection, I want to see shimmer placeholder animations while data loads, so the app doesn't feel broken. | P1 | — | 1. Skeleton shimmer placeholders for cards and images during loading state. |
