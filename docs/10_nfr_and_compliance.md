# 10. Non-Functional Requirements (NFRs), SLAs & Compliance

This document specifies the system's quality attributes beyond its functional behavior — performance, security, scalability, availability, observability, and accessibility.

---

## 10.1 Performance Requirements

| ID | Requirement | Target | Measurement Method |
|:---|:---|:---|:---|
| NFR-P001 | Dashboard page load (Time to First Byte) | < 200ms | Vercel Analytics |
| NFR-P002 | Explorer search results return time | < 800ms for queries across 5M+ creator records | PostgreSQL `EXPLAIN ANALYZE`; target index scan, not seq scan |
| NFR-P003 | Kanban drag-and-drop round-trip | < 150ms perceived (optimistic UI + background sync) | Browser DevTools Network tab |
| NFR-P004 | Creator mobile app cold launch | < 2 seconds on iPhone 12 or equivalent | Flutter DevTools |
| NFR-P005 | Creator feed infinite scroll next-page load | < 500ms | API response time logging |
| NFR-P006 | Contest leaderboard live update latency | < 1 second from sale webhook to UI update | End-to-end trace via OpenTelemetry |
| NFR-P007 | DM sending throughput per worker | 1 DM per 45-310 seconds (by design, for safety) | Redis queue depth monitoring |
| NFR-P008 | PayPal payout API round-trip | < 5 seconds end-to-end | APM Trace |
| NFR-P009 | AI Analysis (LLM call) response | < 8 seconds (streaming preferred) | API Gateway timeout config |
| NFR-P010 | Database query p95 latency | < 100ms | AWS RDS Performance Insights |

---

## 10.2 Scalability Requirements

| ID | Requirement | Target |
|:---|:---|:---|
| NFR-S001 | Concurrent brand dashboard users | Support 500 concurrent sessions without degradation |
| NFR-S002 | Concurrent creator app users | Support 10,000 concurrent sessions |
| NFR-S003 | Creator database size | Must perform well up to 10M creator records (indexed) |
| NFR-S004 | Outreach queue throughput | Process 50,000 queued DMs per day across all brands |
| NFR-S005 | Contest leaderboard under load | 5,000 concurrent reads during a $5k contest final hour |
| NFR-S006 | Horizontal scaling | All microservices must be stateless and horizontally scalable via ECS auto-scaling |

---

## 10.3 Availability & Reliability Requirements

| ID | Requirement | Target |
|:---|:---|:---|
| NFR-A001 | Platform uptime SLA | 99.9% (max 8.76 hrs downtime/year) |
| NFR-A002 | Database: Recovery Point Objective (RPO) | < 1 hour (point-in-time recovery) |
| NFR-A003 | Database: Recovery Time Objective (RTO) | < 4 hours (failover to standby) |
| NFR-A004 | Zero-downtime deployments | Blue/Green deployment via ECS; no user-visible interruption |
| NFR-A005 | Circuit breaker on 3rd party APIs | If PayPal API fails 3 consecutive times, queue retries and alert on-call |

---

## 10.4 Security Requirements

| ID | Requirement | Implementation |
|:---|:---|:---|
| NFR-SEC001 | All data in transit encrypted | TLS 1.3 enforced on all endpoints (HSTS header) |
| NFR-SEC002 | All PII encrypted at rest | AES-256-GCM via AWS KMS; keys rotated annually |
| NFR-SEC003 | Passwords hashed with Argon2id | Cost factor: memory 64MB, iterations 3, parallelism 2 |
| NFR-SEC004 | JWT Access Tokens expire in 15min | Short-lived; Refresh tokens (opaque, stored in DB) last 30 days |
| NFR-SEC005 | Rate limiting on all public endpoints | 100 req/min per IP on auth routes; 500 req/min on data routes |
| NFR-SEC006 | SQL Injection prevention | Prisma ORM parameterized queries; no raw SQL except admin scripts |
| NFR-SEC007 | XSS prevention | React's JSX auto-escaping; CSP headers set: `script-src 'self'` |
| NFR-SEC008 | CSRF prevention | SameSite=Lax cookies; CSRF token on all state-changing forms |
| NFR-SEC009 | Secret management | All API keys, DB passwords in AWS Secrets Manager; never in `.env` files in production |
| NFR-SEC010 | Dependency vulnerability scanning | GitHub Dependabot + Snyk integrated into CI; block merge if HIGH/CRITICAL CVE found |
| NFR-SEC011 | Audit logging | Every state change on `collaborations`, `ledger_transactions`, `contracts` logged to immutable `audit_events` table with `user_id`, `action`, `timestamp`, `ip_address`, `old_value`, `new_value` |

---

## 10.5 Observability & Monitoring Stack

| Component | Tool | Purpose |
|:---|:---|:---|
| APM (Application Performance Monitoring) | Datadog or New Relic | Trace every request end-to-end across Node.js ↔ Python microservices |
| Log Aggregation | AWS CloudWatch Logs → Datadog | Centralized searchable logs |
| Error Tracking | Sentry | Capture unhandled exceptions in Next.js, NestJS, Flutter |
| Uptime Monitoring | Betteruptime or Pingdom | External health checks every 30s; PagerDuty alerts |
| Database Monitoring | AWS RDS Performance Insights | Slow query detection, connection pool exhaustion alerts |
| Redis Monitoring | Redis Commander + Datadog | Queue depth, memory usage, eviction rates |
| Custom Dashboards | Grafana | Business KPIs: Active Campaigns, DMs Sent, Revenue Processed |

### Alerting Severity Levels
| Severity | Condition | Response Time | Notification |
|:---|:---|:---|:---|
| **P0 - Critical** | Platform completely down; Payments failing | < 15 min | PagerDuty phone call + Slack #incidents |
| **P1 - High** | DM engine stalled; Leaderboard not updating | < 1 hour | Slack alert + Email to on-call |
| **P2 - Medium** | Explorer search degraded (> 3s) | < 4 hours | Slack alert |
| **P3 - Low** | Non-critical UI rendering bug | Next business day | Jira ticket auto-created |

---

## 10.6 Accessibility Requirements (WCAG 2.1 AA)

| ID | Requirement |
|:---|:---|
| NFR-ACC001 | All interactive elements must have ARIA labels |
| NFR-ACC002 | Color contrast ratio minimum 4.5:1 for body text, 3:1 for large text |
| NFR-ACC003 | All forms must be navigable via keyboard (Tab/Shift+Tab) |
| NFR-ACC004 | All images/icons must have descriptive `alt` text |
| NFR-ACC005 | Mobile app must support Dynamic Type (iOS) and Font Scaling (Android) |
| NFR-ACC006 | Animations must respect `prefers-reduced-motion` media query |

---

## 10.7 Browser & Device Compatibility Matrix

| Platform | Supported Versions |
|:---|:---|
| Chrome (Desktop) | Last 2 major versions |
| Firefox (Desktop) | Last 2 major versions |
| Safari (Desktop) | Last 2 major versions |
| Edge (Desktop) | Last 2 major versions |
| Safari (iOS) | iOS 16+ |
| Chrome (Android) | Android 10+ |
| Flutter App (iOS) | iOS 15+ |
| Flutter App (Android) | Android 8.0+ (API 26+) |
| Screen Resolutions (Web) | 1280x720 minimum; responsive up to 3840x2160 |
| Screen Resolutions (Mobile) | 320px minimum width (iPhone SE) to 428px (iPhone 15 Pro Max) |

---
