# 9. Notifications, CRON Jobs & Background Systems

> **Cross-References:** FCM feature → [02 — Features](./02_core_features_and_roadmap.md#27-epic-push-notifications) · User stories → [05 — App Stories](./05_user_stories_app.md#57-epic-push-notifications) · Scraping pipeline → [10 — Scraping](./10_data_aggregation_and_scraping.md).

---

## 9.1 Data Ingestion Strategy (Not Automated CRON)

We explicitly **do not** use automated CRON scrapers for data ingestion. This is a deliberate architectural decision to avoid:
*   IP bans and CAPTCHA blocks from anime sites (especially Cloudflare-protected ones like Anikoto.me).
*   Brittle scraper code breaking every time a site updates its HTML.
*   Legal gray areas around automated scraping.

### The Manual Pipeline
Data is ingested via a **Chrome Extension** operated by the Admin. See [10 — Data Aggregation](./10_data_aggregation_and_scraping.md) for full technical details.

| Step | Actor | Action | Frequency |
|:---|:---|:---|:---|
| 1 | Admin | Navigates to `anikoto.me/home` in Chrome | Once per season (quarterly) for new shows; weekly for updates |
| 2 | Admin | Clicks Chrome Extension → "Extract Schedule" | Per session |
| 3 | Extension | Parses DOM → POSTs JSON to `localhost:3000/api/ingest` | Instant |
| 4 | Admin | Reviews Staging Queue → Approves/Edits/Rejects | 2-5 minutes |
| 5 | System | Supabase Webhook → Cloudflare Worker → R2 JSON rebuild | Automatic on approval |

---

## 9.2 The JSON Edge Sync (Automated CRON)

This is the **only** automated job. It regenerates the static JSON files that the Flutter app consumes.

### 9.2.1 Primary Trigger: Event-Driven (Webhook)
When any record in `anime_series`, `broadcast_schedule`, or `news_articles` is `INSERT`ed, `UPDATE`d, or `DELETE`d:
1.  Supabase Database Webhook fires a POST request to the Cloudflare Worker URL.
2.  The Worker queries all relevant tables from Supabase.
3.  Builds `schedule.json` (current week), `news.json` (latest 50), and `anime_catalog.json` (full catalog metadata).
4.  Validates each JSON against a schema. If valid → uploads to R2. If invalid → aborts and alerts SuperAdmin.

### 9.2.2 Fallback Trigger: Hourly CRON
A Cloudflare Worker CRON trigger runs every 60 minutes as a safety net, in case a Webhook is dropped or fails silently.

```toml
# wrangler.toml (Cloudflare Worker config)
[triggers]
crons = ["0 * * * *"]  # Every hour, on the hour
```

### 9.2.3 The Worker Code (TypeScript)
```typescript
// Cloudflare Worker: json-generator.ts
import { createClient } from '@supabase/supabase-js';
import Ajv from 'ajv';
import scheduleSchema from './schemas/schedule.schema.json';

interface Env {
    SUPABASE_URL: string;
    SUPABASE_KEY: string;
    R2_BUCKET: R2Bucket;
    DISCORD_WEBHOOK_URL: string;
}

export default {
    // Webhook handler (event-driven)
    async fetch(request: Request, env: Env): Promise<Response> {
        await generateAndUpload(env);
        return new Response('OK', { status: 200 });
    },

    // CRON handler (hourly fallback)
    async scheduled(event: ScheduledEvent, env: Env): Promise<void> {
        await generateAndUpload(env);
    },
};

async function generateAndUpload(env: Env) {
    const supabase = createClient(env.SUPABASE_URL, env.SUPABASE_KEY);

    // --- Generate schedule.json ---
    const weekStart = getWeekStart(); // Helper: Monday of current week
    const weekEnd = getWeekEnd();     // Helper: Sunday of current week

    const { data: schedule } = await supabase
        .from('broadcast_schedule')
        .select(`
            id, episode_number, air_datetime_utc, status, delay_reason,
            anime_series!inner(
                id, title_en, title_jp, studio, cover_image_url,
                genres, streaming_platforms
            )
        `)
        .gte('air_datetime_utc', weekStart)
        .lte('air_datetime_utc', weekEnd)
        .order('air_datetime_utc', { ascending: true });

    // Group episodes by day-of-week (matches Doc 03 JSON shape)
    const dayNames = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday'];
    const days: Record<string, any[]> = {
        monday: [], tuesday: [], wednesday: [], thursday: [],
        friday: [], saturday: [], sunday: [],
    };
    for (const ep of (schedule || [])) {
        const dayIndex = new Date(ep.air_datetime_utc).getUTCDay();
        const dayName = dayNames[dayIndex];
        days[dayName].push({
            anime_id: ep.anime_series.id,
            title_en: ep.anime_series.title_en,
            title_jp: ep.anime_series.title_jp,
            studio: ep.anime_series.studio,
            episode_number: ep.episode_number,
            air_datetime_utc: ep.air_datetime_utc,
            status: ep.status,
            cover_image_url: ep.anime_series.cover_image_url,
            streaming_platforms: ep.anime_series.streaming_platforms,
        });
    }

    const schedulePayload = {
        generated_at: new Date().toISOString(),
        week_start: weekStart,
        week_end: weekEnd,
        days,
    };

    // --- Validate against schema ---
    const ajv = new Ajv();
    const isValid = ajv.validate(scheduleSchema, schedulePayload);

    if (!isValid) {
        await alertSuperAdmin(env, `Schedule JSON validation failed: ${ajv.errorsText()}`);
        return; // ABORT: do not upload invalid JSON
    }

    // --- Upload to R2 ---
    await env.R2_BUCKET.put('api/schedule.json', JSON.stringify(schedulePayload), {
        httpMetadata: {
            contentType: 'application/json',
            cacheControl: 'public, max-age=3600, s-maxage=3600',
        },
    });

    // --- Generate news.json (latest 50) ---
    const { data: news } = await supabase
        .from('news_articles')
        .select('*')
        .lte('published_at', new Date().toISOString()) // Exclude future-scheduled
        .order('published_at', { ascending: false })
        .limit(50);

    const newsPayload = {
        generated_at: new Date().toISOString(),
        articles: news || [],
    };

    await env.R2_BUCKET.put('api/news.json', JSON.stringify(newsPayload), {
        httpMetadata: {
            contentType: 'application/json',
            cacheControl: 'public, max-age=1800, s-maxage=1800',
        },
    });

    console.log(`✅ JSON sync complete. Schedule: ${(schedule || []).length} episodes. News: ${(news || []).length} articles.`);
}

async function alertSuperAdmin(env: Env, message: string) {
    await fetch(env.DISCORD_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            content: `🚨 **AniPulse JSON Sync Error**\n${message}`,
        }),
    });
}
```

---

## 9.3 Push Notification Architecture (FCM)

### 9.3.1 Why FCM Topics?
The Flutter app does not maintain a persistent WebSocket to any server. Push notifications are handled **entirely out-of-band** via Firebase Cloud Messaging.

Instead of maintaining a database of device tokens and sending individual pushes to 50,000 users (which costs compute and is slow), we use **FCM Topics**:

| Approach | Device Token Targeting | **Topic-Based (Our Choice)** |
|:---|:---|:---|
| Server Cost | Must store + iterate 50K tokens | **$0** (Firebase handles fan-out) |
| API Calls | 50,000 calls (or batches of 500) | **1 single API call** |
| Latency | Minutes for full delivery | **Seconds** (Apple/Google infra) |
| Scalability | Degrades linearly with user count | **Constant** regardless of user count |

### 9.3.2 The Subscription Flow
```dart
// Flutter: When user taps "+" to track an anime
Future<void> onTrackAnime(String animeId) async {
    // 1. Save to local watchlist
    await sqfliteDb.insert('watchlist', {'anime_id': animeId, 'status': 'watching'});

    // 2. Subscribe to FCM Topic for this anime
    await FirebaseMessaging.instance.subscribeToTopic('anime_$animeId');
    // Now this device receives ALL pushes for this anime's episodes
}

// Flutter: When user removes anime from watchlist
Future<void> onUntrackAnime(String animeId) async {
    await sqfliteDb.delete('watchlist', where: 'anime_id = ?', whereArgs: [animeId]);
    await FirebaseMessaging.instance.unsubscribeFromTopic('anime_$animeId');
}
```

### 9.3.3 The Push Trigger (Supabase Edge Function)
When an episode's `air_datetime_utc` arrives, a Supabase Edge Function fires and sends a single broadcast to Firebase:

```typescript
// Supabase Edge Function: send-episode-notification.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';

serve(async (req) => {
    const { anime_id, title_en, episode_number, streaming_platform } = await req.json();

    // Send ONE API call to Firebase → fans out to all subscribed devices
    const response = await fetch('https://fcm.googleapis.com/fcm/send', {
        method: 'POST',
        headers: {
            'Authorization': `key=${Deno.env.get('FCM_SERVER_KEY')}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            to: `/topics/anime_${anime_id}`,
            notification: {
                title: `${title_en} — Episode ${episode_number} is LIVE! 🔥`,
                body: `Now streaming on ${streaming_platform}. Tap to watch.`,
            },
            data: {
                anime_id: anime_id,
                deep_link: `anipulse://anime/${anime_id}`,
            },
        }),
    });

    return new Response(JSON.stringify({ sent: response.ok }), { status: 200 });
});
```

### 9.3.4 Notification Priority Rules
| User Tier | FCM Priority | Behavior |
|:---|:---|:---|
| **Free User** | `normal` | Delivered at next device wake cycle (may be delayed by Doze mode) |
| **PRO User** | `high` | Wakes device immediately. Guaranteed near-instant delivery. |

---

## 9.4 Admin Alert System (Email/Discord)

The platform does **not** send emails to end users. The app is purely push-driven. Alerts are for Admin operational awareness only.

### 9.4.1 Alert Channels
| Channel | Service | Cost | Use Case |
|:---|:---|:---|:---|
| **Discord Webhook** | Discord (free) | $0 | Primary alert channel. Instant delivery to team Discord server. |
| **Email** | Resend | Free (100 emails/day) | Fallback for critical alerts if Discord is down. |

### 9.4.2 Alert Definitions

| Alert ID | Name | Trigger | Channel | Severity |
|:---|:---|:---|:---|:---|
| ALERT-01 | **JSON Sync Failure** | Cloudflare Worker fails to upload to R2 (schema validation error, R2 API error) | Discord + Email | 🔴 Critical |
| ALERT-02 | **Staging Queue Stale** | Items in staging queue with `status = 'pending'` for > 48 hours | Discord | 🟡 Warning |
| ALERT-03 | **Traffic Spike** | R2 read requests exceed 5× the 7-day average (viral moment or DDoS) | Discord | 🟡 Warning |
| ALERT-04 | **Supabase Quota Warning** | Supabase free tier storage exceeds 80% (400MB of 500MB) | Discord + Email | 🟡 Warning |
| ALERT-05 | **SSL/Domain Expiry** | Domain or SSL certificate expires in < 14 days | Email | 🟡 Warning |
