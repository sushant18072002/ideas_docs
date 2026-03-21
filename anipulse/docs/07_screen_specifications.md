# 7. Screen Specifications & Wireframes

This document details the exact UI/UX states, widgets, and layout hierarchy for both the Flutter App and the Next.js Admin Panel.

## 7.1 Flutter App: Global Layout

All screens share this scaffold:
*   **App Bar:** Hidden or Custom SliverAppBar (collapses on scroll).
*   **Bottom Navigation Bar (Blur Effect):**
    *   `Schedule` (Icon: Calendar)
    *   `Discover` (Icon: Search/Grid)
    *   `News` (Icon: Newspaper)
    *   `Profile/Settings` (Icon: User)
*   **Theme:** Dark Mode by default. Primary Accent: Electric Blue or Brand Color. Background: Deep OLED Black (`#000000`).

---

## 7.2 Flutter App: Screens

### S-01: The Daily Schedule (Landing Screen)
*   **Top Header:** "Today's Pulse". Shows current date. 
*   **Day Selector (Horizontal):** Pill-shaped toggles `[Mon] [Tue] [Wed] [Thu] [Fri] [Sat] [Sun]`. The current day is highlighted. 
*   **Main Body:** A `ListView.builder` of Anime Cards.
*   **Anime Card Anatomy:**
    *   Left: Anime Poster (2:3 ratio, rounded corners).
    *   Right Top: English Title (Truncated 2 lines, MaxLines=2).
    *   Right Middle: Studio Name (Greyed out text).
    *   Right Bottom: Huge, prominent Countdown Timer. `02:14:45` (Updates dynamically every second via a Timer/Ticker).
    *   Far Right Edge: Circular `+` button to add to Watchlist.

### S-02: Anime Detail Sheet (Bottom Modal)
*   **Behavior:** Drags up from the bottom, covers 80% of the screen. Drag down to dismiss.
*   **Hero Image:** A faded, blurred background of the cover art.
*   **Header:** Sharp, high-res Cover Art overlapping the top edge. Huge Title.
*   **Pill Row:** `[Action] [Fantasy] [MAPPA] [★ 8.4 MAL]`.
*   **Synopsis Text:** Expandable text widget.
*   **Episodes List:** Horizontal scroll of episodes. Checked boxes for episodes the user has seen.
*   **Where to Watch:** Grid of rectangular buttons containing logos for Crunchyroll, Netflix, Amazon Prime.

### S-03: The News Feed
*   **Layout:** Infinite vertical scroll, akin to Instagram/Twitter but denser.
*   **Card Anatomy:**
    *   Top: Tiny "Source" text (e.g., `From @anime_pr`) and "2h ago".
    *   Body: 3 lines of headline text.
    *   Media: Large 16:9 Image or YouTube iframe.
*   **Action Row:** `[Share Icon]` `[View Details]`.

### S-04: Discover / Seasonal Chart
*   **Layout:** A `GridView` (2 columns or 3 columns depending on screen size).
*   **Filter Chips (Top):** `[Winter 2026] [Popular] [Action] [Romance]`.
*   **Cards:** Just the Poster Image with the Title overlaid at the bottom in a gradient shadow.

### S-04b: Offline State / No Connection
*   If the HTTP GET to Cloudflare fails (no internet):
    *   **Body:** Restores from the device's local `Shared_Preferences` string cache.
    *   **Banner:** A small amber banner drops from the top: "Offline Mode - Showing Cached Schedule".
    *   **Images:** Handled gracefully by `cached_network_image` fallback blocks.

---

## 7.3 Admin Dashboard (Next.js)

### S-05: Admin Authentication
*   **Standard generic login UI.** No branding necessary. Email, Password, OTP field if 2FA enabled.

### S-06: The Admin Hub (Dashboard)
*   **Sidebar (Left):**
    *   🏠 Home
    *   📺 Anime List
    *   ⏰ Schedule Master
    *   📰 News Manager
    *   ⚙️ System Triggers & Logs
*   **Main Content (Right):**
    *   Row 1: 3 KPI Cards. (Total Shows Tracked, Missing Data Alerts, Last JSON Cache Sync Time).
    *   Row 2: "Quick Actions". (Add Show, Write News, Invalidate CDN).

### S-07: Anime Editor (Data Entry Page)
*   **Layout:** Split pane.
    *   **Left Pane:** Search bar (Jikan MAL API). Admin types "Frieren", clicks search, clicks the result.
    *   **Right Pane:** The Form. It auto-fills with the API data.
*   **Form Fields:** Title EN, Title JP, Synopsis, Studio, Select Licensed Platforms (Checkboxes).
*   **Image Uploader:** Drag and drop zone. Converts to `.webp` right in the browser using a JS library before uploading.

### S-08: Schedule Master
*   **Layout:** A large, terrifyingly powerful Data Grid (like Airtable).
*   **Columns:** Status, Anime Title, Ep Number, Air Date, Air Time.
*   **Interaction:** Double-tap a cell to edit. "Save All" button at the top right bulk-updates Supabase. 
