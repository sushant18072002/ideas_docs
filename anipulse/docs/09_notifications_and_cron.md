# 9. Notifications, CRON Jobs & Scrapers

To maintain a massive schedule without 50 human data entry clerks, the system relies on automated scraping, CRON jobs, and event-driven notifications.

## 9.1 Background Scrapers (CRON Jobs)

The backend relies on event-driven notifications. We explicitly *avoid* automated CRON scrapers for data ingestion to prevent IP bans and CAPTCHA blocks from external sites.

### Data Ingestion: The Chrome Extension & Staging Queue
*   **Method:** Manual execution via a custom Chrome Extension.
*   **Action:** The Admin navigates to `https://anikoto.me/home` or a news site, runs the extension, and the script extracts the HTML DOM elements (Cover URLs, Titles, Air Times).
*   **Rule:** The extension sends a JSON payload to the Admin Dashboard's `/api/ingest` endpoint. This data enters a "Staging Queue". It is NEVER written directly to the `schedule` table until a human admin clicks "Approve & Sync".

### Job 2: The "JSON Edge Sync" Cache Builder
*   **Frequency:** Event-Driven (On PostgreSQL `UPDATE` trigger) OR Fallback Every 1 Hour.
*   **Action:** Queries the current week's schedule from Supabase. Structures a minified JSON object. Uploads to Cloudflare R2 bucket.
*   **Code Flow:**
    ```typescript
    // Pseudo-code for Cloudflare Worker Trigger
    const data = await supabase.from('schedule').select('*').eq('week', current);
    const minified = JSON.stringify(data);
    await env.R2_BUCKET.put('schedule.json', minified, {
      httpMetadata: { contentType: 'application/json', cacheControl: 'public, max-age=3600' }
    });
    ```

## 9.2 Push Notification Architecture (FCM)

Because the app relies heavily on Cloudflare R2 (Static Edge), the Flutter app does not maintain a constant WebSocket connection to a server. Push Notifications must be handled out-of-band using Firebase Cloud Messaging (FCM).

### The "Topic" Subscription Strategy
Instead of sending 50,000 individual Push payloads to 50,000 distinct device IDs (which is slow and expensive to process):
1.  When a user taps "+" to track an anime (e.g., ID: `anime_123`), the Flutter app tells Firebase: `FirebaseMessaging.instance.subscribeToTopic('anime_123');`
2.  **The Trigger:** When the system clock hits an episode's Release Time, an Edge Function fires.
3.  **The Broadcast:** The Edge Function sends ONE single API call to Firebase: *"Broadcast 'Episode 5 is Live!' to Topic: `anime_123`."*
4.  **Result:** Apple (APNs) and Google (FCM) handle instantly fan-out the notification to the 50,000 devices. 

*(This costs us $0 in server compute because Firebase handles the fan-out routing).*

## 9.3 Email Triggers (Admin Only)

The platform does not send emails to end users (an App is purely Push-driven). Emails are strictly for Admin alerts using a service like Resend or SendGrid.

*   **Alert-01: Scraper Failure.** If Job 1 fails 3 times consecutively (e.g., MAL API changes their rate limits).
*   **Alert-02: Edge Sync Failure.** If Cloudflare R2 rejects the JSON upload payload.
*   **Alert-03: Sudden Spike.** If Cloudflare reports a 500% increase in Read Requests (Signaling a viral moment or a DDoS attack).
