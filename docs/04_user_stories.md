# 4. Epic & User Story Specifications

> **Cross-References:** Each story maps to a specific screen in [07 — Screen Specs](./07_screen_specifications.md), is governed by rules in [08 — Business Rules](./08_business_rules_and_rbac.md), and implemented using the schema in [03 — Architecture](./03_technical_architecture.md).

---

## Epic 1: Multi-Tenant Auth & Onboarding (Brand Side)
*Priority: P0 — Must Have | Sprint: 1-3 (Weeks 1-6)*

### Story 1.1: Brand Registration
*   **Screen:** [7.1 — Login/Register](./07_screen_specifications.md#screen-71-login-login)
*   **DB Tables:** `brands`, `users`
*   **Acceptance Criteria:**
    *   **AC1 [Happy Path]:** *Given* `/register`, *When* valid email + password (regex: `^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$`) + Stripe card, *Then* create `brand` row, create `user` row with `role = SUPERADMIN`, redirect to `/dashboard/setup`.
    *   **AC2 [Rate Limiting]:** *Given* > 5 registrations from same IP in 1 min, *Then* Redis blocks IP → HTTP 429. *(See [NFR-SEC005](./10_nfr_and_compliance.md))*
    *   **AC3 [Stripe Failure]:** *Given* declined card, *Then* DB transaction rolls back entirely (no orphan rows) → UI: "Card Declined: [Stripe Message]".
    *   **AC4 [Duplicate Email]:** *Given* email already exists in `users`, *Then* HTTP 409 → UI: "An account with this email already exists."

### Story 1.2: Invite Team Members (RBAC)
*   **Screen:** `/dashboard/settings/team`
*   **DB Tables:** `users`
*   **RBAC:** Only `SUPERADMIN` can invite. *(See [RBAC Matrix](./08_business_rules_and_rbac.md#brand-dashboard-permissions))*
*   **Acceptance Criteria:**
    *   **AC1:** *Given* settings page, *When* SuperAdmin enters an email + selects role (`MEMBER` or `VIEWER`), *Then* email invitation sent via [SendGrid](./09_notifications_and_emails.md) with magic link.
    *   **AC2:** *When* invitee clicks link, *Then* redirected to password-set form → `user` row created with `brand_id` and selected `role`.
    *   **AC3:** *Given* a `VIEWER` role user logs in, *Then* all "Create", "Delete", and "Edit" buttons are hidden per RBAC matrix.

---

## Epic 2: Creator Discovery (Brand Side)
*Priority: P0 — Must Have | Sprint: 4-8 (Weeks 7-16)*

### Story 2.1: Advanced Multi-Filter Search
*   **Screen:** [7.3 — Explorer](./07_screen_specifications.md#screen-73-creator-explorer-dashboardexplorer)
*   **API:** `GET /api/v1/creators/search`
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Explorer page, *When* Brand applies filters (Niche=Beauty AND GMV>$10k AND Follower Tier=Micro), *Then* results return in < 800ms *(see [NFR-P002](./10_nfr_and_compliance.md))*.
    *   **AC2:** *When* results load, *Then* each row displays: Avatar, Handle, Followers (formatted), GMV (currency), Engagement Rate (%), AI Score (colored badge).
    *   **AC3:** *When* 0 results, *Then* UI shows empty state with illustration + "No exact matches. Try broadening your search."

### Story 2.2: Lookalike Vector Search
*   **API:** `POST /api/v1/creators/lookalike`
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Explorer page, *When* Brand types `@topCreator` in the Lookalike input, *Then* system embeds profile → queries Pinecone → returns top 50 similar creators.
    *   **AC2:** *When* handle not found (API 404), *Then* modal: "We couldn't find @topCreator. Double-check the spelling."

### Story 2.3: Bulk Add to Campaign
*   **Acceptance Criteria:**
    *   **AC1:** *Given* search results, *When* Brand checks 50 rows and clicks "Add to Campaign" → selects "Summer Sale" from dropdown, *Then* 50 `collaboration` rows inserted with `current_stage = SCOUTED`, without duplicating existing records.
    *   **AC2:** *When* a creator was already added to this campaign, *Then* skip silently and display toast: "45 added, 5 already in campaign."

---

## Epic 3: CRM & Automated Outreach (Brand Side)
*Priority: P0 — Must Have | Sprint: 4-11 (Weeks 7-22)*

### Story 3.1: Kanban Drag-and-Drop
*   **Screen:** [7.4 — Kanban](./07_screen_specifications.md#screen-74-campaign-kanban-board-dashboardcampaignsid)
*   **State Machine:** [8.2](./08_business_rules_and_rbac.md#82-collaboration-state-machine)
*   **Acceptance Criteria:**
    *   **AC1 [Optimistic UI]:** *Given* Kanban, *When* drag card from `CONTACTED` to `REPLIED`, *Then* UI updates instantly → background `PATCH /api/v1/collaborations/:id` fires.
    *   **AC2 [Network Rollback]:** *Given* PATCH returns 500, *Then* toast: "Network error, reverting" → card snaps back.
    *   **AC3 [Blocked Transition]:** *Given* drag to `SAMPLE_SHIPPED` without `shipping_address`, *Then* card snaps back → modal: "Address missing. Send a collection link?"
    *   **AC4 [Blocked Transition]:** *Given* drag to `PAID` without `contract.is_signed = true`, *Then* card snaps back → toast: "Contract not signed yet."

### Story 3.2: Drip Campaign Configuration
*   **Screen:** [7.5 — Drip Builder](./07_screen_specifications.md#screen-75-drip-campaign-builder-dashboardcampaignsidoutreach)
*   **Business Rules:** [OR-001 through OR-006](./08_business_rules_and_rbac.md#85-outreach-safety-business-rules)
*   **Acceptance Criteria:**
    *   **AC1:** *Given* campaign builder canvas, *When* Brand connects Trigger → Send DM → Wait 2 Days → Send Email → End, *Then* DAG serialized as JSON to `campaign_sequences.flow_json`.
    *   **AC2:** *When* Brand activates the toggle, *Then* all un-contacted creators are queued into Redis `outreach:pending`.
    *   **AC3 [Limit Enforcement]:** *When* batch exceeds daily DM limit for this brand's tier, *Then* save button disabled → warning: "Max [X] DMs per 24hrs on your plan."

---

## Epic 4: Creator Mobile Experience
*Priority: P0 — Must Have | Sprint: 11-16 (Weeks 21-32)*

### Story 4.1: Browse & Apply to Opportunities
*   **Screen:** [7.7 — Creator Feed](./07_screen_specifications.md#screen-77-creator-home-feed-home)
*   **RBAC:** [Creator Permissions](./08_business_rules_and_rbac.md#creator-app-permissions)
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Home feed, *When* Creator taps "Retainers" pill, *Then* feed filters instantly to `campaigns.type = RETAINER`.
    *   **AC2:** *Given* Creator is Free tier, *When* they apply > 3 times in a week, *Then* 4th application blocked → modal: "Upgrade to VIP for unlimited applications."
    *   **AC3:** *Given* application bottom sheet, *When* Creator submits rate + video count + "Why You", *Then* `collaboration` row inserted with `current_stage = SCOUTED`, notification sent to Brand ([P-002](./09_notifications_and_emails.md)).

### Story 4.2: Wallet & PayPal Withdrawal
*   **Screen:** [7.11 — Profile/Wallet](./07_screen_specifications.md#screen-711-creator-profile--wallet-profile)
*   **Business Rules:** [FR-001 through FR-008](./08_business_rules_and_rbac.md#84-financial-ledger-business-rules)
*   **API:** `POST /api/v1/payouts/withdraw`
*   **Acceptance Criteria:**
    *   **AC1 [Minimum]:** *Given* `available_balance` < $10, *Then* button greyed + label: "Min. $10 to withdraw".
    *   **AC2 [Idempotency]:** *Given* user taps Withdraw during lag → multiple taps, *Then* frontend generates UUIDv4 `idempotency_key` → button disabled → backend executes exactly 1 transaction.
    *   **AC3 [Success]:** *When* PayPal API returns 201, *Then* ledger row inserted with `type=WITHDRAWN, status=CLEARED` → Lottie confetti → push notification [P-007](./09_notifications_and_emails.md) → email [E-003](./09_notifications_and_emails.md).
    *   **AC4 [PayPal Failure]:** *When* PayPal API returns 4xx/5xx, *Then* ledger row `status=FAILED` → toast: "Payout failed. Try again later." → alert to Platform Admin.

### Story 4.3: Contest Participation & Leaderboard
*   **Screen:** [7.8 — Contests](./07_screen_specifications.md#screen-78-creator-contests-tab-contests)
*   **State Machine:** [8.3](./08_business_rules_and_rbac.md#83-contest-lifecycle-state-machine)
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Active contest, *When* Creator taps "Join Contest", *Then* row inserted in `contest_participants` → leaderboard entry created at score 0.
    *   **AC2:** *When* sale attributed, *Then* Redis `ZINCRBY` → leaderboard updates via WebSocket in < 1s *(see [NFR-P006](./10_nfr_and_compliance.md))*.
    *   **AC3:** *When* Creator is in 4th place, *Then* sticky footer shows: "You are #4. $200 away from Tier 3!" Push notification [P-008](./09_notifications_and_emails.md) sent on rank change.

### Story 4.4: AI Trend Analysis
*   **Screen:** [7.10 — Trends](./07_screen_specifications.md#screen-710-creator-trends-trends)
*   **RBAC:** Free: 5 calls/day. VIP: Unlimited.
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Trends tab, *When* Creator taps "AI Analysis" on a keyword, *Then* shimmer loading state → FastAPI calls `gpt-4o-mini` → result displayed as 3 bullets.
    *   **AC2 [Cache Hit]:** *Given* another creator analyzed this keyword < 1 hour ago, *Then* result served from Redis cache → no LLM call → < 200ms response.
    *   **AC3 [LLM Error]:** *Given* OpenAI returns 500 or malformed JSON, *Then* bottom sheet shows: "AI is busy. Try again in a moment." + Retry button.
    *   **AC4 [Rate Limit]:** *Given* Free Creator has used 5 calls today, *Then* button disabled → tooltip: "Upgrade to VIP for unlimited AI Analysis."

---

## Epic 5: Contracts & Legal (Cross-Cutting)
*Priority: P1 — Should Have | Sprint: 15-16 (Weeks 29-32)*

### Story 5.1: In-App E-Signature
*   **Screen:** Flutter full-screen WebView
*   **API Integration:** [DropBox Sign](./06_ai_and_integrations.md#632-dropbox-sign-api-embedded-e-signatures)
*   **Acceptance Criteria:**
    *   **AC1:** *Given* Brand offers Usage Rights deal, *Then* Node generates PDF → DropBox Sign returns `claim_url` → Flutter opens in `webview_flutter`.
    *   **AC2:** *When* Creator signs, *Then* DropBox webhook fires → `contracts.is_signed = true` → PDF stored in S3 → SHA-256 hash saved in `contracts.document_hash`.
    *   **AC3 [Disconnect]:** *When* Creator loses internet mid-signature, *Then* Flutter caches locally (SQLite) → background retry on reconnection.

---

## Epic 6: Analytics & Reporting (Brand Side)
*Priority: P1 — Should Have | Sprint: 17-19 (Weeks 33-38)*

### Story 6.1: KPI Dashboard
*   **Screen:** [7.2 — Dashboard Home](./07_screen_specifications.md#screen-72-brand-dashboard-home-dashboard)
*   **Acceptance Criteria:**
    *   **AC1:** *Given* dashboard, *Then* display 4 KPI cards: Active Creators, Revenue This Month, DMs Sent Today, Reply Rate.
    *   **AC2:** Revenue chart toggles 30/60/90 days; triggers API refetch on toggle.
    *   **AC3:** "Recent Activity" table shows last 20 `collaboration` stage changes with infinite scroll.

### Story 6.2: CSV Export
*   **RBAC:** Available to `SUPERADMIN`, `MEMBER`, `VIEWER`. *(See [RBAC Matrix](./08_business_rules_and_rbac.md))*
*   **Acceptance Criteria:**
    *   **AC1:** *Given* any data table (Explorer, Kanban list view, Analytics), *When* user clicks "Export CSV", *Then* server generates CSV file and triggers browser download.
    *   **AC2:** CSV includes all visible columns + `collaboration_id` for reconciliation.

---
