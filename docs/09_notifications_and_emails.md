# 9. Notification System, Email Templates & Push Strategy

This document specifies every notification the platform will ever send, across every channel (Email, Push, In-App, SMS), including exact templates.

---

## 9.1 Notification Channel Matrix

| Event | Email | Push (Mobile) | In-App Toast | SMS |
|:---|:---:|:---:|:---:|:---:|
| Brand: New creator reply received | ✅ | — | ✅ | — |
| Brand: Creator signed contract | ✅ | — | ✅ | — |
| Brand: Sample marked Delivered | — | — | ✅ | — |
| Brand: Creator uploaded video | ✅ | — | ✅ | — |
| Brand: DM account rate-limited (alert) | ✅ | — | ✅ (red) | — |
| Brand: Weekly performance digest | ✅ | — | — | — |
| Creator: New deal available (matching niche) | — | ✅ | — | — |
| Creator: Application accepted | ✅ | ✅ | ✅ | — |
| Creator: Application rejected | ✅ | — | — | — |
| Creator: Contract ready to sign | — | ✅ | ✅ | — |
| Creator: Sample shipped | ✅ | ✅ | — | — |
| Creator: Sample delivered | — | ✅ | ✅ | — |
| Creator: Reminder to post (Nudge) | — | ✅ | — | — |
| Creator: Video approved by brand | — | ✅ | ✅ | — |
| Creator: Video rejected (needs revision) | ✅ | ✅ | ✅ | — |
| Creator: Payment processed | ✅ | ✅ | ✅ (confetti) | ✅ |
| Creator: Contest leaderboard position changed | — | ✅ | — | — |
| Creator: Referral bonus earned | — | ✅ | ✅ | — |
| Creator: Account deletion confirmed | ✅ | — | — | — |
| System: Scheduled maintenance | ✅ | ✅ | ✅ | — |

---

## 9.2 Email Templates (Exact Copy)

### Template E-001: Welcome Email (Brand)
*   **Subject:** "Welcome to Euka-Plus, {{brand.name}}! 🚀"
*   **From:** noreply@eukaplus.com
*   **Body:**
    ```
    Hi {{user.first_name}},

    Your Euka-Plus workspace is live!

    Here's how to launch your first campaign in 3 steps:
    1. 🔍 Head to the Explorer to find your ideal creators.
    2. 📨 Set up your first Drip Campaign with personalized DMs.
    3. 📊 Watch your dashboard light up with real-time analytics.

    [Launch My Dashboard →] (CTA button, links to /dashboard)

    Need help? Reply to this email — a real human will respond within 4 hours.

    — The Euka-Plus Team
    ```
*   **Trigger:** On `brand.created` event.

### Template E-002: Creator Application Accepted
*   **Subject:** "You're in! {{brand.name}} wants to work with you 🎉"
*   **From:** deals@eukaplus.com
*   **Body:**
    ```
    Hey {{creator.handle}},

    Great news — {{brand.name}} has accepted your application 
    for the "{{campaign.title}}" collab!

    Next steps:
    1. Open the Euka app
    2. Go to "My Work" → "In Progress"
    3. Submit your shipping address so they can send you {{product.name}}

    [Open My Work →] (Deep link to mobile app)

    Let's make this one count! 💪
    ```
*   **Trigger:** On `collaboration.current_stage` changed to `NEGOTIATING` (brand accepts application and begins conversation). See [State Machine 8.2](./08_business_rules_and_rbac.md#82-collaboration-state-machine).

### Template E-003: Payout Confirmation
*   **Subject:** "💰 ${{amount}} is on its way to your PayPal!"
*   **From:** payments@eukaplus.com
*   **Body:**
    ```
    Hey {{creator.handle}},

    We've just sent ${{amount}} to {{creator.paypal_email}}.

    Transaction ID: {{paypal.payout_item_id}}
    Deal: {{campaign.title}} for {{brand.name}}
    
    It should arrive in your PayPal within 1-2 business days.

    Your updated balance:
    • Lifetime Earnings: ${{creator.lifetime_earnings}}
    • Available Balance: ${{creator.available_balance}}

    Keep creating amazing content! 🎬

    — The Euka-Plus Team
    ```
*   **Trigger:** On PayPal webhook `status: SUCCESS`.

### Template E-005: Shipping Exception Alert (Brand + Creator)
*   **Subject:** "⚠️ Shipping issue for {{creator.handle}} — {{campaign.title}}"
*   **From:** alerts@eukaplus.com
*   **Body (to Brand):**
    ```
    Hi {{user.first_name}},

    There's a shipping issue with the sample for @{{creator.handle}}:

    📦 Tracking: {{tracking_number}} ({{carrier}})
    ❌ Status: {{shipping_status}} — {{shipping_message}}

    What to do:
    • The creator has been notified and asked to verify their address
    • Once they update it, you can re-ship from the Kanban board

    [View in Kanban →] (CTA button, links to /dashboard/campaigns/{{campaign_id}})

    — The Euka-Plus Team
    ```
*   **Body (to Creator):**
    ```
    Hey {{creator.handle}},

    Your sample from {{brand.name}} couldn't be delivered 😕

    📦 Tracking: {{tracking_number}} ({{carrier}})
    ❌ Status: {{shipping_status}}

    Please double-check your shipping address in the app:
    [Update My Address →] (Deep link to /profile → Edit Shipping Address)

    Once updated, {{brand.name}} will re-ship your {{product.name}}!
    ```
*   **Trigger:** On `collaboration.current_stage` changed to `SHIPPING_EXCEPTION`. See [State Machine 8.2](./08_business_rules_and_rbac.md).

### Template E-004: Weekly Brand Digest
*   **Subject:** "Your weekly Euka-Plus recap — Week of {{week_start_date}}"
*   **From:** reports@eukaplus.com
*   **Body:**
    ```
    Hi {{user.first_name}},

    Here's your weekly performance snapshot for {{brand.name}}:

    📊 This Week at a Glance:
    • New Creators Contacted: {{metrics.contacted}}
    • Reply Rate: {{metrics.reply_rate}}%
    • Samples Shipped: {{metrics.samples_shipped}}
    • Videos Live: {{metrics.videos_live}}
    • Revenue Generated: ${{metrics.revenue}}
    • ROAS: {{metrics.roas}}x

    Top Performing Creator: {{top_creator.handle}} 
    (Generated ${{top_creator.revenue}} from {{top_creator.views}} views)

    [View Full Dashboard →]
    ```
*   **Trigger:** Cron job every Monday 9:00 AM UTC.

---

## 9.3 Push Notification Templates (Mobile)

| ID | Title | Body | Deep Link | Badge |
|:---|:---|:---|:---|:---|
| P-001 | "New Deal Alert 🔥" | "{{brand.name}} is offering {{commission}}% on {{product.name}}!" | `/home?filter=collabs` | +1 |
| P-002 | "Application Accepted! 🎉" | "{{brand.name}} wants to collab. Submit your address now!" | `/my-work/in-progress/{{collab_id}}` | +1 |
| P-003 | "Your sample shipped! 📦" | "Tracking: {{tracking_number}} via {{carrier}}" | `/my-work/in-progress/{{collab_id}}` | — |
| P-004 | "Sample delivered! 🏠" | "Your {{product.name}} just arrived. Time to create!" | `/my-work/in-progress/{{collab_id}}` | +1 |
| P-005 | "Gentle reminder 😊" | "Your {{product.name}} arrived 3 days ago. Don't forget to post!" | `/my-work/in-progress/{{collab_id}}` | — |
| P-006 | "Video approved! ✅" | "{{brand.name}} loved your content. Payment incoming!" | `/profile/wallet` | — |
| P-007 | "Cha-ching! 💰" | "We just sent ${{amount}} to your PayPal!" | `/profile/wallet` | +1 |
| P-008 | "You moved up! 🏆" | "You're now #{{rank}} in the {{contest.title}} contest!" | `/contests/{{contest_id}}/leaderboard` | — |
| P-009 | "Referral Bonus! 🎁" | "{{referred.handle}} just joined. You earned ${{bonus}}!" | `/profile/referrals` | +1 |

---

## 9.4 In-App Notification Center (Bell Icon)

### UI Specification
*   **Badge Count:** Red circle overlaying bell icon. Increments with unread count. Decrements on open.
*   **List View:** Reverse-chronological. Each item: Icon (type-specific), Title, Timestamp ("2 min ago", "Yesterday").
*   **Tap Behavior:** Deep-links to relevant screen. Marks item as `read`.
*   **"Mark All as Read"** button at top-right.
*   **Empty State:** "You're all caught up! 🎉"

---
