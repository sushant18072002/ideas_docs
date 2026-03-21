# 6. User Stories: Admin Dashboard

> **Format:** As an [Admin Role], I want to [Action] so that [Benefit/Outcome].
> **Context:** The Admin uses a Next.js or React web portal connected directly to the Supabase database. They do NOT interact with the Cloudflare delivery layer directly; the system handles that bridging.

## 6.1 Epic: Authentication & Dashboard

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-01 | As a Staff Member, I want to log in securely using an Admin Email/Password, so unauthorized users cannot alter the global schedule. | P1 | 1. JWT auth via Supabase. 2. Fails if user role is not `admin` or `editor`. |
| ADM-02 | As an Admin, I want to see a High-Level Dashboard on login (Total Anime, Upcoming Drops Today, Scraper Errors), so I know my immediate tasks. | P2 | 1. Displays 3 key metric cards. 2. Highlights any CRON scraper errors in red. |

## 6.2 Epic: Anime Series Management (The Catalog)

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-03 | As a Data Entry Clerk, I want to see a "Pending Review" queue of data payloads sent from my Chrome Extension, so I can visually verify scraped HTML data before it goes live. | P1 | 1. Receives POST payloads from extension. 2. Displays visual diffs (Old vs New time). |
| ADM-04 | As an Admin, I want to manually override any auto-filled data (e.g., fixing a typo in a synopsis), so quality remains perfectly curated. | P1 | 1. Form fields are editable before hitting "Save to Database". |
| ADM-05 | As an Admin, I want to upload high-res cover art directly from my PC, so I am not reliant on external image URLs breaking. | P1 | 1. File picker widget. 2. Auto-compresses to WebP. 3. Uploads to Cloudflare R2 Assets bucket, saves URL to Supabase. |

## 6.3 Epic: Schedule & Episode Management

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-06 | As an Admin, I want to define the global timezone for a specific show's drop, so the system accurately computes the UTC timestamp for the mobile app. | P1 | 1. Input fields for: Day of Week, Time, Timezone (e.g., JST). 2. System calculates standard Unix Timestamp. |
| ADM-07 | As an Admin, I want to mark an episode as "Delayed", so the mobile app displays a red "Delayed" tag instead of a broken countdown timer. | P2 | 1. Status dropdown on the episode record (`airing`, `delayed`, `cancelled`). 2. Forces a CDN cache invalidation. |
| ADM-08 | As an Admin, I want to bulk-create 12 episodes for a 1-cour anime with a single click (assuming weekly intervals), to save mass data entry time. | P2 | 1. Input 1st episode date. 2. System generates rows for Ep 2-12 automatically spaced by exactly 7 days. |

## 6.4 Epic: News Feed Curation

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-09 | As a Content Editor, I want to write a news headline, paste a YouTube Trailer URL, and hit Publish, so users instantly see breaking news. | P1 | 1. WYSIWYG or simple text form. 2. Extracts YouTube Thumbnail automatically. |
| ADM-10 | As an Editor, I want to schedule a news post for the future (e.g., Embargo lifts at 9am JST), so I don't have to be awake to hit publish. | P3 | 1. Date/Time picker for `published_at`. 2. System filters it out of the JSON generation until the time passes. |

## 6.5 Epic: CDN & System Triggers

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-11 | As a SuperAdmin, I want a big red "Force JSON Sync" button on the dashboard, in case the automated webhook fails and the Cloudflare JSON is out of sync. | P1 | 1. Button manually fires Edge Function. 2. Shows green toast "R2 Cache Rebuilt successfully." |
| ADM-12 | As a SuperAdmin, I want to view a log of the last 10 automated scrapes/syncs, so I can debug why users are complaining about missing shows. | P3 | 1. Table showing timestamp of sync, rows affected, and Success/Error status. |

## 6.6 Epic: Ads & Revenue Management

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-13 | As a SuperAdmin, I want to inject a Native "Sponsored Card" into the news feed globally via the dashboard, so I can fulfill direct ad-buys (e.g., a VPN company pays us directly). | P2 | 1. Toggle switch "Is Sponsored?". 2. Allows custom CTA link. |
