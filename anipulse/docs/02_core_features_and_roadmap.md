# 2. Core Features & Roadmap

## 2.1 Epic: The Global Feed ("The Pulse")
The core landing screen of the application. It acts as an aggregate timeline of everything happening in the anime world today.

*   **F-01: Today's Schedule Carousel:** A horizontally scrolling list of anime dropping *today*, sorted chronologically. Shows countdown timers (e.g., "Airs in 2h 15m").
*   **F-02: Breaking News Feed:** Infinite vertical scroll of news cards. Cards support embedded YouTube iframe players (for PVs/Trailers), key visual images, and text snippets.
*   **F-03: Quick Add Button:** A prominent '+' button on every schedule card allowing users to quickly add the show to their local watchlist.

## 2.2 Epic: The Comprehensive Calendar
*   **F-04: Weekly Grid View:** Standard Mon-Sun layout showing episodes dropping on each day.
*   **F-05: Seasonal View:** A macro view showing all shows airing in the current "Cour" (e.g., Spring 2026), clustered by popularity or genre.
*   **F-06: Timezone Localization:** All times fetched from the JSON are strictly UTC. The Flutter app translates these perfectly to the user's localized device time.

## 2.3 Epic: Anime Details Page
*   **F-07: Unified Detail View:** Tapping an anime opens a bottom modal sheet (iOS style) showing the synopsis, genres, MAL score overlay, and the Studio.
*   **F-08: 'Where to Watch' Deep Links:** Actionable buttons taking the user directly to Crunchyroll, Netflix, Hulu, or HIDIVE's app via deep linking.

## 2.4 Epic: User Watchlist & Profiles
*   **F-09: Local-First Watchlist:** Users can track "Watching", "Completed", and "Dropped". By default, this uses `SQFlite` (local device database) so no login is required.
*   **F-10: Cloud Sync (Pro/Auth Feature):** If a user signs in via Supabase (Google/Apple Auth), their `SQFlite` data syncs to the cloud `watchlists` table.

## 2.5 Phase Rollout Roadmap

### Phase 1: MVP (The Static Edge)
*   **Goal:** Prove the UI/UX and launch the app with zero server costs.
*   **Features:** F-01 through F-08.
*   **Architecture:** Admin enters data in local CMS -> Uploads highly optimized `schedule.json`, `news.json` to Cloudflare R2. Flutter app just does a rapid HTTP GET. No user accounts. 

### Phase 2: Engagement (The Cloud Era)
*   **Goal:** Increase Day 7 retention through personalization.
*   **Features:** F-09, F-10, Push Notifications.
*   **Architecture:** Introduce Supabase Auth. When an episode in the database hits its release time, a Supabase Edge Function triggers Firebase Cloud Messaging (FCM) to send a push to all users tracking that ID.

### Phase 3: Community & Social (The "Social" Vision)
*   **Goal:** Build a moat against competitors by making it a community hub.
*   **Features:** Episode discussion threads, user ratings, sharing "My Schedule" cards to Instagram Stories.
