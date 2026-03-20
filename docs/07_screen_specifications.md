# 7. Screen-by-Screen Wireframe & UI Specification

This document describes **every screen** in the platform, specifying every field, button, empty state, loading state, error state, and interaction.

---

## PART A: BRAND WEB DASHBOARD (Next.js)

---

### Screen 7.1: Login (`/login`)
| Element | Type | Validation Rules | Behavior |
|:---|:---|:---|:---|
| Email Input | `<input type="email">` | Required; must match RFC 5322 email regex | Auto-lowercase on blur |
| Password Input | `<input type="password">` | Required; min 8 chars | Show/hide toggle icon |
| "Remember Me" Checkbox | `<input type="checkbox">` | Optional | Sets JWT refresh token duration to 30 days vs 24 hrs |
| "Forgot Password?" Link | `<a>` | — | Navigates to `/forgot-password` |
| "Sign Up" Link | `<a>` | — | Navigates to `/register` |
| "Login" Button | `<button>` | Disabled until both fields valid | Shows spinner on click; disabled during request |
| **Error States:** | | | |
| — Invalid credentials | — | — | Red banner: "Invalid email or password. Please try again." |
| — Account locked (5 failed attempts) | — | — | Red banner: "Account locked for 15 minutes. Contact support." |
| — 2FA Required | — | — | Redirects to `/login/2fa` with TOTP input |
| **Empty State:** | N/A | | |
| **Loading State:** | Full-page skeleton with logo | | |

---

### Screen 7.1b: Registration (`/register`)
| Element | Type | Validation Rules | Behavior |
|:---|:---|:---|:---|
| Company Name | `<input type="text">` | Required; min 2, max 255 chars | |
| Email Input | `<input type="email">` | Required; RFC 5322; must be unique in `users` | On blur: async check via `GET /api/v1/auth/check-email`; if taken → red inline: "Email already registered." |
| Password Input | `<input type="password">` | Required; regex `^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$` | Strength meter: Weak (red), Medium (yellow), Strong (green) |
| Confirm Password | `<input type="password">` | Must match Password field | Real-time match check on keystroke |
| Stripe Card Element | Stripe Elements `<CardElement>` | Required; valid card | Stripe.js validates client-side before submission |
| "Create Account" Button | `<button>` | Disabled until all fields valid | Shows spinner; calls `POST /api/v1/auth/register` |
| **Error States:** | | | |
| — Card declined | — | — | Red banner: "Card Declined: [Stripe decline_code message]" |
| — Duplicate email (race condition) | — | — | Red banner: "An account with this email already exists." |
| — Server error | — | — | Red banner: "Something went wrong. Please try again." |
| **Success State:** | Redirect to `/dashboard/setup` (Onboarding wizard) | | |

---

### Screen 7.1c: Forgot Password (`/forgot-password`)
| Element | Type | Validation Rules | Behavior |
|:---|:---|:---|:---|
| Email Input | `<input type="email">` | Required; RFC 5322 | |
| "Send Reset Link" Button | `<button>` | Disabled until email valid | Calls `POST /api/v1/auth/forgot-password` |
| **Success State:** | Green banner: "If an account exists for this email, we've sent a password reset link." (intentionally vague for security) | | |
| **Reset Form (via link):** | `/reset-password?token=JWT` | | |
| — New Password | `<input type="password">` | Same regex as Registration | Strength meter |
| — Confirm Password | `<input type="password">` | Must match | |
| — "Reset Password" Button | `<button>` | | Calls `POST /api/v1/auth/reset-password` with token + new password |
| — Token Expired | — | — | Full page: "This link has expired. Request a new one." with link to `/forgot-password` |

---

### Screen 7.2: Brand Dashboard Home (`/dashboard`)
**Purpose:** High-level KPI overview for the brand manager.

| Element | Type | Data Source | Refresh |
|:---|:---|:---|:---|
| **KPI Card: "Active Creators"** | Card with large number | `SELECT COUNT(*) FROM collaborations WHERE brand_id = X AND current_stage NOT IN ('COMPLETED', 'REJECTED')` | Real-time via WebSocket |
| **KPI Card: "Revenue This Month"** | Card with currency | `SUM(revenue) FROM attribution WHERE month = CURRENT` | Cached; refreshed every 5 min |
| **KPI Card: "DMs Sent Today"** | Card with number | `COUNT(*) FROM outreach_logs WHERE brand_id = X AND date = TODAY` | Real-time |
| **KPI Card: "Reply Rate"** | Card with percentage | `(replied / sent) * 100` from outreach_logs | Cached; 15 min |
| **Chart: Revenue Over Time** | Line chart (Recharts) | 30/60/90 day toggle; X=Date, Y=Revenue | Toggle triggers API refetch |
| **Table: "Recent Activity"** | Paginated table | Last 20 `collaboration` state changes | Infinite scroll pagination |
| **Empty State:** | "You haven't started any campaigns yet. [Create Campaign] button." | | |

---

### Screen 7.3: Creator Explorer (`/dashboard/explorer`)
**Purpose:** The AI-powered search engine.

| Element | Type | Validation / Constraints | Behavior |
|:---|:---|:---|:---|
| **Search Bar** | Text input with autocomplete | Debounce 300ms before API call | Returns creator handles matching input |
| **Filter: Niche** | Multi-select dropdown | Enum: Beauty, Tech, Fitness, Home, Food, Fashion, Pet, Baby, Automotive, Other | AND logic with other filters |
| **Filter: GMV Range** | Dual-thumb slider | Min: $0, Max: $500,000, Step: $1,000 | URL query params update on change |
| **Filter: Follower Tier** | Checkbox group | Nano (1k-10k), Micro (10k-100k), Macro (100k-1M), Mega (1M+) | Multiple selectable |
| **Filter: Engagement Rate Min** | Single slider | 0.0% — 25.0%, Step: 0.5% | |
| **Filter: Location** | Google Places autocomplete | Returns `lat`, `lng`, `radius_miles` | Triggers geo-query on backend |
| **Filter: Platform** | Radio buttons | Instagram, YouTube, Amazon | Single select |
| **"Lookalike Search" Input** | Text input for handle | Must start with `@` | Triggers vector similarity search on backend |
| **Results Table Columns:** | | | |
| — Avatar | 40x40px thumbnail | Lazy-loaded from CDN | |
| — Handle | Clickable link | — | Opens creator detail modal |
| — Followers | Formatted number (e.g., "85.2k") | — | |
| — GMV (30d) | Currency (e.g., "$12,400") | — | Sortable column |
| — Engagement Rate | Percentage (e.g., "4.2%") | — | Sortable column |
| — AI Score | Badge (1-10 with color) | Green >= 7, Yellow 4-6, Red <= 3 | Hover shows breakdown tooltip |
| — "Add to Campaign" | Checkbox | — | Bulk-select action bar appears at top |
| **Pagination:** | Cursor-based (not offset) | 20 results per page | "Load More" button at bottom |
| **Empty State:** | "No creators match your filters. Try broadening your search." with illustration | | |
| **Loading State:** | 20 skeleton rows with shimmer animation | | |

---

### Screen 7.4: Campaign Kanban Board (`/dashboard/campaigns/:id`)
**Purpose:** The visual pipeline tracking creator relationships.

| Element | Type | Behavior |
|:---|:---|:---|
| **Column Headers** | Draggable (reorderable) | Default order matches [State Machine 8.2](./08_business_rules_and_rbac.md#82-collaboration-state-machine): SCOUTED → CONTACTED → REPLIED → NEGOTIATING → CONTRACT_SENT → CONTRACT_SIGNED → ADDRESS_RECEIVED → SAMPLE_PROCESSING → SAMPLE_SHIPPED → SAMPLE_DELIVERED → NUDGE_SENT → VIDEO_SUBMITTED → VIDEO_APPROVED → VIDEO_LIVE → PAYMENT_PENDING → PAID → ARCHIVED |
| **Collapsed Columns** | Toggle | Columns with 0 cards auto-collapse to headers only to save horizontal space |
| **Creator Card** | Drag-and-drop item | Shows: Avatar, Handle, Days in Stage badge, Last Activity timestamp |
| — Card Click | Opens full Creator Side Panel | Side panel slides in from the right (60% width overlay) |
| — Card Badge: "⚠️" | Warning icon | Appears if creator has been in current stage > 7 days (calculated from `collaborations.stage_entered_at`) |
| **Side Panel Contents:** | | |
| — Creator profile header | Avatar + handle + follower count + link to Instagram profile | |
| — "Outreach History" tab | Timeline of all DMs/Emails sent (from `outreach_logs`), with read receipts if available | |
| — "Shipping" tab | Address (masked: "*** Main St, Austin TX"), Tracking number, Carrier status (from `collaborations.tracking_number`) | |
| — "Content" tab | Embedded video player if `collaborations.video_url IS NOT NULL` | |
| — "Contract" tab | Contract signing status from `contracts` table; link to view signed PDF from S3 | |
| — "Notes" section | Rich text area (Markdown support) for brand team internal notes | Auto-saves on blur |
| — "Move Stage" dropdown | Select target column | Same as drag-drop; validates transition rules from [State Machine 8.2](./08_business_rules_and_rbac.md#82-collaboration-state-machine) |
| **Drag Validation Rules:** | | |
| — Cannot skip states (must follow state machine order) | Card snaps back; toast: "Invalid transition" | |
| — Cannot move to "SAMPLE_SHIPPED" if `shipping_address` is NULL | UI snaps card back; toast: "Address missing" | |
| — Cannot move to "PAID" if `contract.is_signed` is FALSE | UI snaps card back; toast: "Contract not signed" | |
| — Cannot move to "CONTRACT_SIGNED" manually (webhook-driven only) | UI snaps card back; toast: "Waiting for creator's signature" | |
| **Empty State (No creators in campaign):** | "No creators added yet. Go to [Explorer] to find creators." | |

---

### Screen 7.5: Drip Campaign Builder (`/dashboard/campaigns/:id/outreach`)
**Purpose:** A visual flow editor for multi-step automated outreach.

| Element | Type | Behavior |
|:---|:---|:---|
| **Canvas** | React Flow drag-and-drop | Infinite scrollable canvas; zoom in/out; minimap in bottom-right |
| **Node: "Trigger"** | Entry node (green) | Options: "On Add to Campaign", "On Sample Delivered", "Manual Start" |
| **Node: "Send DM"** | Action node (blue) | Fields: Platform (Instagram), Message Template (rich text with `{{variables}}`), A/B variant toggle |
| **Node: "Send Email"** | Action node (blue) | Fields: Subject, Body (HTML editor), From name |
| **Node: "Wait"** | Timer node (grey) | Fields: Duration (integer), Unit (Hours / Days) |
| **Node: "Condition"** | Decision diamond (yellow) | Options: "If Reply Received" (Yes/No branches), "If Email Opened" |
| **Node: "End"** | Terminal node (red) | Campaign sequence terminates for this creator |
| **Variable Tokens Available:** | `{{creator.handle}}`, `{{creator.first_name}}`, `{{brand.name}}`, `{{product.name}}`, `{{campaign.commission_rate}}`, `{{creator.recent_video_topic}}` | |
| **Save Button** | Primary button | Validates flow (must have Trigger and at least one Action). Serializes the DAG as JSON and saves to `campaign_sequences` table. |
| **"Activate" Toggle** | Switch | When ON, queues all un-contacted creators in the campaign into the Redis outreach worker. |

---

## PART B: CREATOR MOBILE APP (Flutter)

---

### Screen 7.6: Creator Login (`/login`)
| Element | Type | Behavior |
|:---|:---|:---|
| "Login with Instagram" Button | Primary CTA | Triggers Instagram OAuth 2.0 flow (redirect to Instagram, return with auth code) |
| "Login with Email" | Secondary link | Navigates to email + password form |
| "Login via Magic Link" | Tertiary link | Input email; backend sends a JWT-signed link valid for 15 minutes |
| **Error States:** | | |
| — Instagram OAuth fails | — | Toast: "Instagram login failed. Please try again." |
| — Magic Link expired | — | Full screen: "This link has expired. Request a new one." |

---

### Screen 7.7: Creator Home Feed (`/home`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Top Navbar** | Fixed | Logo left, Notification bell (badge count) right |
| **Filter Pills** | Horizontal scroll | "All", "Collabs", "High Commission", "Retainers", "Contests", "Amazon" |
| — Active Pill | Filled background | Filters the feed below |
| **Promotional Banner** | Carousel (auto-scroll 5s) | Shows featured campaigns or seasonal contests with imagery |
| **Product Card (Repeating)** | Vertical list | Shows: Product Image (16:9), Brand Logo (24px), Product Title, "XX% Commission", "XXk Sold", "Apply" CTA button |
| — "Apply" Button | Primary CTA | Opens Application Bottom Sheet |
| **Application Bottom Sheet** | Modal from bottom | Fields: "Your Rate ($)" (number input), "# of Videos" (stepper, 1-10), "Why You?" (textarea, max 500 chars), "Submit Application" button |
| **Empty State (No opportunities):** | "No deals available right now. Check back later! 🎉" | |
| **Pull-to-Refresh** | Gesture | Triggers API refetch of feed; shows refresh indicator |
| **Infinite Scroll** | Gesture | Loads next 10 items when 80% scrolled |

---

### Screen 7.8: Creator Contests Tab (`/contests`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Active Contest Card** | Grid (2 columns) | Shows: Brand Logo, Contest Title, Prize ($5,000), Time Remaining countdown |
| — Card Tap | Navigates to Contest Detail | |
| **Contest Detail Screen** | Full screen | |
| — Header | Brand hero image | |
| — Rules Section | Bullet list | E.g., "Post 15 videos", "Hit 6,000 sales" |
| — Reward Tiers Table | Table | Tier 1: $100, Tier 2: $250, Tier 3: $500, Grand Prize: $5,000 |
| — "Join Contest" Button | Primary CTA | Adds creator to `contest_participants` table |
| — **Leaderboard Tab** | Ranked list | Shows: Rank #, Avatar, Handle, Sales Count, Prize Earned so far |
| — Current user is highlighted | Yellow background row | |
| — "Your Rank" sticky footer | Fixed bottom bar | "You are #4. $200 away from Tier 3!" |

---

### Screen 7.9: Creator My Work (`/my-work`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Tab Bar** | Horizontal | "Applied", "In Progress", "Completed", "Not Selected" |
| **Applied Tab** | Card list | Shows: Brand name, Product, Date Applied, Status: "Under Review" |
| **In Progress Tab** | Card list | Shows: Brand name, Product, Stage ("Sample Shipped" / "Content Due"), Due Date countdown |
| — "Upload Content" Button | On eligible cards | Opens a URL input field (paste Instagram Reel link); validates against `instagram.com` domain regex |
| — "View Brief" Button | On eligible cards | Opens the AI-generated script in a modal |
| **Completed Tab** | Card list | Shows: Brand name, Revenue Generated, Commission Earned, "Rate Received" label |
| **Not Selected Tab** | Card list | Shows: Brand name, Date, Reason (if provided by brand) |
| **Empty State per Tab:** | | "Nothing here yet. Browse [Home] to find your first deal!" |

---

### Screen 7.10: Creator Trends (`/trends`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Search Bar** | Text input | Debounce 300ms; searches trending keywords |
| **Trending Keywords List** | Sorted by GMV descending | Each row: Keyword, GMV (7d), Sales Count (7d), Trend Spark (⬆️ or ⬇️) |
| — Row Tap | Expands inline detail | Shows: Mini line chart (7d GMV), Top 3 videos using keyword |
| — **"AI Analysis" Button** | Icon button per row | Triggers LLM call; shows bottom sheet with structured response |
| **AI Analysis Bottom Sheet** | Modal | |
| — Loading State | Shimmer placeholder (3 lines) | |
| — Result | 3 bullet points: "📈 The Hook", "👥 The Demographic", "🎵 The Audio" | |
| — Error State | "AI is busy. Try again in a moment." with Retry button | |

---

### Screen 7.11: Creator Profile & Wallet (`/profile`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Avatar** | Circle image (80px) | Pulled from Instagram OAuth profile picture |
| **Handle** | `@username` (bold) | From `creators.instagram_handle` |
| **"Connected" Badge** | Green chip | Shows if Instagram account is successfully linked |
| **Lifetime Earnings Card** | Display card | Large font: "$X,XXX.XX" |
| **Available Balance Card** | Display card | Large font: "$X,XXX.XX" |
| **"Withdraw to PayPal" Button** | Primary CTA | |
| — Disabled State | Greyed out | If `available_balance < $10.00`; label reads "Min. $10 to withdraw" |
| — Active Flow | Tap → Confirm modal ("Withdraw $XX.XX to your.email@paypal.com?") → Tap Confirm → Spinner → Confetti Lottie animation → Balance updates to $0.00 |
| **"Refer a Friend" Card** | CTA with share icon | Generates unique deeplink; copies to clipboard on tap; toast: "Link copied!" |
| — Referral Stats | Below card | "X friends invited · $XX earned from referrals" |
| **Settings List:** | | |
| — "Edit Shipping Address" | Navigates to address form | Fields: Street, Apt, City, State, Zip (validated via Google Maps API) |
| — "Notification Preferences" | Toggle switches | Push for: New Deals, Contest Updates, Payout Received |
| — "Delete My Account" | Red text button | Confirmation modal: "This will permanently delete all your data. Type 'DELETE' to confirm." → soft-delete per [Data Retention rules](./08_business_rules_and_rbac.md#86-data-retention--deletion-rules) |

---

## PART C: BRAND SETTINGS & ANALYTICS (Next.js) — Additional Screens

---

### Screen 7.12: Brand Settings — Team Management (`/dashboard/settings/team`)
*RBAC: Only `SUPERADMIN` can access. See [RBAC Matrix](./08_business_rules_and_rbac.md#brand-dashboard-permissions).*

| Element | Type | Behavior |
|:---|:---|:---|
| **Team Members Table** | Data table | Columns: Name, Email, Role (badge), Last Login, Actions |
| — "Invite Member" Button | Primary CTA | Opens modal: Email input + Role dropdown (Member / Viewer) + "Send Invite" button |
| — Role dropdown (per row) | Inline dropdown | SuperAdmin can change Member ↔ Viewer. Cannot change own role. |
| — "Remove" Button (per row) | Red text icon | Confirmation modal: "Remove [Name] from your team?" → soft-deletes `user` row |
| — Cannot remove self | — | Button hidden on own row |
| **Pending Invitations Section** | List below table | Shows: Email, Role, Sent Date, "Resend" button, "Cancel" button |

---

### Screen 7.13: Brand Settings — Billing (`/dashboard/settings/billing`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Current Plan Card** | Display | Shows: Tier name, Monthly Price, DM Quota, Seats. "Change Plan" button. |
| — "Change Plan" Modal | Plan comparison table | 3 columns (Starter / Growth / Enterprise) with feature checks; upgrade/downgrade CTA |
| — Upgrade | Stripe Checkout redirect | Immediate plan change; prorated billing |
| — Downgrade | Confirmation modal | "Your plan will downgrade at the end of this billing cycle." |
| **Payment Method** | Stripe Elements | Shows last 4 digits: "•••• 4242". "Update Card" button opens Stripe form |
| **Invoice History** | Paginated table | Columns: Date, Amount, Status (Paid/Failed), PDF Download link |

---

### Screen 7.14: Brand Analytics (`/dashboard/analytics`)
| Element | Type | Behavior |
|:---|:---|:---|
| **Date Range Picker** | Calendar dropdown | Preset ranges: Last 7d, 30d, 90d, Custom |
| **KPI Strip (Horizontal)** | 6 metric cards | Total GMV, Total Revenue, ROAS, Creators Active, Videos Live, Avg Commission Rate |
| **Revenue by Creator (Chart)** | Horizontal bar chart (Recharts) | Top 20 creators sorted by revenue; clickable → opens creator side panel |
| **Revenue by Campaign (Chart)** | Stacked area chart | Per-campaign revenue over time |
| **Funnel Visualization** | Funnel chart | Scouted → Contacted → Replied → Shipped → Video Live → Paid (conversion % at each step) |
| **"Export CSV" Button** | Top-right | Downloads currently visible data as `.csv` file |
| **Empty State:** | "Not enough data yet. Start a campaign to see your analytics." | |

---

### Screen 7.15: Brand Onboarding Wizard (`/dashboard/setup`)
*Shown only on first login after registration.*

| Step | Content | Behavior |
|:---|:---|:---|
| Step 1/4: "Welcome" | Company name confirmation + Industry dropdown | Pre-filled from registration |
| Step 2/4: "Connect Your Store" | Shopify OAuth button, or "Skip for Now" | Grants API access for sample fulfillment |
| Step 3/4: "Create Your First Campaign" | Campaign name + Type (Collab/Retainer/Contest) + Product name | Inserts `campaign` row |
| Step 4/4: "Invite Your Team" | Email + Role input (optional) | Or "Skip" link |
| **Progress Bar** | Top of wizard | 25% → 50% → 75% → 100% |
| **Completion** | Redirect to `/dashboard` with celebration confetti | |

---
