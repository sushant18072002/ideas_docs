# 6. User Stories: Admin Dashboard

> **Format:** As an [Admin Role], I want to [Action] so that [Benefit/Outcome].
> **Context:** The Admin Dashboard is a Next.js web application running on `localhost:3000` during development or deployed to Vercel for remote access. It connects directly to Supabase PostgreSQL and manages all data that ultimately reaches the Flutter app via Cloudflare R2 JSON files.

---

## 6.1 Epic: Authentication & Security

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-01 | As a staff member, I want to log in with email/password protected by Supabase Auth, so only authorized admins can modify the global schedule. | P1 | 1. JWT session via Supabase. 2. Row-Level Security (RLS) enforces `role = 'admin' OR role = 'editor'` check. 3. Session expires after 24h of inactivity. |
| ADM-02 | As a SuperAdmin, I want to invite new Content Editors by email, so I can delegate news curation without sharing my credentials. | P2 | 1. Invite form sends Supabase Auth magic link. 2. New user auto-assigned `editor` role. |

## 6.2 Epic: Dashboard Overview

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-03 | As an Admin, I want to see a dashboard on login showing: Total Shows, Today's Drops, Pending Queue Items, and Last R2 Sync Time, so I know my immediate tasks. | P1 | 1. 4 KPI cards at top. 2. "Pending Queue" card pulses red if items > 0. 3. "Last Sync" shows relative time ("12 minutes ago"). |

## 6.3 Epic: Data Ingestion & Staging Queue

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-04 | As an Admin, I want to receive scraped data payloads from the Chrome Extension into a "Pending Review" staging queue, so I can verify accuracy before publishing. | P1 | 1. `/api/ingest` POST endpoint accepts JSON payloads. 2. Each item written to `staging_queue` table with `status = 'pending'`. 3. Dashboard badge count updates in real-time. |
| ADM-05 | As an Admin, I want to see a visual diff comparing scraped data vs. existing database records (old time struck through in red, new time in green), so I can spot changes instantly. | P1 | 1. Side-by-side or inline diff rendering. 2. "NEW" badge for items not yet in DB. 3. "UPDATE" badge for items with changed fields. |
| ADM-06 | As an Admin, I want to click "Approve" on a staged item to write it to the production database, "Edit" to modify it first, or "Reject" to discard it, so I have full control over data quality. | P1 | 1. Approve → INSERT/UPDATE to `anime_series` / `broadcast_schedule`. 2. Edit → Opens pre-filled form. 3. Reject → Soft-delete (keeps audit trail). |
| ADM-07 | As an Admin, I want batch approve/reject for the staging queue, so I can process 50+ items from a seasonal scrape in under 2 minutes. | P2 | 1. "Select All" checkbox. 2. "Approve Selected" / "Reject Selected" bulk actions. |

## 6.4 Epic: Anime Series Management

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-08 | As an Admin, I want to manually create a new anime entry by filling a form (Title EN, Title JP, Synopsis, Studio, Genres, Season, Streaming URLs), for shows not captured by the scraper. | P1 | 1. Form with field validation. 2. Genre multi-select chips. 3. Streaming platform checkboxes with URL inputs. |
| ADM-09 | As an Admin, I want to edit any existing anime record, so I can fix typos, update streaming URLs when a show moves platforms, or add a synopsis. | P1 | 1. Searchable anime list page. 2. Click to edit. 3. "Save" button with confirmation toast. |
| ADM-10 | As an Admin, I want to upload cover art from my PC, have it auto-compressed to WebP, and stored on R2, so images are always fast and self-hosted. | P1 | 1. Drag-and-drop file input. 2. Client-side WebP conversion before upload. 3. URL auto-populated into `cover_image_url` field. |
| ADM-11 | As an Admin, I want to delete an anime and cascade-delete all its episodes, so stale or incorrect entries don't pollute the app. | P2 | 1. Confirmation dialog: "This will delete X episodes." 2. `ON DELETE CASCADE` handles DB cleanup. |

## 6.5 Epic: Schedule & Episode Management

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-12 | As an Admin, I want to set the air day, time, and timezone (e.g., Saturday 23:00 JST) for a show's weekly episode, so the system computes accurate UTC timestamps. | P1 | 1. Day-of-week dropdown. 2. Time picker (24h format). 3. Timezone selector (JST, KST, PST, EST, UTC). 4. Auto-calculates `air_datetime_utc`. |
| ADM-13 | As an Admin, I want to bulk-generate 12 episodes for a 1-cour show with one click, so I don't have to create 12 rows manually. | P2 | 1. Input: first episode air date + total episode count. 2. System generates remaining episodes at 7-day intervals. 3. All rows saved in a single transaction. |
| ADM-14 | As an Admin, I want to mark an episode as "Delayed" with an optional reason (e.g., "Production delay"), so the app shows a red tag instead of a stale countdown. | P2 | 1. Status dropdown: `upcoming`, `released`, `delayed`, `cancelled`. 2. "Reason" text field appears when `delayed` is selected. 3. Triggers CDN cache invalidation. |
| ADM-15 | As an Admin, I want an Airtable-style data grid for the schedule, so I can rapidly scan and edit hundreds of episode rows at once. | P2 | 1. Sortable, filterable grid (TanStack Table or AG Grid). 2. Inline cell editing. 3. "Save All Changes" button for batch update. |

## 6.6 Epic: News Feed Curation

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-16 | As a Content Editor, I want to write a news article by filling: Headline, Summary, Source URL, Cover Image, YouTube PV URL, and Category. | P1 | 1. Simple form (not WYSIWYG). 2. YouTube URL auto-extracts thumbnail preview. 3. Category dropdown: Announcement, Trailer, Renewal, Event. |
| ADM-17 | As a Content Editor, I want to schedule a news post for future publication (e.g., embargo lifts at 9am JST), so I can prepare content in advance. | P3 | 1. Date/time picker for `published_at`. 2. If future, the article is excluded from `news.json` generation until the timestamp passes. |
| ADM-18 | As a SuperAdmin, I want to mark a news card as "Sponsored", with a custom CTA link, so I can fulfill direct ad deals. | P2 | 1. "Is Sponsored?" toggle. 2. Extra fields: CTA text, CTA URL. 3. Sponsored cards always appear at position 3 in the feed. |

## 6.7 Epic: CDN & System Operations

| ID | User Story | Priority | Acceptance Criteria |
|:---|:---|:---|:---|
| ADM-19 | As a SuperAdmin, I want a "Force Sync to R2" button on the dashboard, so I can manually regenerate the JSON files if the automated webhook fails. | P1 | 1. Button triggers Cloudflare Worker. 2. Shows status: "Syncing…" → "✅ Synced at 10:42 AM." 3. Logs the event. |
| ADM-20 | As a SuperAdmin, I want a sync log showing the last 20 JSON generation events (timestamp, rows affected, success/error), so I can debug data issues. | P3 | 1. Table sorted newest first. 2. Error rows highlighted in red with error message. |
| ADM-21 | As a SuperAdmin, I want a "Preview JSON" button that shows me the exact JSON that will be uploaded to R2, so I can verify the payload before it goes live. | P2 | 1. Modal with syntax-highlighted JSON. 2. "Copy to Clipboard" button. |
