# 8. Business Rules & Role-Based Access Control (RBAC)

This document defines the strict logic the system must follow, preventing bad data from reaching the end users and managing who can do what.

## 8.1 Role-Based Access Control (RBAC) Matrix

| User Role | Dashboard Access | Edit App Data | Push Notifications | User Accounts Mgt | Subscription Access |
|:---|:---|:---|:---|:---|:---|
| **SuperAdmin** | Full | Full | Send Global | Full | Free |
| **Content Editor** | Limited (News/Anime) | News, Schedules | Cannot Send | No Access | Free |
| **App User (Free)** | Mobile App Only | Local Watchlist | Receive Only | Own Profile | Ads Active |
| **App User (PRO)** | Mobile App Only | Cloud Watchlist | Priority Receive | Own Profile | Ad-Free |

## 8.2 The "Episode Status" State Machine

An episode must transition through these strict states to ensure the UI renders correctly:

1.  **Status: `UPCOMING`** (Default upon creation)
    *   Rule: `air_datetime_utc` is in the future.
    *   App UI: Displays countdown timer text in Primary Brand Color (e.g., Electric Blue `#00E5FF`).
2.  **Status: `RELEASED`**
    *   Rule: `air_datetime_utc` matches current time OR admin manually forces state.
    *   App UI: Countdown disappears. "Watch Now" button solidifies to Success Green (`#00C853`).
3.  **Status: `DELAYED`**
    *   Rule: Manual override by Admin.
    *   App UI: Replaces timer with a Red (`#FF1744`) "DELAYED" tag. Pushes notification to subscribed users advising of the delay.
4.  **Status: `CANCELLED`**
    *   Rule: Manual override. (Rare, usually only for sudden tragic events).
    *   App UI: Card opacity drops to `0.4`. Greyed out (`#9E9E9E`), moved to bottom of list.

## 8.3 Data Validation Rules (Supabase Restrictions)

To prevent the CDN JSON from breaking the Flutter app's parsing engine:
*   **BR-01 (Null Safety):** `title_en` and `air_datetime_utc` cannot be NULL at the database level.
*   **BR-02 (Time Zones):** All times ingested by the Admin Panel MUST be cast to `UTC` before being saved to PostgreSQL. The Flutter app assumes everything arriving in the JSON is UTC.
*   **BR-03 (JSON Schema):** The Cloudflare Worker that generates `schedule.json` validates the payload against a strict strict JSON schema before pushing to R2. If validation fails, it aborts the upload and alerts the SuperAdmin (via Discord/Slack webhook), ensuring the app never downloads a malformed JSON file.

## 8.4 Free/Pro User Rules
*   **BR-04 (Watchlist Limit):** Free users can track an infinite amount of shows locally (SQFlite). If they create a free account to sync to the cloud, the free tier limits them to syncing 50 shows to save on database storage costs.
*   **BR-05 (Ad Delivery):** The Flutter app checks RevenueCat (or Google/Apple native receipts) on App Start. If an active PRO subscription receipt is found, the `AdsManager` class is never initialized, saving memory and battery.
