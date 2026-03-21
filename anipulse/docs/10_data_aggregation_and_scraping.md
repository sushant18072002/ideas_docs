# 10. Data Aggregation & Scraping Strategy

> **Context:** To avoid external API rate limits and complex backend crons, AniPulse relies on a **semi-manual scraping pipeline**. Data is extracted directly from the DOM of popular anime sites via a Chrome Extension (or Python scraper), dumped into the local Admin dashboard for human review, and then pushed to production.

## 10.1 The Chrome Extension Scraper (Recommended)

Building a custom Chrome Extension is the safest and most reliable way to extract data because the extension runs in the *user's* browser. It completely bypasses Cloudflare bot protection, CAPTCHAs, and IP bans on target websites.

### How It Works:
1.  **Target Sites:** 
    *   Schedules: `https://anikoto.me/home` (or livechart/MAL).
    *   News: AnimeNewsNetwork, Crunchyroll News.
2.  **The Action:** The Admin navigates to the target site, clicks the AniPulse Extension icon, and hits "Extract Schedule".
3.  **The Payload:** The extension parses the DOM (HTML nodes), structures it into a uniform JSON format, and sends a `POST` request to the local Admin Dashboard (`http://localhost:3000/api/ingest`).

## 10.2 The Admin Review Pipeline

Data ingested from the wild web is never pushed directly to production. It must enter a "Staging" state.

### The Staging Queue UI (`localhost:3000/queue`)
*   When the local Admin dashboard receives the JSON payload from the extension, it populates a "Pending Review" table.
*   **Visual Diffing:** The UI highlights changes. If the scraper found that *Jujutsu Kaisen* moved from 9:00 AM to 10:00 AM, the old time is struck through in red, and the new time is highlighted in green.
*   **The Final Action:** The Admin clicks **[Approve & Sync]**. Only then is the database updated, which triggers the Cloudflare JSON generation.

## 10.3 HTML Parsing Strategy (Target: Anikoto / News Sites)

Because UI layouts change, the scraper relies on DOM query selectors that are easily configurable.

**Example Extractor Logic (JavaScript injected via Extension):**
```javascript
// Pseudo-code for Anikoto.me extraction
const animeCards = document.querySelectorAll('.anime-card-class');
const payload = [];

animeCards.forEach(card => {
    payload.push({
        title_en: card.querySelector('.title-en').innerText,
        air_time_local: card.querySelector('.countdown-text').innerText, // Will be parsed to UTC
        cover_url: card.querySelector('img').src
    });
});

// Send to local Admin
fetch('http://localhost:3000/api/ingest', {
    method: 'POST',
    body: JSON.stringify(payload)
});
```

## 10.4 News Scraping
Extracting news is simpler but requires formatting HTML to Markdown or plain text so it renders perfectly in the Flutter App.
*   The Extension grabs the Article Title, Cover Image `src`, and paragraphs `<p>`, joins them, and sends them to the Admin.
*   The Admin can trim the article down to a 3-line summary before hitting "Publish to R2".
