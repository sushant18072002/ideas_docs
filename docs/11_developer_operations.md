# 11. Developer Operations Reference — Cron Jobs, WebSocket Events, Environment Variables & Error Codes

> **Cross-References:** This document provides the operational configuration details needed to actually build and run the services defined in [03 — Architecture](./03_technical_architecture.md). Every cron job maps to a feature in [02 — Features](./02_core_features.md). Every error code maps to a screen state in [07 — Screens](./07_screen_specifications.md).

---

## 11.1 Environment Variables (Per Service)

### `euka-api` (Node.js / NestJS)
| Variable | Example Value | Required | Description |
|:---|:---|:---:|:---|
| `NODE_ENV` | `production` | ✅ | `development`, `staging`, `production` |
| `PORT` | `3000` | ✅ | Server listen port |
| `DATABASE_URL` | `postgresql://user:pass@rds-host:5432/euka_prod` | ✅ | Prisma connection string |
| `REDIS_URL` | `redis://elasticache-host:6379` | ✅ | Redis connection |
| `JWT_ACCESS_SECRET` | `(32-byte hex)` | ✅ | Signing key for access tokens |
| `JWT_REFRESH_SECRET` | `(32-byte hex)` | ✅ | Signing key for refresh tokens |
| `JWT_ACCESS_TTL` | `900` | ✅ | Access token TTL in seconds (15min) |
| `JWT_REFRESH_TTL` | `2592000` | ✅ | Refresh token TTL in seconds (30 days) |
| `ENCRYPTION_KEY` | `(AWS KMS key ARN)` | ✅ | For PII AES-256-GCM encryption |
| `STRIPE_SECRET_KEY` | `sk_live_...` | ✅ | Stripe billing API |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | ✅ | Stripe webhook signature verification |
| `PAYPAL_CLIENT_ID` | `...` | ✅ | PayPal Payouts API |
| `PAYPAL_CLIENT_SECRET` | `...` | ✅ | PayPal Payouts API |
| `PAYPAL_MODE` | `live` | ✅ | `sandbox` or `live` |
| `DROPBOX_SIGN_API_KEY` | `...` | ✅ | E-signature API |
| `DROPBOX_SIGN_CLIENT_ID` | `...` | ✅ | Embedded signing client |
| `EASYPOST_API_KEY` | `...` | ✅ | Shipping tracker API |
| `EASYPOST_WEBHOOK_SECRET` | `...` | ✅ | Webhook HMAC verification |
| `SENDGRID_API_KEY` | `SG.xxx` | ✅ | Transactional email |
| `SENDGRID_FROM_EMAIL` | `noreply@eukaplus.com` | ✅ | |
| `GOOGLE_MAPS_API_KEY` | `AIza...` | ✅ | Address validation |
| `AWS_S3_BUCKET` | `euka-prod-contracts` | ✅ | Contract/media storage |
| `AWS_REGION` | `us-east-1` | ✅ | |
| `SHOPIFY_API_KEY` | `...` | ❌ | Per-brand OAuth; stored in `brands` table |
| `SENTRY_DSN` | `https://...@sentry.io/...` | ✅ | Error tracking |
| `CORS_ORIGINS` | `https://app.eukaplus.com,https://creators.eukaplus.com` | ✅ | Comma-separated |

### `euka-scraper` / `euka-outreach` / `euka-ai` (Python)
| Variable | Example Value | Required | Description |
|:---|:---|:---:|:---|
| `BRIGHTDATA_PROXY_URL` | `http://user:pass@brd.superproxy.io:22225` | ✅ | Primary residential proxy |
| `SMARTPROXY_URL` | `http://user:pass@gate.smartproxy.com:7000` | ✅ | Fallback proxy |
| `OPENAI_API_KEY` | `sk-...` | ✅ | GPT-4o, Whisper, Embeddings |
| `PINECONE_API_KEY` | `...` | ✅ | Vector DB |
| `PINECONE_INDEX_NAME` | `euka-creators` | ✅ | |
| `REDIS_URL` | `redis://elasticache-host:6379` | ✅ | Celery broker |
| `DATABASE_URL` | `postgresql://...` | ✅ | Direct DB reads for scraper |

### `euka-mobile` (Flutter — Build-time constants)
| Constant | Value | Description |
|:---|:---|:---|
| `API_BASE_URL` | `https://api.eukaplus.com` | |
| `WS_BASE_URL` | `wss://ws.eukaplus.com` | WebSocket for leaderboard |
| `INSTAGRAM_CLIENT_ID` | `...` | Instagram OAuth login |
| `INSTAGRAM_CLIENT_SECRET` | `...` | Instagram OAuth login |
| `INSTAGRAM_REDIRECT_URI` | `eukaplus://oauth/instagram` | Deep link scheme |
| `PAYPAL_CLIENT_ID` | `...` | PayPal SDK (mobile) |

---

## 11.2 Scheduled Cron Jobs

| Job ID | Service | Schedule | Description | DB/Redis Impact | Cross-Ref |
|:---|:---|:---|:---|:---|:---|
| CRON-01 | `euka-scraper` | Every 6 hours | Scrape Instagram trending hashtags and product tags | INSERT/UPDATE `trending_keywords` | [Feature 2.4.4](./02_core_features.md#244-viral-wave-trend-tool) |
| CRON-02 | `euka-ai` | Daily 2:00 AM UTC | AI Vision scoring (batch 200 creators) | UPDATE `creators.ai_quality_score` | [Feature 6.2](./06_ai_and_integrations.md#62-ai-vision-scoring-pipeline) |
| CRON-03 | `euka-api` | Daily midnight UTC | Reset brand DM counters | DELETE Redis keys `brand:*:dm_count` | [Rule OR-001](./08_business_rules_and_rbac.md#85-outreach-safety-business-rules) |
| CRON-04 | `euka-api` | Daily 3:00 AM UTC | Check video URL validity | SELECT `collaborations.video_url`, HTTP HEAD each → flag 404s | [Edge Case EC-09](./02_core_features.md#233-edge-cases) |
| CRON-05 | `euka-api` | Daily 4:00 AM UTC | Refresh materialized view `creator_feed_scores` | `REFRESH MATERIALIZED VIEW CONCURRENTLY` | [Feature 2.4.1](./02_core_features.md#241-feed-algorithm--opportunity-matching) |
| CRON-06 | `euka-api` | Every minute | Check contests: SCHEDULED→ACTIVE, ACTIVE→CLOSING, CLOSING→ENDED | UPDATE `contests.status` based on timestamps | [State Machine 8.3](./08_business_rules_and_rbac.md#83-contest-lifecycle-state-machine) |
| CRON-07 | `euka-api` | Every minute | Fire nudge DMs (3 days post-delivery) | Query Redis timers; trigger outreach worker | [State transition](./08_business_rules_and_rbac.md#transition-validation-rules-server-side) |
| CRON-08 | `euka-api` | 1 hour before contest ACTIVE | Check participant count ≥ 3; auto-cancel if < 3 | UPDATE `contests.status = CANCELLED`; refund | [Rule CR-003](./08_business_rules_and_rbac.md) |
| CRON-09 | `euka-api` | Monday 9:00 AM UTC | Send weekly brand digest emails | Query `outreach_logs`, `collaborations`, `ledger_transactions` | [Email E-004](./09_notifications_and_emails.md#template-e-004-weekly-brand-digest) |
| CRON-10 | `euka-api` | January 15, annually | Generate 1099-NEC forms for creators ≥ $600 | Query `ledger_transactions` by calendar year | [Rule FR-008](./08_business_rules_and_rbac.md#84-financial-ledger-business-rules) |
| CRON-11 | `euka-api` | Monthly | Purge `outreach_logs` older than 2 years | DELETE with batch LIMIT 10000 | [Data Retention](./08_business_rules_and_rbac.md#86-data-retention--deletion-rules) |
| CRON-12 | `euka-api` | Monthly | Purge video transcripts older than 1 year | DELETE from S3 + DB | [Data Retention](./08_business_rules_and_rbac.md#86-data-retention--deletion-rules) |

---

## 11.3 WebSocket Events (Socket.io)

### Brand Dashboard Channels
| Event Name | Direction | Payload | Trigger | Screen |
|:---|:---|:---|:---|:---|
| `kanban:stage_changed` | Server → Client | `{ collaborationId, oldStage, newStage, creatorHandle, timestamp }` | `collaboration.current_stage` UPDATE | [7.4 Kanban](./07_screen_specifications.md) |
| `kanban:card_added` | Server → Client | `{ collaborationId, creatorId, campaignId }` | New `collaboration` INSERT | [7.4](./07_screen_specifications.md) |
| `dashboard:kpi_update` | Server → Client | `{ activeCreators, revenueToday, dmsSentToday, replyRate }` | KPI recalculated (every 5 min or on-event) | [7.2 Dashboard](./07_screen_specifications.md) |
| `outreach:alert` | Server → Client | `{ brandId, message, severity }` | DM engine rate-limited or stalled | [7.2](./07_screen_specifications.md) |

### Creator Mobile Channels
| Event Name | Direction | Payload | Trigger | Screen |
|:---|:---|:---|:---|:---|
| `leaderboard:update` | Server → Client | `{ contestId, rankings: [{creatorId, rank, score}] }` | Sale webhook → Redis ZINCRBY | [7.8 Contests](./07_screen_specifications.md) |
| `notification:new` | Server → Client | `{ id, type, title, body, deepLink, timestamp }` | Any push-worthy event | [9.4 Notification Center](./09_notifications_and_emails.md) |
| `balance:updated` | Server → Client | `{ availableBalance, lifetimeEarnings }` | `ledger_transaction` INSERT with status CLEARED | [7.11 Wallet](./07_screen_specifications.md) |

### Connection Protocol
1. Client connects with JWT access token as query param: `wss://ws.eukaplus.com?token={jwt}`.
2. Server validates token → extracts `user_id` and `brand_id` / `creator_id`.
3. Server auto-joins the client to rooms: `brand:{brand_id}` or `creator:{creator_id}` and `contest:{active_contest_ids}`.
4. On token expiry: client-side interceptor refreshes token and reconnects automatically.

---

## 11.4 API Error Code Registry

Every API error returns a structured JSON body. Frontend maps `error_code` to user-facing messages.

```json
{
  "error": true,
  "error_code": "AUTH_INVALID_CREDENTIALS",
  "message": "Invalid email or password.",
  "details": {}
}
```

### Authentication Errors (`4xx`)
| Code | HTTP | Message | Screen |
|:---|:---:|:---|:---|
| `AUTH_INVALID_CREDENTIALS` | 401 | "Invalid email or password." | [7.1](./07_screen_specifications.md) |
| `AUTH_ACCOUNT_LOCKED` | 423 | "Account locked for 15 minutes." | [7.1](./07_screen_specifications.md) |
| `AUTH_2FA_REQUIRED` | 403 | "Two-factor authentication required." | [7.1](./07_screen_specifications.md) |
| `AUTH_TOKEN_EXPIRED` | 401 | "Session expired. Please log in again." | All screens |
| `AUTH_MAGIC_LINK_EXPIRED` | 410 | "This link has expired." | [7.6](./07_screen_specifications.md) |
| `AUTH_EMAIL_EXISTS` | 409 | "An account with this email already exists." | [7.1b](./07_screen_specifications.md) |

### Authorization Errors
| Code | HTTP | Message | Rule |
|:---|:---:|:---|:---|
| `RBAC_FORBIDDEN` | 403 | "You do not have permission to perform this action." | [RBAC Matrix](./08_business_rules_and_rbac.md) |
| `TENANT_MISMATCH` | 403 | "Access denied." | Multi-tenant isolation |

### Business Logic Errors
| Code | HTTP | Message | Rule |
|:---|:---:|:---|:---|
| `COLLAB_INVALID_TRANSITION` | 422 | "This stage transition is not allowed." | [State Machine 8.2](./08_business_rules_and_rbac.md) |
| `COLLAB_MISSING_ADDRESS` | 422 | "Shipping address is required before shipping." | [EC-10](./02_core_features.md) |
| `COLLAB_CONTRACT_NOT_SIGNED` | 422 | "Contract must be signed before payment." | [EC-11](./02_core_features.md) |
| `PAYOUT_INSUFFICIENT_BALANCE` | 422 | "Insufficient balance. Minimum withdrawal: $10." | [FR-005](./08_business_rules_and_rbac.md) |
| `PAYOUT_IDEMPOTENCY_DUPLICATE` | 409 | "This withdrawal has already been processed." | [FR-004](./08_business_rules_and_rbac.md) |
| `OUTREACH_DAILY_LIMIT` | 429 | "Daily DM limit reached for your plan." | [OR-001](./08_business_rules_and_rbac.md) |
| `OUTREACH_COOLDOWN` | 429 | "Account is in cooldown. Try again later." | [OR-004](./08_business_rules_and_rbac.md) |
| `CREATOR_APPLICATION_LIMIT` | 429 | "Free tier: max 3 applications per week." | [Creator RBAC](./08_business_rules_and_rbac.md) |
| `AI_ANALYSIS_RATE_LIMIT` | 429 | "Free tier: max 5 AI analyses per day." | [Creator RBAC](./08_business_rules_and_rbac.md) |
| `CONTEST_ESCROW_REQUIRED` | 402 | "Prize pool must be fully funded." | [CR-001](./08_business_rules_and_rbac.md) |
| `CONTEST_MIN_PARTICIPANTS` | 422 | "Minimum 3 participants required." | [CR-003](./08_business_rules_and_rbac.md) |

### External Service Errors
| Code | HTTP | Message | Action |
|:---|:---:|:---|:---|
| `PAYPAL_PAYOUT_FAILED` | 502 | "Payment provider error. Please retry." | Queue for retry; alert on-call |
| `STRIPE_CARD_DECLINED` | 402 | "Card declined: [reason]" | Show Stripe decline reason |
| `OPENAI_SERVICE_ERROR` | 503 | "AI is busy. Try again in a moment." | Retry 1x; show fallback |
| `PINECONE_TIMEOUT` | 504 | "Search temporarily unavailable." | Fallback to PostgreSQL text search |

---

## 11.5 Mobile App Navigation Structure (Flutter)

### Bottom Navigation Bar (5 Tabs)
| Tab Index | Icon | Label | Route | Screen |
|:---|:---|:---|:---|:---|
| 0 | 🏠 | Home | `/home` | [7.7 Feed](./07_screen_specifications.md) |
| 1 | 🏆 | Contests | `/contests` | [7.8 Contests](./07_screen_specifications.md) |
| 2 | 📋 | My Work | `/my-work` | [7.9 My Work](./07_screen_specifications.md) |
| 3 | 📈 | Trends | `/trends` | [7.10 Trends](./07_screen_specifications.md) |
| 4 | 👤 | Profile | `/profile` | [7.11 Profile/Wallet](./07_screen_specifications.md) |

### Navigation Rules
*   Bottom bar is **hidden** on Login and Onboarding screens.
*   Active tab is highlighted with filled icon + accent color.
*   Each tab maintains its own navigation stack (nested `Navigator`).
*   Deep links from push notifications navigate to the correct tab and screen.
*   Badge count on Tab 0 (Home) reflects unread in-app notifications.

### Deep Link Scheme
| URI Pattern | Route | Source |
|:---|:---|:---|
| `eukaplus://home` | Home tab | Push [P-001](./09_notifications_and_emails.md) |
| `eukaplus://my-work/:id` | My Work → specific collab | Push [P-002 to P-006](./09_notifications_and_emails.md) |
| `eukaplus://contests/:id/leaderboard` | Contests → detail → leaderboard | Push [P-008](./09_notifications_and_emails.md) |
| `eukaplus://profile/wallet` | Profile → wallet section | Push [P-007](./09_notifications_and_emails.md) |
| `eukaplus://profile/referrals` | Profile → referral stats | Push [P-009](./09_notifications_and_emails.md) |
| `eukaplus://oauth/instagram?code=X` | OAuth callback | Instagram login redirect |

---

## 11.6 Redis Key Naming Convention

| Key Pattern | Type | TTL | Purpose | Rule |
|:---|:---|:---|:---|:---|
| `brand:{id}:dm_count` | STRING (counter) | Resets at midnight UTC | Daily DM limit tracking | [OR-001](./08_business_rules_and_rbac.md) |
| `brand:{id}:cooldown` | STRING (flag) | 4 hours | Platform rate-limit cooldown | [OR-004](./08_business_rules_and_rbac.md) |
| `outreach:creator:{id}:48h_lock` | STRING (flag) | 48 hours | Prevent duplicate DMs to same creator | [OR-005](./08_business_rules_and_rbac.md) |
| `creator:{id}:ai_calls:{date}` | STRING (counter) | 24 hours | AI Analysis rate limit for Free tier | [Creator RBAC](./08_business_rules_and_rbac.md) |
| `contest:{id}:leaderboard` | SORTED SET (ZSET) | Persistent until contest COMPLETED | Real-time leaderboard rankings | [CR-002](./08_business_rules_and_rbac.md) |
| `idempotency:{key}` | STRING | 60 seconds | Withdrawal deduplication | [FR-004](./08_business_rules_and_rbac.md) |
| `session:{refresh_token_hash}` | HASH | 30 days | Refresh token session tracking | [NFR-SEC004](./10_nfr_and_compliance.md) |
| `nudge:{collab_id}` | STRING (flag) | 3 days | Delivery → nudge timer | [State Machine 8.2](./08_business_rules_and_rbac.md) |
| `cache:trends:{keyword_id}` | STRING (JSON) | 1 hour | Cached AI Analysis result | [Feature 2.4.4](./02_core_features.md) |
| `queue:outreach:pending` | LIST | Persistent | Celery outreach job queue | [Feature 2.2.2](./02_core_features.md) |

---

## 11.7 Deployment Environments

| Environment | URL (Web) | URL (API) | Database | Purpose |
|:---|:---|:---|:---|:---|
| **Local** | `http://localhost:3000` | `http://localhost:3000/api` | Docker Compose PostgreSQL + Redis | Individual dev |
| **Staging** | `https://staging.eukaplus.com` | `https://api-staging.eukaplus.com` | AWS RDS (staging instance) | QA / Demos |
| **Production** | `https://app.eukaplus.com` | `https://api.eukaplus.com` | AWS RDS Multi-AZ | Live |

### CI/CD Pipeline (GitHub Actions)
```mermaid
graph LR
    PR["Pull Request"] --> LINT["Lint + Type Check"]
    LINT --> TEST["Unit Tests (80% coverage)"]
    TEST --> BUILD["Docker Build"]
    BUILD --> STAGING["Deploy to Staging (auto)"]
    STAGING --> E2E["Cypress E2E on Staging"]
    E2E --> APPROVE["Manual Approval Gate"]
    APPROVE --> PROD["Blue/Green Deploy to Production"]
```

### Rollback Procedure
1. On P0 incident: `aws ecs update-service --desired-count 0` on new task definition.
2. `aws ecs update-service --task-definition euka-api:PREVIOUS_VERSION`.
3. Verify health check passes on ALB.
4. Post-mortem within 48 hours.

---
