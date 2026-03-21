# 7. Screen Specifications & Wireframes

> **Cross-References:** User stories → [05 — App Stories](./05_user_stories_app.md) / [06 — Admin Stories](./06_user_stories_admin.md) · Feature IDs → [02 — Features](./02_core_features_and_roadmap.md).

This document specifies the exact UI states, widget hierarchy, color tokens, spacing, and interaction behaviors for every screen in both the Flutter App and the Admin Dashboard.

---

## 7.1 Design System Tokens

### 7.1.1 Color Palette (Dark Mode — Default)
| Token | Hex | Usage |
|:---|:---|:---|
| `--bg-primary` | `#000000` | OLED black background (saves battery on AMOLED) |
| `--bg-card` | `#121212` | Card surfaces, modals |
| `--bg-elevated` | `#1E1E1E` | Elevated surfaces (bottom sheets, FABs) |
| `--text-primary` | `#FFFFFF` | Headings, titles |
| `--text-secondary` | `#B0B0B0` | Subtitles, studio names, timestamps |
| `--text-tertiary` | `#6B6B6B` | Disabled text, placeholder text |
| `--accent-primary` | `#00E5FF` | Electric Blue — countdown timers, active pills, CTAs |
| `--accent-success` | `#00C853` | "Aired ✓" status, "Watch Now" buttons |
| `--accent-danger` | `#FF1744` | "DELAYED" tag, errors, destructive actions |
| `--accent-warning` | `#FFAB00` | Offline banner, low-priority alerts |
| `--accent-cancelled` | `#9E9E9E` | Cancelled episodes, disabled cards |
| `--nav-blur` | `rgba(0,0,0,0.6)` | Bottom nav bar blur overlay |

### 7.1.2 Typography
| Style | Font | Size | Weight | Usage |
|:---|:---|:---|:---|:---|
| `heading-xl` | Inter | 28px | Bold (700) | Screen titles ("Today's Pulse") |
| `heading-lg` | Inter | 22px | SemiBold (600) | Section headers |
| `body-lg` | Inter | 16px | Regular (400) | Synopsis text, news body |
| `body-md` | Inter | 14px | Regular (400) | Studio name, secondary info |
| `body-sm` | Inter | 12px | Medium (500) | Timestamps, source labels |
| `countdown` | JetBrains Mono | 20px | Bold (700) | Countdown timer digits (monospace for stable width) |

### 7.1.3 Spacing & Layout
*   **Card Padding:** 12px horizontal, 10px vertical.
*   **Card Gap (List):** 8px between cards.
*   **Grid Gap:** 10px.
*   **Screen Margin:** 16px horizontal.
*   **Bottom Nav Height:** 64px + safe area.
*   **Poster Aspect Ratio:** 2:3 (width:height).
*   **News Image Ratio:** 16:9.
*   **Corner Radius (Cards):** 12px.
*   **Corner Radius (Buttons):** 8px.
*   **Corner Radius (Posters):** 8px.

---

## 7.2 Flutter App: Global Layout

All screens share this scaffold:

*   **AppBar:** Custom `SliverAppBar`. Collapses on scroll. Contains screen title and optional action buttons.
*   **Bottom Navigation Bar:**
    *   Style: Frosted glass blur (`BackdropFilter`) over `--nav-blur` color.
    *   Tabs:
        1. `Schedule` (Icon: `Icons.calendar_today`) — Landing tab.
        2. `Discover` (Icon: `Icons.explore_outlined`) — Seasonal grid.
        3. `News` (Icon: `Icons.newspaper_outlined`) — News feed.
        4. `Profile` (Icon: `Icons.person_outline`) — Watchlist + Settings.
    *   Active tab: `--accent-primary` icon + label. Inactive: `--text-tertiary`.
*   **Theme:** Dark Mode by default. OLED Black (`#000000`). Light Mode available in Settings (white bg `#FAFAFA`).

---

## 7.3 Flutter App: Screen Specifications

### S-01: The Daily Schedule (Landing Screen)
*   **Maps to:** APP-03, APP-04, APP-05, APP-06 (Features F-01, F-02, F-03).
*   **Header:** `heading-xl`: "Today's Pulse" with the formatted date: "Thursday, March 21".
*   **Day Selector:** Horizontal row of pill-shaped `ChoiceChip` widgets: `[Mon] [Tue] [Wed] [Thu] [Fri] [Sat] [Sun]`.
    *   Active pill: Filled `--accent-primary` background, white text.
    *   Inactive pill: `--bg-card` background, `--text-secondary` text.
    *   Interaction: Tap or horizontal swipe (`PageView`) changes the active day.
*   **Schedule List:** `ListView.builder` of Anime Schedule Cards.
*   **Anime Schedule Card Anatomy:**
    ```
    ┌────────────────────────────────────────────────┐
    │ ┌──────┐  Title EN (max 2 lines)          [+]  │
    │ │Poster│  Studio Name (greyed)                  │
    │ │ 2:3  │  [CR logo] [NF logo]                   │
    │ │      │  ┌──────────────────────┐              │
    │ └──────┘  │  02:14:45  countdown │              │
    │           └──────────────────────┘              │
    └────────────────────────────────────────────────┘
    ```
    *   **Poster:** 60×90px, `ClipRRect` with 8px radius. `cached_network_image` with shimmer placeholder.
    *   **Title:** `body-lg`, bold, white. `maxLines: 2`, `overflow: ellipsis`.
    *   **Studio:** `body-sm`, `--text-secondary`.
    *   **Platform Logos:** 20×20px icons for Crunchyroll, Netflix, etc. Max 2 shown.
    *   **Countdown Timer:** `countdown` font style in `--accent-primary`. Updates every second via `Timer.periodic`. When timer reaches 0:00:00, text changes to "Aired ✓" in `--accent-success`.
    *   **Quick-Add Button:** Circular icon button (24px diameter). Default: `+` outline. On tap: morphs to `✓` with a scale-bounce animation (150ms). Haptic feedback on iOS.
*   **Empty State:** If no anime airs on the selected day: illustration + "No drops today. Check another day!" text.

### S-02: Anime Detail Sheet (Bottom Modal)
*   **Maps to:** APP-09, APP-10, APP-11, APP-12 (Features F-07, F-08, F-09, F-10).
*   **Trigger:** Tap on any schedule card or seasonal grid card.
*   **Behavior:** `showModalBottomSheet` with `DraggableScrollableSheet`. Initial height: 85%. Drag down to dismiss.
*   **Layout (top-to-bottom):**
    1.  **Hero Banner:** Full-width blurred background of `banner_image_url`. Overlaid with a gradient fade to `--bg-card`.
    2.  **Cover Art:** Sharp, high-res poster (120×180px) overlapping the banner's bottom edge, offset left.
    3.  **Title:** `heading-lg`, white. Below title: `body-sm` Japanese title in `--text-secondary`.
    4.  **Pill Row:** Horizontally scrollable chips: `[Action] [Fantasy] [MAPPA] [★ 8.4 MAL]`. Genre pills: `--bg-elevated` background. MAL score pill: `--accent-primary` background.
    5.  **Synopsis:** `body-lg`, `--text-primary`. Clamped to 3 lines with "Read More" toggle (expand/collapse animation, 200ms).
    6.  **Episode Tracker:** Horizontal `ListView` of small circular chips labeled "Ep 1", "Ep 2", etc.
        *   `Aired + Watched`: Filled `--accent-success` circle.
        *   `Aired + Unwatched`: Outlined `--accent-success` circle. Tappable to mark watched.
        *   `Upcoming`: Outlined `--text-tertiary` circle with mini-countdown text below.
        *   `Delayed`: Outlined `--accent-danger` circle with "DELAYED" text.
    7.  **Embedded PV Player:** If `youtube_url` exists, render `youtube_player_iframe` widget (16:9 ratio). Auto-pauses on scroll-away.
    8.  **"Where to Watch" Section:** Header: "Where to Watch". Grid of rectangular buttons (56×40px) with platform logos. Tapping deep-links to the streaming app (`crunchyroll://series/...`). Fallback to web browser if app not installed.

### S-03: The News Feed
*   **Maps to:** APP-13, APP-14 (Features F-11, F-12).
*   **Layout:** Full-screen infinite-scroll vertical `ListView.builder`.
*   **Card Anatomy:**
    ```
    ┌────────────────────────────────────────┐
    │ Source: AnimeNewsNetwork  •  2h ago     │
    │                                        │
    │ Chainsaw Man Season 2 Announced for    │
    │ Fall 2026 by MAPPA Studios             │
    │                                        │
    │ ┌────────────────────────────────────┐  │
    │ │                                    │  │
    │ │     16:9 Cover Image / YouTube     │  │
    │ │                                    │  │
    │ └────────────────────────────────────┘  │
    │                                        │
    │ [Share ↗]              [View Details →] │
    └────────────────────────────────────────┘
    ```
    *   **Source:** `body-sm`, `--text-tertiary`.
    *   **Headline:** `body-lg`, bold, white. Max 3 lines.
    *   **Media:** If `youtube_url` exists → YouTube iframe. Else if `image_url` exists → `CachedNetworkImage` (16:9).
    *   **Sponsored Card:** Identical layout but with a subtle "Sponsored" label in `--accent-warning` and position fixed at index 3 in the list.
*   **Pull-to-Refresh:** `RefreshIndicator` re-fetches `news.json` from R2.
*   **Pagination:** Loads 20 cards initially. On scroll-to-end, renders next 20 from JSON (up to 50 total).

### S-04: Discover / Seasonal Chart
*   **Maps to:** APP-08 (Feature F-05).
*   **Header:** `heading-xl`: "Spring 2026" (auto-detects current season).
*   **Filter Chips:** Horizontal scroll: `[All] [Popular] [Action] [Romance] [Fantasy] [Sci-Fi]`. Active chip: filled `--accent-primary`.
*   **Grid:** `GridView.builder`, 2 columns (phone) or 3 columns (tablet).
*   **Card:** Poster-only card. 2:3 ratio `ClipRRect`. Title overlaid at bottom with gradient shadow (`LinearGradient` from transparent to `--bg-primary`). `body-md`, white, bold.

### S-04b: Offline State
*   **Maps to:** APP-23.
*   If HTTP GET to R2 fails (timeout or no connection):
    *   **Banner:** Material banner drops from top: amber background (`--accent-warning`), text: "Offline Mode — Showing cached schedule."
    *   **Body:** Restores JSON from `SharedPreferences` cache and renders schedule normally.
    *   **Images:** `cached_network_image` loads from disk cache. If cache miss, shows grey placeholder with anime icon.

### S-05: Profile & Settings
*   **Maps to:** APP-15, APP-16, APP-17, APP-21, APP-22 (Features F-14, F-15, F-20, F-21, F-22).
*   **Top Section:** Avatar (placeholder or Google avatar), username (or "Guest"), watchlist stats: "5 Watching · 12 Completed".
*   **Watchlist Tabs:** Segmented control: `[Watching] [Plan to Watch] [Completed] [Dropped]`. Each tab shows a `ListView` of anime cards with poster thumbnail + title.
*   **Settings Section (Below Watchlist):**
    *   Title Display Language: Dropdown (English / Romaji / Japanese).
    *   Theme: Toggle (Dark / Light). PRO: Custom accent color picker.
    *   Notifications: Toggle global push on/off.
    *   Sign In / Sign Out (Supabase Auth).
    *   Delete Account (red destructive button, confirmation dialog).
    *   App Version, Privacy Policy link, Terms of Service link.

---

## 7.4 Admin Dashboard (Next.js) Screens

### S-06: Admin Login
*   Standard email/password form. No branding required (internal tool).
*   "Forgot Password" link triggers Supabase password reset email.
*   OTP field shown if 2FA is enabled.

### S-07: The Admin Hub (Dashboard)
*   **Sidebar Navigation (Left, 240px wide):**
    *   🏠 Dashboard
    *   📥 Staging Queue (badge count of pending items)
    *   📺 Anime Catalog
    *   ⏰ Schedule Master
    *   📰 News Manager
    *   ⚙️ System & Logs
*   **Main Content Area:**
    *   Row 1: 4 KPI Cards (Total Shows, Today's Drops, Pending Queue, Last R2 Sync).
    *   Row 2: Quick Actions — `[+ Add Show]` `[+ Write News]` `[⚡ Force Sync R2]` buttons.

### S-08: Staging Queue Page
*   **Maps to:** ADM-04, ADM-05, ADM-06, ADM-07.
*   **Table Columns:** Checkbox (for batch), Title, Air Time (Raw), Air Time (UTC), Cover Thumbnail, Status Badge (NEW/UPDATE), Actions (Approve/Edit/Reject).
*   **Batch Actions Bar:** Appears when 1+ rows selected: `[Approve Selected ({n})]` `[Reject Selected ({n})]`.
*   **Visual Diff:** Inline diff rendering for UPDATE items (old values struck-through red, new values green).

### S-09: Anime Editor (Data Entry Form)
*   **Maps to:** ADM-08, ADM-09, ADM-10.
*   **Layout:** Single-column form.
*   **Fields:** Title EN (required), Title JP, Synopsis (textarea), Studio (required), Genres (multi-select chips), Season/Year dropdowns, Streaming Platforms (checkboxes + URL inputs), MAL ID, AniList ID.
*   **Image Upload:** Drag-and-drop zone. Preview thumbnail after upload. Auto-converts to WebP.

### S-10: Schedule Master (Data Grid)
*   **Maps to:** ADM-12, ADM-13, ADM-14, ADM-15.
*   **Layout:** Full-width data grid (TanStack Table or AG Grid).
*   **Columns:** Status (dropdown), Anime Title (read-only), Episode Number, Air Date, Air Time, Timezone, Actions.
*   **Interactions:** Double-click cell to edit inline. "Save All Changes" button. "Bulk Generate Episodes" action.

### S-11: News Manager
*   **Maps to:** ADM-16, ADM-17, ADM-18.
*   **List View:** Table of published/scheduled news. Columns: Headline, Category, Published At, Is Sponsored, Actions (Edit/Delete).
*   **Create/Edit Form:** Headline, Body Summary (textarea, max 500 chars), Source URL, Cover Image (upload), YouTube URL, Category (dropdown), Is Sponsored (toggle), Publish Date/Time picker.
