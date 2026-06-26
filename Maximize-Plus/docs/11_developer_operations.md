# 11. Developer Operations (DevOps) & Engineering Reference

> **Cross-References:** Daily engineering reference for **Maximize-Plus**. Governs runtime deployment of microservices in [03 — Architecture](./03_technical_architecture.md). Orchestrates scheduled jobs supporting [02 — Features](./02_core_features.md) and [04 — Stories](./04_user_stories.md).

## 11.1 Environment Variable Dictionary (40+ Variables)

### AWS Infrastructure & Database Storage
```bash
# Aurora PostgreSQL Primary DB Cluster
DB_PRIMARY_HOST=aurora-pgsql-mumbai-prod.cluster-c9182.ap-south-1.rds.amazonaws.com
DB_PRIMARY_PORT=5432
DB_PRIMARY_NAME=maximize_plus_prod
DB_PRIMARY_USER=maxplus_app_role
DB_PRIMARY_SECRET_ARN=arn:aws:secretsmanager:ap-south-1:9918231:secret:db_prod-eU91

# AWS MemoryDB Redis Cluster
REDIS_CLUSTER_URI=rediss://maxplus-cache-mumbai.memdb.ap-south-1.amazonaws.com:6379
REDIS_AUTH_TOKEN=kms_enc_redis_token_9912

# AWS KMS Hardware Encryption Keys
KMS_GC_VAULT_KEY_ID=arn:aws:kms:ap-south-1:9918231:key/1123-8819-gc-vault
```

### Fintech Payment Gateways & Aggregators
```bash
# Razorpay / Juspay Payment Routing
RAZORPAY_KEY_ID=rzp_live_991823149
RAZORPAY_KEY_SECRET=kms_enc_rzp_secret
JUSPAY_MERCHANT_ID=MAXIMIZE_PLUS_SAFE
JUSPAY_API_KEY=kms_enc_juspay_key

# Qwix / Woohoo Instant GC Wholesale Fulfillment
QWIX_MERCHANT_SLUG=maximize_plus_b2b
QWIX_API_SECRET=kms_enc_qwix_secret
```

### Affiliate Aggregators & Loyalty Partners
```bash
# Admitad / Cuelinks Affiliate Tracking
ADMITAD_CLIENT_ID=maxplus_admitad_app
ADMITAD_CLIENT_SECRET=kms_enc_adm_secret
ADMITAD_WEBHOOK_HMAC_KEY=kms_hmac_adm_9912

# Air India Maharaja Club Loyalty API
AIR_INDIA_OAUTH_CLIENT_ID=maximize_fintech_partner
AIR_INDIA_OAUTH_CLIENT_SECRET=kms_enc_ai_secret
MAXCOIN_INR_PEG_RATE=1.00
```

---

## 11.2 Scheduled Background Cron Jobs (15 Jobs)

| Cron Job ID | Schedule Expression | Microservice Task | Execution Description | Target Table / Service |
|:---|:---|:---|:---|:---|
| **CRON-01** | `*/5 * * * *` (Every 5 mins) | `cron_gc_lock_release` | Releases expired 300s gift card checkout reservation locks | `gift_card_catalog` |
| **CRON-02** | `0 * * * *` (Hourly) | `cron_affiliate_epc_sync` | Scrapes latest EPC and net commission rules from Admitad | `partner_brands` |
| **CRON-03** | `0 2 * * *` (Daily 2 AM) | `cron_cashback_settlement`| Queries Admitad/Impact API to settle Pending Coins to Available | `maxcoins_ledger` |
| **CRON-04** | `0 */6 * * *` (Every 6 hrs) | `cron_miles_sync_retry` | Batches and retries failed Marriott Bonvoy point transfers | `miles_conversion_rates`|
| **CRON-05** | `0 4 * * 0` (Weekly Sun 4 AM)| `cron_wholesale_gc_sync` | Reconciles wholesale gift voucher stock float with Qwix | `gift_card_catalog` |
| **CRON-06** | `0 3 1 * *` (Monthly 1st) | `cron_dpdp_anonymize` | Cascading anonymization of CCPA/DPDP deleted shopper PII | `users`, `user_kyc` |

---

## 11.3 WebSocket Live Event Dictionary

### 1. `WSE_STACK_CALCULATED` (Real-Time Savings Update)
Dispatched to web client when background compare scraper updates cart pricing.
```json
{
  "event": "WSE_STACK_CALCULATED",
  "payload": {
    "cart_id": "cart_compare_99123",
    "cheapest_merchant": "AMAZON_INDIA",
    "effective_price_inr": 48200.00,
    "net_savings_inr": 6800.00
  }
}
```

### 2. `WSE_GC_FULFILLED` (Instant Voucher PIN Ready)
Dispatched to mobile/web UI upon asynchronous PG confirmation.
```json
{
  "event": "WSE_GC_FULFILLED",
  "payload": {
    "order_id": "ORD-TAJ-991823",
    "status": "DELIVERED",
    "reveal_token": "kms_tok_881249"
  }
}
```

---

## 11.4 Standardized System Error Codes

| Error Code Identifier | HTTP Status | User-Facing Error Title | Detailed System Cause |
|:---|:---:|:---|:---|
| **ERR_STACK_EXPIRED** | `410 Gone` | Calculation Expired | The 300s cart calculation or promo coupon lock has timed out. |
| **ERR_COINS_INSUFFICIENT**| `422 Unprocessable`| Insufficient MaxCoins | Available balance is below required gift card or miles conversion cost. |
| **ERR_KYC_REQUIRED** | `403 Forbidden` | PAN Verification Needed | Cumulative annual wallet withdrawals exceed ₹10,000 without PAN verification. |
| **ERR_GC_OUT_OF_STOCK** | `409 Conflict` | Denomination Sold Out | Digital voucher wholesale pool for target brand tier depleted. |
| **ERR_HMAC_SIG_INVALID** | `401 Unauthorized` | Security Signature Failed| Webhook payload HMAC SHA256 signature mismatch. |

---

## 11.5 Redis Key Pattern Dictionary

| Redis Key Pattern | Key Data Type | TTL Expiry | Caching Purpose |
|:---|:---:|:---:|:---|
| `CACHE_BRAND_RULES:{brand_slug}`| Hash | 300 seconds | Stores active affiliate rakes and coupon codes. |
| `RATE_LIMIT_USER:{user_id}:CALC`| Integer | 60 seconds | Velocity limit counter (Max 30 calculations/min). |
| `LOCK_GC_ITEM:{gc_sku_id}` | String (UUID)| 300 seconds | Distributed mutex lock reserving gift voucher inventory. |
| `OVL_SUPPRESS:{user_id}:{brand}`| String ("1") | 86400 secs (24h)| Assistant popup suppression flag post-dismissal. |

---

## 11.6 CI/CD Deployment & Mobile Deep Links

*   **CI/CD Pipeline:** GitHub Actions builds Docker containers upon merge to `main`. Deploys via AWS CodeDeploy Blue-Green strategy to ECS Fargate.
*   **Deep Link URI Scheme:** `maxplus://app/stack/{cart_token}` (Routes mobile app directly to calculated comparison modal).
