# 10. Non-Functional Requirements (NFRs) & Regulatory Compliance

> **Cross-References:** Governance blueprint for **Maximize-Plus**. Governs infrastructure in [03 — Architecture](./03_technical_architecture.md). Enforces sprint DoD benchmarks in [05 — Roadmap](./05_project_roadmap.md). Governs data models in [08 — Rules](./08_business_rules_and_rbac.md).

## 10.1 System Performance SLAs & Scalability

| NFR Metric Category | Target Benchmark SLA | Measurement Protocol | Failure Mitigation Action |
|:---|:---|:---|:---|
| **Stacking Calculation Latency** | 99th Percentile $< 150\text{ms}$ | Datadog APM Tracing on `/stack/calculate`| Auto-scale ECS Fargate tasks; failover to static rules cache. |
| **API Availability Uptime** | $99.99\%$ Uptime ($\le 5.26\text{ mins/yr}$ downtime)| AWS Route53 Health Checks | Multi-AZ Aurora failover; Cloudflare WAF DDoS mitigation. |
| **Concurrent Calculation Load**| $10,000\text{ req/sec}$ continuous | JMeter Synthetic Benchmarks | Redis MemoryDB auto-sharding expansion. |
| **Instant Gift Card Delivery SLA**| $98\%$ delivered $< 3.0\text{ seconds}$| Webhook to UI socket timer | Asynchronous SQS queue retry worker (`cron_gc_retry`). |

---

## 10.2 Reserve Bank of India (RBI) PPI Compliance

### Master Directions on Digital Prepaid Payment Instruments (PPIs)
Since Maximize-Plus facilitates digital brand vouchers (closed or semi-closed system PPIs) out of Bangalore, India:
1.  **No Direct Float Holding:** Maximize Pay Solutions Pvt. Ltd. acts strictly as a technology facilitator and co-branding partner. All unspent gift voucher monetary value float is held within RBI-escrowed nodal accounts operated by licensed PPI issuers (Pine Labs / Woohoo, Qwix).
2.  **Transaction Caps:** Closed-loop gift vouchers issued without full KYC verification are strictly restricted to a maximum purchase denomination of ₹10,000 per instrument.
3.  **Audit Trail:** Complete immutable audit logging of originating IP, shopper phone number, and PG transaction reference enforced across `orders` and `audit_logs` tables.

---

## 10.3 DPDP Act 2023 Data Privacy Governance

### Digital Personal Data Protection Act Adherence
1.  **Explicit Unbundled Consent:** Shoppers must affirmatively check standalone consent checkboxes before the mobile application activates Accessibility Service DOM checkouts or captures transaction SMS alerts.
2.  **Data Localization:** 100% of consumer personally identifiable information (PII) and financial ledger databases reside permanently inside AWS `ap-south-1` (Mumbai). Zero replication to offshore cloud regions.
3.  **Right to Erasure SLA:** Invoking `DELETE /api/v1/me` guarantees irreversible cryptographic hashing of consumer profile attributes within 30 days.

---

## 10.4 PCI-DSS v4.0 Payment Tokenization

### Card-on-File (CoF) Tokenization Mandates
To eliminate card theft risk during stacked checkouts:
*   **Prohibition of Raw PAN:** Maximize-Plus servers never store raw 16-digit primary account numbers, CVVs, or magnetic stripe data.
*   **Tokenization Vault:** Card saving executes via Juspay Safe CoF network vaults (`user_linked_cards`). Transactions execute passing cryptographic network tokens (`card_network_token`).

---

## 10.5 Observability & WCAG 2.1 AA Accessibility

*   **Observability:** Complete distributed tracing enabled across Kong API Gateway, ECS services, and Aurora PostgreSQL queries via Datadog APM.
*   **Accessibility:** All mobile and web storefront interfaces (Screens 01–16) comply with **WCAG 2.1 Level AA** standards, supporting screen readers (TalkBack / VoiceOver) and high-contrast dark mode palettes.
