# EUKA Clone — Project Documentation Hub

Welcome to the **Euka-Plus** project repository. This documentation set constitutes a full Business Analyst-grade Software Requirements Specification (SRS). All 11 documents are **fully cross-referenced** — every feature traces to a screen spec, every story traces to a business rule, and every sprint task traces to a user story.

## Documentation Index

| # | Document | Contents | Key Cross-References |
|:--|:---|:---|:---|
| 01 | [PRD & Market Analysis](./docs/01_project_overview_and_market.md) | Glossary, Personas, SWOT, Competitive Matrix, Pricing, Risk Register, GTM, Compliance | Referenced by all docs |
| 02 | [Core Features](./docs/02_core_features.md) | Per-feature mechanics, backend logic, edge cases with tables | → 07 (Screens), 08 (Rules), 06 (APIs) |
| 03 | [Technical Architecture](./docs/03_technical_architecture.md) | AWS Topology, 16 DB Tables, 39 API Routes, Service Catalog, Security | → 08 (State Machines), 10 (NFRs) |
| 04 | [User Stories](./docs/04_user_stories.md) | 6 Epics, Given/When/Then ACs, error paths, sprint assignments | → 07 (Screens), 08 (Rules), 09 (Notifications) |
| 05 | [Project Roadmap](./docs/05_project_roadmap.md) | Gantt Chart, 12 Sprint task tables with owners and DoD | → 04 (Stories), 07 (Screens), 10 (NFRs) |
| 06 | [AI & API Integrations](./docs/06_ai_and_integrations.md) | RAG Pipeline, Prompt Templates, Stealth Config, API Payloads, Cost Model | → 02 (Features), 03 (Services), 09 (Notifications) |
| 07 | [Screen Specifications](./docs/07_screen_specifications.md) | 15 screens, every field, validation, empty/loading/error state | → 03 (API Routes), 04 (Stories) |
| 08 | [Business Rules & RBAC](./docs/08_business_rules_and_rbac.md) | RBAC Matrix, State Machines (Mermaid), Financial Rules, Outreach Safety, Data Retention | → 02 (Features), 03 (Schema), 04 (Stories) |
| 09 | [Notifications & Emails](./docs/09_notifications_and_emails.md) | Channel Matrix, Email Templates, Push Notification Payloads | → 04 (Story triggers), 06 (API webhooks) |
| 10 | [NFRs & Compliance](./docs/10_nfr_and_compliance.md) | Performance SLAs, Security, Observability, Accessibility, Compatibility | → 03 (Architecture), 05 (Sprint DoD) |
| 11 | [Developer Operations](./docs/11_developer_operations.md) | Env Variables, Cron Jobs, WebSocket Events, Error Codes, Redis Keys, CI/CD, Deep Links | → All docs |

## How to Read These Docs
1. **Start with [01 — PRD](./docs/01_project_overview_and_market.md)** to understand the market, personas, and strategy.
2. **Read [02 — Features](./docs/02_core_features.md)** to understand what the platform does.
3. **Read [03 — Architecture](./docs/03_technical_architecture.md)** to understand how it's built.
4. **Read [04 — Stories](./docs/04_user_stories.md)** to understand the exact behavioral requirements.
5. **Read [05 — Roadmap](./docs/05_project_roadmap.md)** to see the execution plan.
6. **Reference [06](./docs/06_ai_and_integrations.md)–[10](./docs/10_nfr_and_compliance.md)** as deep-dive annexes during development.
7. **Use [11 — Developer Operations](./docs/11_developer_operations.md)** as your daily reference for env vars, cron schedules, error codes, and deployment.

## Quick Stats
| Metric | Count |
|:---|:---:|
| Documentation Files | 11 |
| Database Tables | 16 |
| API Routes | 39 |
| UI Screens | 15 |
| User Story Epics | 6 |
| User Stories | 12 |
| State Machine States (Collab) | 17 |
| Business Rules | 20 |
| Notification Events | 19 |
| Cron Jobs | 12 |
| WebSocket Events | 7 |
| Error Codes | 20+ |
| Environment Variables | 35+ |
| Redis Key Patterns | 10 |
