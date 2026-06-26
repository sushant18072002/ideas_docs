# 9. Omnichannel Notifications & Messaging Architecture

> **Cross-References:** Communication blueprint for **Maximize-Plus**. Triggered by behavioral user stories in [04 — Stories](./04_user_stories.md) and aggregator webhooks in [06 — Integrations](./06_ai_and_integrations.md). Displayed on UI screens in [07 — Screens](./07_screen_specifications.md). Governed by DPDP Act user consent rules in [10 — Compliance](./10_nfr_and_compliance.md).

## 9.1 Omnichannel Notification Routing Matrix

| Notification Event ID | Event Trigger Description | Push (FCM)| SMS (Twilio)| WhatsApp | Email (AWS SES)| Priority Level |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **NOTIF_AUTH_OTP** | User requests login OTP on Screen 16 | ❌ | ✅ | ✅ (Primary)| ❌ | CRITICAL (P0) |
| **NOTIF_GC_DELIVER** | Instant gift card PG payment confirmed | ✅ | ✅ | ✅ | ✅ | HIGH (P1) |
| **NOTIF_OVL_SAVINGS**| Mobile assistant detects cheaper checkout | ✅ Pill | ❌ | ❌ | ❌ | HIGH (P1) |
| **NOTIF_COINS_PENDING**| Affiliate network confirms tracked click | ✅ | ❌ | ❌ | ✅ Weekly | MEDIUM (P2) |
| **NOTIF_COINS_AVAIL**| Cashback settlement return window passes | ✅ | ✅ | ✅ | ✅ | HIGH (P1) |
| **NOTIF_MILES_SENT** | MaxCoins converted to Air India Maharaja | ✅ | ❌ | ✅ | ✅ | HIGH (P1) |
| **NOTIF_CART_SHARE** | Friend opens shared comparison MaxCart | ✅ | ❌ | ❌ | ❌ | LOW (P3) |

---

## 9.2 Push Notification Payloads (Firebase Cloud Messaging)

### NOTIF_GC_DELIVER (Instant Gift Card Issued)
```json
{
  "message": {
    "token": "eU821_fcm_mobile_client_push_token",
    "notification": {
      "title": "🎁 Your Taj Hotels Voucher is Ready!",
      "body": "Tap to reveal your ₹10,000 gift voucher PIN and claim your 400 reward MaxCoins."
    },
    "data": {
      "click_action": "FLUTTER_NOTIFICATION_CLICK",
      "screen_id": "SCR_04_ORDER_CONFIRM",
      "order_id": "ORD-TAJ-991823",
      "brand_slug": "taj_hotels"
    },
    "android": {
      "priority": "high",
      "notification": {
        "channel_id": "fintech_instant_fulfillment_v1",
        "color": "#10B981"
      }
    }
  }
}
```

---

## 9.3 WhatsApp Interactive Message Templates (Twilio / Meta API)

### Template Name: `instant_voucher_delivery_v2`
**Approved Category:** TRANSACTIONAL
**Language:** English (`en`)

```markdown
*⚡ Maximize-Plus Instant Fulfillment*

Hey {{1}}! Your discounted *{{2}}* gift card purchase was successful.

*Voucher Denomination:* ₹{{3}}
*Effective Stacked Price:* ₹{{4}} (You saved ₹{{5}})

Tap the button below to instantly copy your uncompromised voucher code and PIN.

[👉 Reveal & Copy PIN Box] *(Dynamic Quick Reply URL: https://www.maximize.money/app/pin/{{6}})*
```

---

## 9.4 AWS SES Transactional HTML Email Template

### Template: Airline Miles Conversion Confirmation (`EMAIL_MILES_SENT`)
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0F172A; color: #F8FAFC; margin: 0; padding: 40px; }
        .card { max-width: 600px; margin: 0 auto; background-color: #1E293B; border-radius: 16px; padding: 32px; border: 1px solid #334155; }
        .hero { font-size: 24px; font-weight: 700; color: #38BDF8; margin-bottom: 16px; }
        .stats { background-color: #0F172A; border-radius: 12px; padding: 20px; margin: 24px 0; }
        .stat-row { display: flex; justify-content: space-between; margin-bottom: 12px; }
        .label { color: #94A3B8; font-size: 14px; }
        .value { font-weight: 600; font-size: 16px; color: #F1F5F9; }
        .cta { display: block; width: 100%; text-align: center; background: linear-gradient(135deg, #0284C7, #2563EB); color: white; padding: 16px; border-radius: 12px; text-decoration: none; font-weight: 600; margin-top: 24px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="hero">✈️ Maharaja Points Transferred!</div>
        <p>Hi Rohan, your MaxCoins conversion request during the exclusive 5:4 transfer window has executed successfully.</p>
        
        <div class="stats">
            <div class="stat-row"><span class="label">Frequent Flyer Account:</span><span class="value">Air India (AI-982341)</span></div>
            <div class="stat-row"><span class="label">Debited MaxCoins:</span><span class="value">-5,000 Coins (₹5,000)</span></div>
            <div class="stat-row"><span class="label">Credited Loyalty Yield:</span><span class="value" style="color: #34D399;">+4,000 Maharaja Points</span></div>
            <div class="stat-row"><span class="label">Partner Reference:</span><span class="value">AI_LOYALTY_TX_88192</span></div>
        </div>
        
        <a href="https://www.maximize.money/max-coins" class="cta">View Updated Coin Ledger</a>
    </div>
</body>
</html>
```
