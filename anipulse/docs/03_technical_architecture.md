# 3. Technical Architecture & Data Flow

> **Cross-References:** Data scraping pipeline → [10 — Scraping](./10_data_aggregation_and_scraping.md) · Business rules & state machine → [08 — RBAC](./08_business_rules_and_rbac.md) · CRON jobs → [09 — Notifications](./09_notifications_and_cron.md).

## 3.1 Architecture Overview

AniPulse uses a **"Hybrid Edge" architecture**: data is managed in a cloud database (Supabase), but the heavy read load (100,000+ Flutter users) is served entirely from static JSON files on a zero-egress-fee CDN (Cloudflare R2). This eliminates traditional server costs while maintaining full admin control.

### 3.1.1 High-Level System Diagram

```mermaid
graph TD
    subgraph "1. Data Ingestion Layer"
        EXT["Chrome Extension<br/>(Admin's Browser)"] -->|Extracts DOM from<br/>Anikoto / MAL / News Sites| ADMIN["Admin Dashboard<br/>(Next.js on localhost or Vercel)"]
    end

    subgraph "2. Data Management Layer"
        ADMIN -->|Review Queue → Approve| DB[(Supabase PostgreSQL)]
        ADMIN -->|Upload Cover Art| R2_ASSETS["R2: /assets/ bucket<br/>(WebP images)"]
    end

    subgraph "3. CDN Delivery Layer (Cloudflare)"
        DB -->|Webhook on INSERT/UPDATE| WORKER["Cloudflare Worker<br/>(JSON Generator)"]
        WORKER -->|Generates & Uploads| R2_JSON["R2: /api/ bucket"]
        R2_JSON --> SCHED["schedule.json"]
        R2_JSON --> NEWS["news.json"]
        R2_JSON --> META["anime_catalog.json"]
    end

    subgraph "4. Client Layer (Flutter App)"
        APP["Flutter App<br/>(iOS + Android)"] -->|HTTP GET on launch| SCHED
        APP -->|HTTP GET on launch| NEWS
        APP -->|HTTP GET images| R2_ASSETS
        APP -->|Cache locally| SQFLITE["SQFlite<br/>(Offline Cache)"]
    end

    subgraph "5. Phase 2: User Layer"
        APP -.->|Supabase Auth<br/>(Google/Apple OAuth)| DB
        DB -.->|Edge Function Trigger| FCM["Firebase Cloud Messaging"]
        FCM -.->|Push Notification| APP
    end
```

### 3.1.2 Technology Stack Summary

| Layer | Technology | Why This Choice | Cost |
|:---|:---|:---|:---|
| **Mobile App** | Flutter (Dart) | Single codebase for iOS + Android. 120fps rendering. Hot reload for fast dev. | Free |
| **State Management** | Riverpod | Compile-safe, testable, scales better than Provider for complex state. | Free |
| **Local Database** | SQFlite | Mature SQLite wrapper for Flutter. Stores watchlist + cached JSON offline. | Free |
| **Backend Database** | Supabase (PostgreSQL) | Free tier: 500MB storage, 2GB bandwidth, 50K monthly active users. Row-Level Security. Auth built-in. | Free (Free Tier) |
| **CDN / Static Files** | Cloudflare R2 | **$0 egress fees.** $0.015/GB storage. 10M Class B reads free/month. The killer feature. | ~$0/mo |
| **JSON Builder** | Cloudflare Workers | Serverless. Triggered by Supabase Webhooks. 100K free requests/day. | Free |
| **Push Notifications** | Firebase Cloud Messaging (FCM) | Unlimited free pushes. Topic-based fan-out eliminates per-device targeting. | Free |
| **Admin Dashboard** | Next.js (React) on Vercel | Free hosting. Serverless API routes. Connects directly to Supabase. | Free (Hobby Tier) |
| **Image Processing** | Sharp (Node.js) or browser-side | Converts uploaded images to WebP before R2 upload. Reduces bandwidth 60-80%. | Free |
| **Subscriptions** | RevenueCat | Manages Apple/Google in-app purchases. Free under 2,500 MAU revenue. | Free (Starter) |
| **Analytics** | Firebase Analytics + Crashlytics | Free crash reporting + user behavior analytics. | Free |

---

## 3.2 The Justification: Why "Hybrid Edge"?

### 3.2.1 Why Supabase instead of Local MongoDB?
| Factor | Local MongoDB | Supabase (Cloud Postgres) |
|:---|:---|:---|
| **Accessibility** | Locked to admin's machine | Accessible from any device globally |
| **Collaboration** | Single user only | Multiple editors via RBAC |
| **Auth** | Must build from scratch | Built-in (Google, Apple, Email) |
| **Webhooks** | Must build custom trigger system | Native database webhooks on INSERT/UPDATE |
| **Cost** | Free (but requires always-on machine) | Free (500MB, 50K MAU) |
| **Verdict** | ❌ Not viable for a growing project | ✅ **Recommended** |

### 3.2.2 Why Cloudflare R2 instead of direct Supabase reads?
| Scenario | Supabase Direct | Cloudflare R2 |
|:---|:---|:---|
| 100K users fetch schedule simultaneously | 100K database reads. Free tier exhausted in minutes. $0.09/100K reads after. | 100K reads of a cached static file. **$0 egress. Free.** |
| Latency (global) | 200-400ms (single region DB) | **10-50ms** (edge-cached globally at 300+ PoPs) |
| Downtime risk | DB overload → 500 errors | Static file → **Effectively unhittable** |

---

## 3.3 Data Models (Supabase PostgreSQL)

### Table: `anime_series`
The master record for each anime show.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `UUID` | `PRIMARY KEY`, `DEFAULT gen_random_uuid()` | Unique identifier |
| `title_en` | `TEXT` | `NOT NULL` | English title |
| `title_jp` | `TEXT` | `NULLABLE` | Japanese title (kanji/romaji) |
| `synopsis` | `TEXT` | `NULLABLE` | 2-3 sentence plot summary |
| `cover_image_url` | `TEXT` | `NOT NULL` | URL to WebP image on R2 `/assets/` |
| `banner_image_url` | `TEXT` | `NULLABLE` | Wide banner for detail page hero |
| `studio` | `TEXT` | `NOT NULL` | Animation studio name (e.g., "MAPPA") |
| `genres` | `TEXT[]` | `DEFAULT '{}'` | Array of genre tags: `{"Action","Fantasy"}` |
| `mal_id` | `INTEGER` | `UNIQUE, NULLABLE` | MyAnimeList external ID for linking |
| `anilist_id` | `INTEGER` | `UNIQUE, NULLABLE` | AniList external ID for linking |
| `total_episodes` | `INTEGER` | `NULLABLE` | Known total episode count (NULL if ongoing/unknown) |
| `status` | `TEXT` | `DEFAULT 'airing'`, `CHECK (status IN ('airing','completed','upcoming','cancelled'))` | Show-level status |
| `season` | `TEXT` | `CHECK (season IN ('winter','spring','summer','fall'))` | Airing season |
| `season_year` | `INTEGER` | | e.g., `2026` |
| `streaming_platforms` | `JSONB` | `DEFAULT '{}'` | `{"crunchyroll":"url","netflix":"url","hidive":"url"}` |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT now()` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT now()` | Last modification timestamp |

### Table: `broadcast_schedule`
Per-episode airing data.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `UUID` | `PRIMARY KEY` | Unique identifier |
| `anime_id` | `UUID` | `FOREIGN KEY → anime_series(id) ON DELETE CASCADE` | Parent anime |
| `episode_number` | `INTEGER` | `NOT NULL` | Episode number within the season |
| `air_datetime_utc` | `TIMESTAMPTZ` | `NOT NULL` | Exact UTC air time |
| `status` | `TEXT` | `DEFAULT 'upcoming'`, `CHECK (status IN ('upcoming','released','delayed','cancelled'))` | Episode status |
| `delay_reason` | `TEXT` | `NULLABLE` | Reason for delay (displayed to users) |

### Table: `news_articles`
Curated news feed entries.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `UUID` | `PRIMARY KEY` | Unique identifier |
| `headline` | `TEXT` | `NOT NULL`, `MAX 200 chars` | News headline |
| `body_summary` | `TEXT` | `NULLABLE`, `MAX 500 chars` | 2-3 sentence summary |
| `source_name` | `TEXT` | `NOT NULL` | e.g., "AnimeNewsNetwork", "Crunchyroll" |
| `source_url` | `TEXT` | `NOT NULL` | Link to original article |
| `image_url` | `TEXT` | `NULLABLE` | 16:9 cover image hosted on R2 |
| `youtube_url` | `TEXT` | `NULLABLE` | YouTube PV/Trailer embed URL |
| `category` | `TEXT` | `DEFAULT 'announcement'`, `CHECK (category IN ('announcement','trailer','renewal','event'))` | News category |
| `is_sponsored` | `BOOLEAN` | `DEFAULT false` | Flag for paid/sponsored cards |
| `published_at` | `TIMESTAMPTZ` | `NOT NULL` | Publication timestamp (supports future scheduling) |

### Table: `staging_queue` (Admin Only)
Temporary holding area for scraped data before approval.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `UUID` | `PRIMARY KEY` | Unique identifier |
| `source` | `TEXT` | `NOT NULL` | e.g., "anikoto.me", "animenewsnetwork.com" |
| `payload` | `JSONB` | `NOT NULL` | Raw scraped data from Chrome Extension |
| `status` | `TEXT` | `DEFAULT 'pending'`, `CHECK (status IN ('pending','approved','rejected'))` | Review status |
| `reviewed_by` | `UUID` | `NULLABLE, FOREIGN KEY → auth.users(id)` | Admin who reviewed |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT now()` | Ingestion timestamp |

### Table: `user_watchlists` (Phase 2)
Cloud-synced user watchlists.

| Column | Type | Constraints | Description |
|:---|:---|:---|:---|
| `id` | `UUID` | `PRIMARY KEY` | Unique identifier |
| `user_id` | `UUID` | `FOREIGN KEY → auth.users(id) ON DELETE CASCADE` | Supabase Auth user |
| `anime_id` | `UUID` | `FOREIGN KEY → anime_series(id)` | Tracked anime |
| `watch_status` | `TEXT` | `CHECK (watch_status IN ('watching','plan_to_watch','completed','dropped'))` | User's status |
| `episodes_watched` | `INTEGER` | `DEFAULT 0` | Progress tracker |

---

## 3.4 The JSON Generator (Cloudflare Worker)

### 3.4.1 Trigger Mechanism
1.  Admin approves data in the Staging Queue → writes to `anime_series` / `broadcast_schedule` / `news_articles`.
2.  Supabase **Database Webhook** fires on `INSERT`, `UPDATE`, or `DELETE` on these tables.
3.  Webhook sends a POST request to a **Cloudflare Worker** URL.
4.  The Worker queries Supabase *once*, builds optimized JSON payloads (clamped to latest 50 news + current week's schedule), and uploads to R2.
5.  R2 serves the JSON globally via Cloudflare's 300+ edge PoPs.

### 3.4.2 JSON File Structure

**`/api/schedule.json`** — The current week's schedule:
```json
{
  "generated_at": "2026-03-21T10:00:00Z",
  "week_start": "2026-03-17",
  "week_end": "2026-03-23",
  "days": {
    "monday": [
      {
        "anime_id": "uuid-here",
        "title_en": "Solo Leveling Season 2",
        "title_jp": "俺だけレベルアップな件",
        "studio": "A-1 Pictures",
        "episode_number": 14,
        "air_datetime_utc": "2026-03-17T16:00:00Z",
        "status": "released",
        "cover_image_url": "https://r2.anipulse.app/assets/solo-leveling-s2.webp",
        "streaming_platforms": {
          "crunchyroll": "https://crunchyroll.com/series/...",
          "hulu": "https://hulu.com/series/..."
        }
      }
    ],
    "tuesday": [],
    "...": "..."
  }
}
```

**`/api/news.json`** — Latest 50 news articles:
```json
{
  "generated_at": "2026-03-21T10:00:00Z",
  "articles": [
    {
      "id": "uuid-here",
      "headline": "Chainsaw Man Season 2 Confirmed for Fall 2026",
      "body_summary": "MAPPA has officially confirmed...",
      "source_name": "AnimeNewsNetwork",
      "source_url": "https://animenewsnetwork.com/...",
      "image_url": "https://r2.anipulse.app/assets/news/csm-s2-announce.webp",
      "youtube_url": "https://youtube.com/watch?v=...",
      "category": "announcement",
      "is_sponsored": false,
      "published_at": "2026-03-21T08:30:00Z"
    }
  ]
}
```

---

## 3.5 Image Management Pipeline

| Step | Action | Tool | Output |
|:---|:---|:---|:---|
| 1 | Admin uploads cover art via Admin Dashboard | Browser File Picker | Raw PNG/JPG |
| 2 | Browser-side compression (before upload) | `browser-image-compression` JS library | WebP, max 200KB, 600px wide |
| 3 | Upload to R2 `/assets/` bucket | Supabase Edge Function or direct R2 API | `https://r2.anipulse.app/assets/{slug}.webp` |
| 4 | URL saved to `anime_series.cover_image_url` | Supabase INSERT/UPDATE | Database record updated |
| 5 | Flutter app fetches and caches | `cached_network_image` package | Cached locally on device |

---

## 3.6 Flutter App: Networking & Caching Strategy

1.  **On App Launch:** Fetch `schedule.json` and `news.json` from R2 via `http.get()`.
2.  **Cache Locally:** Store the raw JSON string in `SharedPreferences` (fast key-value store).
3.  **On Subsequent Launch:** Display cached data *immediately* (0ms perceived load). Then fetch fresh JSON in the background. If new data differs, update the UI with a smooth fade animation.
4.  **Offline Mode:** If the HTTP GET fails (no internet), the app renders from cache. An amber banner: "Offline Mode — Showing cached schedule."
5.  **Image Caching:** `cached_network_image` handles all poster art with automatic disk caching and placeholder shimmer animations during load.
