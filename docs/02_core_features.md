# 2. Exhaustive Feature Specifications & Edge Cases

> **Cross-References:** This document expands on the features summarized in [01 — PRD](./01_project_overview_and_market.md). For the UI specification of each feature, see [07 — Screen Specs](./07_screen_specifications.md). For the state machine governing status transitions, see [08 — Business Rules](./08_business_rules_and_rbac.md).

---

## 2.1 The AI Affiliate Scouting Engine (Explorer)
*Mapped to: Screen [7.3 — Explorer](./07_screen_specifications.md#screen-73-creator-explorer-dashboardexplorer) | User Story [2.1 — Advanced Filtering](./04_user_stories.md)*

### 2.1.1 The UI Query Builder
| Filter Field | UI Component | Data Type | Backend Mapping | Validation |
|:---|:---|:---|:---|:---|
| Niche | Multi-select dropdown | ENUM | `creators.niche` | At least 1 required when searching |
| GMV 30-Day Range | Dual-thumb slider | NUMERIC | `creators.gmv_30_day BETWEEN min AND max` | Min ≥ 0, Max ≤ 500,000. Min < Max. |
| Follower Tier | Checkbox group | INTEGER range | `creators.follower_count BETWEEN low AND high` | Multi-selectable; values: 1k-10k, 10k-100k, 100k-1M, 1M+ |
| Avg Views Range | Integer min/max inputs | INTEGER | `creators.avg_views BETWEEN min AND max` | Min ≥ 0 |
| Engagement Rate Min | Single slider | FLOAT | `creators.engagement_rate >= value` | Range: 0.0% — 25.0%, Step: 0.5% |
| Location | Google Places autocomplete | JSON (lat, lng, radius) | PostGIS `ST_DWithin(geog, point, radius_m)` | Max radius: 500 miles |
| Platform | Radio buttons | ENUM | `creators.platform = value` | Single select: Instagram, YouTube, Amazon |
| Content Quality (AI Score) | Slider (1-10) | FLOAT | `creators.ai_quality_score >= value` | Populated by nightly Vision AI cron |

### 2.1.2 The "Lookalike" Vector Search
*   **Input:** Brand enters a creator handle (must start with `@`).
*   **Backend Pipeline:**
    1. Python FastAPI receives handle → calls Instagram Graph API to fetch the creator's profile bio, category tags, and audience demographics.
    2. Text is concatenated and embedded via OpenAI `text-embedding-3-small` (1536 dimensions).
    3. Vector is queried against a pgvector index in PostgreSQL using Cosine Similarity (K=50).
    4. Results are filtered by `gmv_30_day > 0` to exclude inactive accounts.
    5. Paginated results returned to the Next.js frontend.
*   **Cost:** ~$0.0001 per embedding call. Batch 100 new creators per minute during ingestion.

### 2.1.3 Edge Cases
| # | Edge Case | Detection | Resolution | UI Feedback |
|:---|:---|:---|:---|:---|
| EC-01 | Query returns 0 results | `results.length === 0` | AI relaxes constraints by 15%; re-query | Toast: "No exact matches. Showing closest results." |
| EC-02 | Creator handle not found for Lookalike | Instagram Graph API 404 | Abort | Modal: "We couldn't find @handle. Double-check the spelling." |
| EC-03 | pgvector timeout (>5s) | DB timeout | Retry 1x; fallback to standard text search | Spinner → "Results loaded from backup index." |

---

## 2.2 The Automated Outreach Engine (Drip Campaigns)
*Mapped to: Screen [7.5 — Drip Builder](./07_screen_specifications.md#screen-75-drip-campaign-builder-dashboardcampaignsidoutreach) | Business Rules [OR-001 through OR-006](./08_business_rules_and_rbac.md#85-outreach-safety-business-rules)*

### 2.2.1 Sequence Builder Canvas
*   **UI Library:** React Flow (v11+). Custom node types defined in `/components/flow-nodes/`.
*   **Available Node Types:**

| Node Type | Icon | Configurable Fields | Output Ports |
|:---|:---|:---|:---|
| Trigger | ▶️ | Event: "On Add to Campaign" / "On Sample Delivered" / "Manual Start" | 1 (Next) |
| Send DM | 💬 | Platform (Instagram/Email), Message Template, A/B Variant ID | 1 (Next) |
| Send Email | ✉️ | Subject, HTML Body, From Name | 1 (Next) |
| Wait | ⏳ | Duration (integer), Unit (Hours/Days) | 1 (Next) |
| Condition | 🔀 | Check: "If Reply Received" / "If Email Opened" / "If Link Clicked" | 2 (Yes / No) |
| End | 🛑 | — | 0 |

*   **Variable Tokens:** `{{creator.handle}}`, `{{creator.first_name}}`, `{{brand.name}}`, `{{product.name}}`, `{{campaign.commission_rate}}`, `{{creator.recent_video_topic}}`
*   **Serialization:** The canvas DAG is serialized to JSON and stored in `campaign_sequences.flow_json` (JSONB column in PostgreSQL).

### 2.2.2 Execution Engine (Worker)
*   **Technology:** Python Celery workers consuming from Redis queue `outreach:pending`.
*   **Per-Message Lifecycle:**
    1. Worker pulls job from Redis.
    2. Checks Redis counter: `brand:{id}:dm_count` — if `>= daily_limit` (per tier from [01 — Pricing](./01_project_overview_and_market.md#18-revenue-model--unit-economics)), job is re-queued with 1hr delay.
    3. Checks Redis flag: `brand:{id}:cooldown` — if `true`, job is re-queued.
    4. Checks Redis for duplicate prevention: `outreach:creator:{id}:48h_lock` — if exists, skip (see rule [OR-005](./08_business_rules_and_rbac.md)).
    5. Applies jitter: `sleep(random(45, 310))` seconds.
    6. Executes DM via Playwright stealth (see [06 — Stealth Ops](./06_ai_and_integrations.md#62-stealth-operations-bypassing-anti-bot-systems)).
    7. Logs result to `outreach_logs` table with status: `SENT`, `FAILED`, or `RATE_LIMITED`.
    8. Sets Redis lock: `outreach:creator:{id}:48h_lock` with TTL 172800s.

### 2.2.3 Edge Cases
| # | Edge Case | Detection | Resolution | UI Feedback |
|:---|:---|:---|:---|:---|
| EC-04 | Creator handle changed → DM fails (404) | HTTP 404 from platform | Halt sequence for creator; set `collaboration.current_stage = HANDLE_INVALID` | Kanban card shows ⚠️ badge |
| EC-05 | Platform rate-limits account (429) | HTTP 429 | Set `brand:{id}:cooldown = true` (4hr TTL); halt *all* outreach for brand | Email notification [E-DM-ALERT](./09_notifications_and_emails.md) |
| EC-06 | Creator replies "stop" / "unsubscribe" | NLP keyword match in reply webhook | Add to `opt_out_list`; archive collaboration | — (silent) |
| EC-07 | Brand has exhausted daily DM quota | Redis counter check | Re-queue with 1hr delay | Dashboard banner: "Daily DM limit reached. Remaining queued for tomorrow." |

---

## 2.3 Creator CRM & Sample Logistics (Kanban)
*Mapped to: Screen [7.4 — Kanban](./07_screen_specifications.md#screen-74-campaign-kanban-board-dashboardcampaignsid) | State Machine [8.2](./08_business_rules_and_rbac.md#82-collaboration-state-machine)*

### 2.3.1 Kanban Board Implementation
*   **Frontend Library:** `@dnd-kit/core` + `@dnd-kit/sortable`.
*   **State Management:** Zustand store mirroring server state. Optimistic updates on drag; rollback on API failure (see Story [2.1 AC3](./04_user_stories.md)).
*   **Default Pipeline Columns:** (matches exactly the State Machine in doc 08)
    `SCOUTED` → `CONTACTED` → `REPLIED` → `NEGOTIATING` → `CONTRACT_SENT` → `CONTRACT_SIGNED` → `ADDRESS_RECEIVED` → `SAMPLE_PROCESSING` → `SAMPLE_SHIPPED` → `SAMPLE_DELIVERED` → `NUDGE_SENT` → `VIDEO_SUBMITTED` → `VIDEO_APPROVED` → `VIDEO_LIVE` → `PAYMENT_PENDING` → `PAID` → `ARCHIVED`

### 2.3.2 Logistics Integration Flows
| Trigger Event | API Called | Payload | Result |
|:---|:---|:---|:---|
| Brand clicks "Fulfill Sample" on card | Shopify `POST /admin/api/2024-01/orders.json` | Zero-dollar order to creator's decrypted address, line item = campaign product | Returns `order_id`; saved to `collaborations.shopify_order_id` |
| Shopify webhook: order fulfilled | — | Contains `tracking_number`, `carrier` | Saved to `collaborations.tracking_number`; stage → `SAMPLE_SHIPPED` |
| EasyPost webhook: `tracker.updated` | — | `status = delivered` | Stage → `SAMPLE_DELIVERED`; starts 3-day Redis timer for [automatic nudge](./09_notifications_and_emails.md) |
| EasyPost webhook: `tracker.updated` | — | `status = return_to_sender` or `failure` | Stage → `SHIPPING_EXCEPTION`; sends email [E-EXCEPTION](./09_notifications_and_emails.md) to brand |

### 2.3.3 Edge Cases
| # | Edge Case | Detection | Resolution |
|:---|:---|:---|:---|
| EC-08 | Carrier loses package (status: `EXCEPTION`) | EasyPost webhook | Move to `SHIPPING_EXCEPTION` column; auto-email creator asking to confirm address; auto-email brand offering reshipment |
| EC-09 | Creator deletes promotional video post-payment | Daily cron job (`check_video_urls`) returns HTTP 404 for `collaborations.video_url` | Flag creator as `UNRELIABLE` in `creators.trust_flag`; alert brand via email |
| EC-10 | Drag to "SAMPLE_SHIPPED" but no `shipping_address` | Server validates pre-condition | API returns 422; UI snaps card back; modal prompts address collection |
| EC-11 | Drag to "PAID" but `contract.is_signed = false` | Server validates pre-condition | API returns 422; UI snaps card back; toast: "Contract not signed yet." |

---

## 2.4 Creator App Modules (Flutter)
*Mapped to: Screens [7.6–7.11](./07_screen_specifications.md) | RBAC [Creator Permissions](./08_business_rules_and_rbac.md#creator-app-permissions)*

### 2.4.1 Feed Algorithm & Opportunity Matching
*   **Input Signals (Weighted):**

| Signal | Weight | Description |
|:---|:---|:---|
| Niche Match | 40% | Creator's historical content category vs. campaign category |
| Conversion History | 25% | Creator's past GMV on similar products |
| Geo-Proximity | 15% | Distance from creator to brand HQ (for event-based collabs) |
| Campaign Budget Remaining | 10% | Campaigns nearing budget cap are deprioritized to avoid waste |
| Recency | 10% | Newer campaigns ranked higher |

*   **Implementation:** PostgreSQL materialized view `creator_feed_scores` refreshed every 15 minutes. Mobile app fetches via `GET /api/v1/creators/feed?page=X`.

### 2.4.2 In-App Native Contract Signing
*Mapped to: [06 — Docuseal API](./06_ai_and_integrations.md#652-docuseal-api-self-hosted-e-signature) | Business Rule [FR contract pre-condition](./08_business_rules_and_rbac.md)*

*   **Flow:**
    1. Brand creates a contract template (Node.js generates PDF with dynamic fields).
    2. Node calls Docuseal → returns `slug`.
    3. Flutter opens `claim_url` in `webview_flutter` widget (full screen).
    4. Creator signs with finger on the touch canvas.
    5. Docuseal fires webhook → Node.js stores signed PDF to S3 → updates `contracts.is_signed = true`, `contracts.signed_at = NOW()`.
    6. SHA-256 hash of the PDF bytes is stored in `contracts.document_hash` for tamper-proof verification.
*   **Edge Case EC-12:** User disconnects mid-signature upload → Flutter caches the signature attempt in local SQLite → Background retry on reconnection.

### 2.4.3 Gamified Contest Engine (Leaderboards)
*Mapped to: Screen [7.8 — Contests](./07_screen_specifications.md#screen-78-creator-contests-tab-contests) | State Machine [8.3 — Contest Lifecycle](./08_business_rules_and_rbac.md#83-contest-lifecycle-state-machine) | Business Rules [CR-001 through CR-004](./08_business_rules_and_rbac.md)*

*   **Real-Time Leaderboard Data Structure (Redis):**
    ```
    Key:    contest:{contest_id}:leaderboard
    Type:   Sorted Set (ZSET)
    Member: creator_id (UUID)
    Score:  sales_count * 1000000 - unix_timestamp_of_last_sale
    ```
*   **Update Trigger:** Every sale attribution webhook → `ZINCRBY contest:{id}:leaderboard 1000000 {creator_id}`.
*   **Read Path:** `ZREVRANGE contest:{id}:leaderboard 0 49 WITHSCORES` → returns top 50; served via WebSocket to Flutter for instant UI refresh.
*   **NFR:** Must respond in < 50ms under 5,000 concurrent reads (see [NFR-P006](./10_nfr_and_compliance.md)).

### 2.4.4 Viral Wave Trend Tool
*Mapped to: Screen [7.10 — Trends](./07_screen_specifications.md#screen-710-creator-trends-trends) | User Story [4.2 — AI Analysis](./04_user_stories.md)*

*   **Data Pipeline:**
    1. Python cron job (every 6 hours) queries Instagram's trending hashtags and product tags for keywords with > 300% week-over-week engagement growth.
    2. Results stored in `trending_keywords` table with `gmv_7d`, `sales_7d`, `trend_direction`.
    3. Creator taps "AI Analysis" → FastAPI endpoint → OpenAI `gpt-4o-mini` generates structured JSON:
        ```json
        {
          "hook": "Creators are using the 'Get Ready With Me' format...",
          "demographic": "Primary audience: Women 18-25 in the US...",
          "audio": "The trending audio is 'Pedro Pedro Pedro' by Jaxomy..."
        }
        ```
    4. Result cached in Redis for 1 hour per keyword to avoid redundant LLM calls.
*   **RBAC:** Free Creators: 5 AI Analysis calls/day. VIP Creators: Unlimited (see [RBAC Matrix](./08_business_rules_and_rbac.md#creator-app-permissions)).

---
