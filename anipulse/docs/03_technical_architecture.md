# 3. Technical Architecture & Data Flow

> **Context:** The original idea proposed a fully local Admin (MongoDB) generating JSON files to Cloudflare R2. While cost-effective, this limits collaboration and automation. We are advancing this to the **Hybrid Edge Architecture**.

## 3.1 High-Level System Diagram

```mermaid
graph TD
    subgraph Data Layer
        A[Anime Sites: Anikoto, MAL] -->|Chrome Extension Extraction| C[Admin Web Portal: Review Queue]
        C -->|Manual Approval| B(Supabase PostgreSQL)
    end

    subgraph The Edge Proxy (Cloudflare R2)
        B -->|Edge Trigger| D{Cloudflare R2 Storage}
        D --> E[schedule.json]
        D --> F[news.json]
        D --> G[anime_metadata.json]
    end

    subgraph Client Layer (Flutter App)
        H[Mobile User] -->|HTTP GET on App Open| E
        H -->|HTTP GET on App Open| F
    end
    
    subgraph Phase 2: User Layer
        H -.->|Auth & Watchlist Sync| B
        B -.->|Triggers| I[Firebase FCM Notifications]
        I -.->|Push Alert| H
    end
```

## 3.2 The Justification for "Hybrid Edge"
1.  **Why Supabase instead of Local Mongo?** A local database locks the project to one computer. Supabase is a globally available Postgres database with a generous free tier. A React/Next.js Admin panel can be hosted on Vercel for free, allowing anyone with the password to curate news from their phone or laptop.
2.  **Why Cloudflare R2?** Egress fees from AWS S3 or Supabase Storage would bankrupt the project if it goes viral. R2 has zero egress fees. The Flutter app fetching a 50KB JSON file 1,000,000 times a day costs nothing on R2.

## 3.3 Data Models (Supabase PostgreSQL)

### Table: `anime_series`
The master record for an anime.
*   `id` (UUID, Primary Key)
*   `title_en` (String)
*   `title_jp` (String)
*   `synopsis` (Text)
*   `cover_image_url` (String - hosted on R2)
*   `studio` (String)
*   `mal_id` (Int - for external linking)

### Table: `broadcast_schedule`
The exact dates and times for episodes.
*   `id` (UUID)
*   `anime_id` (Foreign Key -> anime_series)
*   `episode_number` (Int)
*   `air_datetime_utc` (TimestampZ)
*   `streaming_urls` (JSONB - e.g., `{"crunchyroll": "url", "netflix": "url"}`)

### Table: `news_feed`
The curated pulse of news.
*   `id` (UUID)
*   `headline` (String)
*   `source_url` (String)
*   `image_url` (String)
*   `published_at` (TimestampZ)

## 3.4 The JSON Generator (The Secret Sauce)
Instead of the Flutter app querying Supabase directly (which would consume thousands of database reads per second), a database trigger handles it.

**The Workflow:**
1.  Admin adds a new news article in Supabase.
2.  Supabase Postgres Trigger fires a Webhook.
3.  The Webhook tells a Cloudflare Worker: *"Regenerate the news.json file!"*
4.  The Worker queries Supabase *once*, builds a perfectly structured JSON array (clamped to the **latest 50 items** to keep the payload strictly under ~100KB for rapid mobile parsing), and drops it into the R2 bucket.
5.  All 100,000 Flutter users just read the `news.json` file from the CDN. Total cost: ~0. Database reads: 1.

## 3.5 Managing Images
Never serve raw images from external APIs. They break, change, or block hotlinking. 
*   **Process:** When the Admin adds an anime, a background script downloads the cover image, compresses it to WebP format (saving massive bandwidth), and uploads it to an `assets` bucket on Cloudflare R2. The Flutter app uses `cached_network_image` to pull these edge-optimized WebP files.
