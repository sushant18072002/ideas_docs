# 5. User Stories: Flutter App (End User)

> **Format:** As a [Role], I want to [Action] so that [Benefit/Outcome].
> **Priority:** Must Have (P1), Should Have (P2), Could Have (P3), Won't Have (P4).

## 5.1 Epic: Discovery & Schedule (The Core Pulse)

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| APP-01 | As a fan, I want to see a localized countdown timer for today's anime drops, so I know exactly when to open Crunchyroll. | P1 | 1. Timers recalculate client-side. 2. Timezones adjust automatically via device locale. 3. Cards shift from "Upcoming" to "Aired" instantly upon expiration. |
| APP-02 | As a user, I want to swipe horizontally between Mon-Sun, so I can see what dropped yesterday or what drops tomorrow. | P1 | 1. Swiping changes the active day. 2. The active day underlines in the top TabBar. |
| APP-03 | As a binger, I want to view a "Seasonal Overview" grid, so I can see every single show airing in the current 3-month block (Cour). | P1 | 1. Grid displays high-res 2:3 ratio posters. 2. Tap to view details. |
| APP-04 | As a user, I want to search for an anime by its English or Romaji title, so I don't have to guess the translation used. | P2 | 1. Search bar queries both `title_en` and `title_jp` fields. 2. Results show as-you-type (debounce 300ms). |

## 5.2 Epic: The News Feed

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| APP-05 | As an engaged fan, I want to see a vertical feed of official PVs and studio announcements, so I don't have to scour Reddit/Twitter. | P1 | 1. Infinite scroll feed. 2. Headlines bolded, source linked. |
| APP-06 | As a viewer, I want to play a YouTube PV directly in the news card, so I don't have to leave the app. | P2 | 1. YouTube iframe embeds in the Flutter card. 2. Auto-pauses if scrolled out of view. |
| APP-07 | As a user, I want to share a news article to my friends via native iOS/Android share sheets. | P2 | 1. Triggers native share UI. 2. Sends a deep link or formatted text. |

## 5.3 Epic: Anime Details & "Where to Watch"

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| APP-08 | As a user, I want to see the studio, genres, and synopsis of a show when I tap on it, so I can decide if it's worth my time. | P1 | 1. Bottom Sheet slides up. 2. Displays Mal Score, Studio, 3-line synopsis with "Read More" expansion. |
| APP-09 | As a subscriber, I want to see which exact streaming platform holds the license (Netflix, CR, HIDIVE), so I know where to go. | P1 | 1. Displays logos of licensed platforms. 2. Tapping the logo opens the respective app via deep link. |
| APP-10 | As an organized watcher, I want to tap a "+" button to add a show to "My Watchlist", so I can track my personal schedule. | P2 | 1. Button toggles to a checked state. 2. Saved locally (MVP) or to Cloud (Phase 2). |

## 5.4 Epic: Push Notifications

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| APP-11 | As a tracker, I want a push notification the exact minute an episode I follow drops, so I can watch it before spoilers hit Twitter. | P1 | 1. FCM receives payload. 2. Device wakes and shows alert: "Jujutsu Kaisen Ep 14 is now live!". |
| APP-12 | As a casual user, I want to turn off global notifications but keep them on for specific shows, so my lock screen isn't spammed. | P2 | 1. Toggle in settings for "All Shows". 2. Individual bell icons on Anime Detail pages. |
| APP-13 | As a user, I want a weekly "Anime Sunday Recap" push, so I can see what I missed over the weekend. | P3 | 1. Weekly batch push outlining the top 3 highest-rated episodes that dropped that week. |

## 5.5 Epic: Authentication & Pro Tier (Phase 2)

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| APP-14 | As a user who relies on the app, I want to sign in with Google/Apple, so my watchlist is safeguarded if I buy a new phone. | P2 | 1. OAuth implementation via Supabase Auth. 2. On login, merges local SQFlite data to Cloud. |
| APP-15 | As a Pro User, I want to change the app's accent color/theme, so it matches my favorite character (e.g., Orange for Naruto, Purple for Frieren). | P3 | 1. Settings page unlocks theme pallet. 2. Changing theme instantly updates Provider state app-wide. |
| APP-16 | As a Pro User, I want all native AdMob units to disappear forever, so I have a clean unbroken UI. | P2 | 1. Validates active RevenueCat subscription. 2. Strips all `AdMobWidget` injections from the lists. |
| APP-17 | As a user, I want a single "Delete My Account" button in Settings, so I can instantly purge all my PII and watchlists in compliance with GDPR. | P1 | 1. Calls Supabase Edge function. 2. Hard deletes auth record and cascades to watchlist. |
