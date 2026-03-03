---
stepsCompleted: [1, 2, 3, 4, 5, 6]
status: complete
inputDocuments:
  - docs/project_idea.md
  - docs/reference-repo-mapping.md
  - docs/planning-artifacts/research/market-cobol-modernisation-agents-research-2026-03-01.md
date: 2026-03-01
author: Kamal
---

# Product Brief: Mainframe Modernisation Agents

<!-- Content will be appended sequentially through collaborative workflow steps -->

---

## Executive Summary

The Mainframe Modernisation Agents project builds the operational backbone of a dedicated modernisation factory — an AI-native internal practice that delivers COBOL modernisation as a managed service. Rather than selling software, the factory delivers outcomes through three integrated pillars: a structured repeatable process (the BMAD agent pipeline), a skilled team that operates it, and bespoke configuration for each client's unique COBOL estate. The open-source agent pipeline (Viper → Crane → Shifu) is the engine; the practice is what makes it commercially and operationally viable at scale.

---

## Core Vision

### Problem Statement

Enterprise organisations with COBOL estates face a convergence of mounting, interconnected risks: the COBOL skill cliff (retiring developers taking institutional knowledge with them permanently), escalating mainframe licensing costs, compliance and regulatory deadlines requiring changes to systems nobody fully understands, and inability to integrate legacy systems with modern cloud and AI capabilities. These risks are universally recognised but paralyse organisations — because traditional modernisation (armies of consultants, multi-year programmes, big-bang rewrites) has a 70% failure rate, and the failures are caused by one root problem: teams replace systems they don't understand, and rediscover requirements through production failures and compliance violations.

### Problem Impact

- Institutional knowledge walks out the door with every retiring COBOL developer — permanently
- Systems cannot be safely changed because nobody fully understands them end-to-end
- Modernisation attempts that skip understanding produce production failures and compliance violations
- Organisations are locked into escalating IBM mainframe licensing with no leverage or exit path
- New capabilities (cloud, AI, APIs) cannot integrate with COBOL estates without enormous, expensive effort
- The 70% historical project failure rate makes boards and risk committees deeply reluctant to approve new attempts

### Why Existing Solutions Fall Short

Commercial tools (IBM watsonx, AWS Transform, Micro Focus) are expensive, cloud-locked, and jump to code conversion without adequate understanding. Open-source alternatives (Microsoft/Bankdata) lack business rule extraction, a structured intermediate representation, and delivery integration. None of them connect analysis through to sprint delivery. None handle org-specific middleware. None produce compliance-grade audit artefacts. And critically — **none are delivered as a managed practice with human expertise wrapping the tooling.** The market offers tools; the market does not offer a factory.

### Proposed Solution — The Modernisation Factory

A modernisation factory built on three integrated pillars:

1. **Process** — Viper → Crane → Shifu → Oogway → BMAD delivery pipeline. Structured, repeatable, auditable. Enforces "understand first, convert later" as an architectural principle, not just a preference.
2. **People** — A skilled team operating the pipeline, interpreting outputs, guiding architectural decisions, and managing delivery. Human judgement wraps AI analysis at every critical decision point.
3. **Customisation** — Each client engagement configured for their specific COBOL estate: glossary mapping, middleware knowledge server (delta-macros-mcp), target language preference, GitLab integration. The customisation layer is what makes generic tooling valuable for a specific client.

Validated internally against a BlackJack COBOL program built with realistic technical debt patterns — the factory's proof-of-concept and client demonstration asset.

### Key Differentiators

- **Factory model** — the agents are the engine, not the product; what is delivered is a practice
- **"Understand first, convert later"** — structurally enforced by the pipeline; no code generation until full program understanding is documented
- **Spec layer (SQLite IR)** — the only structured bridge between analysis and implementation in the open-source space; downstream agents and architects consume structured specs, not raw markdown
- **Business rule extraction (Shifu)** — produces compliance-grade artefacts in human-readable form; regulated clients can show regulators what was found and decided
- **Middleware knowledge server (delta-macros-mcp)** — handles org-specific macros and proprietary middleware that no generic tool addresses
- **End-to-end delivery** — analysis through to GitLab epics, sprints, QA validation, and verified migration; no gap between insight and execution

---

## Target Users

### Primary Users

---

**Alex — The COBOL Factory Analyst** *(factory team, core operator)*

Alex has 15+ years of hands-on COBOL experience. He knows COBOL the way a surgeon knows anatomy — paragraph structures, REDEFINES, PERFORM nesting, DB2 call patterns, and the subtle ways CICS transactions can go wrong. He has spent significant chunks of his career manually tracing legacy programs, building mental models of systems that were never properly documented.

**Alex's problem today:** The analysis work he's exceptional at is also brutally slow, repetitive, and unscalable. Tracing a 3,000-line COBOL program's PERFORM graph manually takes days. Understanding five programs that call each other takes weeks. He can do it — but he can't do it for 200 programs in a reasonable timeframe, which is what most modernisation engagements actually require.

**How Alex uses the factory pipeline:**
- Configures the glossary for each client engagement — mapping cryptic COBOL field names to business terms he already knows from experience
- Documents client-specific Delta macros for the knowledge server
- Reviews Viper's Phase 1 static pre-pass output to validate it's correct (his COBOL expertise is the quality gate)
- Interprets AI analysis outputs in Phase 2 — where the AI is fast and broad, Alex is deep and precise
- Makes the architectural and migration order judgements that only someone with his experience can make

**Alex's "aha" moment:** Viper maps a 5,000-line program's full paragraph call graph in minutes. What Alex would have done in two days, the pipeline does in two minutes — and it's accurate enough that he's reviewing and refining rather than building from scratch.

**What makes Alex say "this is exactly what I needed":** The pipeline handles the volume problem — 200 programs becomes tractable. He stays in the expert seat, not the data-entry seat.

---

**Priya — The Enterprise Architect** *(primary output consumer, factory team or embedded in client)*

Priya is an Enterprise Architect with deep COBOL and mainframe experience. She owns the target architecture decision — Java, Python, or modernised COBOL — and the migration strategy. She needs to understand the full COBOL estate before she can design anything, and the estate is typically opaque.

**Priya's problem today:** She cannot make good architectural decisions without understanding the estate, and understanding the estate requires analysis work that's either expensive (consultants) or unavailable (the people who knew the system retired). She has produced architectures based on incomplete understanding and paid the price later.

**How Priya uses the factory pipeline:**
- Reads Viper's complexity scoring and structural analysis to understand what she's dealing with before committing to a target architecture
- Uses Crane's dependency map and migration order recommendations to sequence the programme logically
- Reads Shifu's business rules to understand what the system actually *does*, beyond its structural mechanics
- Consumes the SQLite spec layer directly to design the target service architecture — entities, operations, rules — from structured data, not raw markdown
- Works with Oogway (BMAD architect agent) to formalise the migration architecture into the delivery plan

**Priya's "aha" moment:** Seeing the Mermaid dependency graph for the whole estate — subsystems emerge, migration order becomes obvious, and she can design an architecture that follows the seam lines of the system rather than cutting across them.

---

### Secondary Users

**David — The Client Technical Leadership Sponsor** *(buyer, client-side)*

David is a CIO, Head of Architecture, or Digital Transformation Director at a client organisation. He may not be a COBOL or deep-tech expert himself — but he carries the budget, the board mandate, and the responsibility for the modernisation programme's success or failure. He has probably seen a previous modernisation attempt fail, and that failure lives in his memory.

**David's primary concerns:**
- Risk: will this disrupt production? Will we break something critical?
- Cost: what does this actually cost, and when does it pay back?
- Visibility: how do I know what's happening, and how do I report progress to the board?
- Credibility: how do I justify this to the compliance function and the audit committee?

**How David interacts with the factory:**
- Is pitched the factory as *process + people + customisation* — not a tool
- Reviews the GitLab migration status dashboard (maintained by Tigress + Monkey agents) — his progress reporting tool
- Signs off on each subsystem Epic completion after Tai Lung QA validation — the compliance gate he needs

**David's "aha" moment:** The GitLab README shows the migration status table — every COBOL program listed, complexity scored, status tracked. For the first time, he can see the entire estate and report it to the board without a weekly status call.

---

**Claire — The Business Process Validator** *(internal signoff, client-side)*

Claire is a Business Analyst, Compliance Officer, or long-tenured domain expert inside the client organisation. She has worked alongside the COBOL system for 10–20 years. She knows what it *should* do from the business side — what the overdraft rules are, what triggers a certain batch job, what the regulatory reporting logic produces — but she has never read COBOL source code.

**Claire's problem today:** When the system does something unexpected, nobody can explain it to her in business terms. When a migration is proposed, nobody can guarantee the new system will behave identically. She is the human repository of business knowledge that exists nowhere in the documentation.

**How Claire uses the factory:**
- Reviews Shifu's Business Analysis markdown — plain English descriptions of what each program does, use cases, and extracted business rules
- Validates each business rule: "Yes, that IS the overdraft calculation rule" or "No, that's missing the exception for corporate accounts"
- Signs off on the spec layer's business rules before migration begins — the compliance and correctness gate
- Her sign-off is what allows the programme to proceed with confidence that the target system will be behaviourally equivalent to the source

**Claire's "aha" moment:** Reading Shifu's output and seeing her business system described accurately in plain English — for the first time, the COBOL system has been "translated" into something she can validate and own.

---

### User Journey Map

---

### Factory Engagement Model

The factory operates on a phased engagement model designed to de-risk client commitment and build confidence through demonstrated delivery before scaling:

| Phase | Duration | Scope | Purpose |
|---|---|---|---|
| **Phase 1 — Prove** | ~6 months | 1 Epic from 1 mainframe application + full factory setup (agents configured, process documented, tools established) | Prove the model with bounded scope; build client trust; establish the customised factory for this client estate |
| **Phase 2 — Complete** | TBD per app | Full application migration (all Epics) | Deliver complete outcome; solidify learnings from Phase 1; refine factory configuration |
| **Scale — Factory Running** | Ongoing | 8–15 applications per year, depending on client budget | Repeatable factory delivery at known resource cost |

**Resource model at scale:** 3 headcount (HC) per application. At 8–15 apps/year, this gives a clear team sizing formula for client proposals.

---

### User Journey Map

| Stage | Alex (Factory Analyst) | Priya (Enterprise Architect) | David (Client Sponsor) | Claire (Business Validator) |
|---|---|---|---|---|
| **Engagement start** | Receives COBOL source files; configures glossary + macro docs | Reviews estate scope; sets target architecture goals | Approves engagement; defines programme constraints | Briefed on process; agrees to review Shifu outputs |
| **Analysis phase** | Runs Viper per file; reviews + validates AI analysis | Reads Crane dependency graph; plans migration order | Monitors GitLab status dashboard | Not yet engaged |
| **Business extraction** | Runs Shifu; reviews business markdown for accuracy | Reads spec layer; begins target architecture design | Reviews programme milestone report | Reviews and validates each business rule; signs off |
| **Architecture + delivery** | Supports Oogway configuration; answers COBOL-specific questions | Authors target architecture; Oogway formalises it | Approves architecture decision; reviews Epic plan | Confirms business rules reflected in target design |
| **Migration execution** | Supports Po (Dev) with COBOL-specific questions | Reviews Po output against spec layer | Tracks Epic progress in GitLab | Reviews QA results against original business rules |
| **Completion** | Validates Tai Lung QA results | Signs off migration architecture as complete | Closes Epic in GitLab; reports to board | Provides final business sign-off |

---

## Success Metrics

### What "Done" Looks Like — Milestone Definitions

**Internal v1 — Factory Established**
The pipeline runs end-to-end on the BlackJack COBOL test corpus: Viper → Crane → Shifu → Oogway → Tigress → Po → Tai Lung → GitLab. Analysis docs produced, spec layer populated, business markdown generated, at least one Epic created in GitLab and tracked to completion. The factory team can demonstrate the full flow live to a prospective client.

**Client Phase 1 — Prove (~6 months)**
One Epic from one mainframe application migrated end-to-end. Agents configured for the client estate (glossary loaded, delta-macros-mcp populated with client middleware). Process documented. All factory artefacts produced: Viper analysis, Crane dependency map, Shifu business markdown, spec layer, architecture decision, GitLab Epics, QA validation. Business rules signed off by client's internal validator (Claire). Epic closed in GitLab and signed off by client sponsor (David).

**Client Phase 2 — Complete**
Full application migrated. All Epics closed and verified. Learnings from Phase 1 incorporated into factory configuration. Client has a fully migrated, QA-validated, business-signed-off application and a live GitLab record of every decision made.

**Factory at Scale**
8–15 applications per year running through the factory. 3 HC per application. Repeatable engagement model with reusable factory components (agents, process docs, templates) that compress Phase 1 setup time on each new engagement.

---

### Factory Pipeline Metrics (GitLab-tracked, always live)

The operational heartbeat of the factory — what the team tracks daily, what the client sponsor sees on his dashboard without asking:

| Metric | What It Measures |
|---|---|
| **Programs analysed** | Viper + Crane complete; structural analysis and dependency map produced |
| **Business rules extracted & signed off** | Shifu output reviewed and validated by client business validator |
| **Epics created in GitLab** | Architecture complete; Tigress has structured the delivery programme |
| **Epics in progress** | Po (Dev) actively working migration stories |
| **Epics tested & signed off** | Tai Lung QA complete; client signed off on verified migration |
| **Applications fully migrated** | All Epics for an application closed, QA'd, and signed off |

---

### User Success Metrics

**Alex & Priya (factory team):**
- Time to first structural analysis for any COBOL program: target < 15 minutes (Viper Phase 1)
- AI analysis accuracy validated by COBOL expert: target > 90% on first pass — no critical misidentifications
- Programs tractably analysable per sprint: target 10–20 vs 1–2 manually — the volume problem solved
- Factory setup time per new client engagement: reduces with each engagement as factory components mature

**Claire (business validator):**
- Business rules correctly extracted on first read: target > 85% — Claire confirms without major corrections
- Time to business rule sign-off per program: 1–2 review sessions vs open-ended discovery workshops
- Zero business rules lost in migration: measured at Tai Lung QA — the compliance guarantee

**David (client sponsor):**
- GitLab dashboard live from engagement week 1 — visibility from day one, no status calls required
- Estate complexity map complete before any migration begins — informed programme commitment
- Board-level progress report available at any time: X of Y programs complete, Z in progress, W signed off

---

### Client Pitch Metrics (the "before/after" story for David)

| What David Cares About | Traditional Approach | Modernisation Factory |
|---|---|---|
| **Time to understand one COBOL program** | Days to weeks (manual expert analysis) | Hours (Viper + Crane + expert review) |
| **Time to extract business rules** | Weeks of workshops, often incomplete | Days (Shifu output + 1–2 Claire validation sessions) |
| **Estate visibility** | Spreadsheet, always out of date | Live GitLab dashboard, always current |
| **Business rules documented & signed off** | Rarely done; rediscovered via production failures | Explicitly captured, validated, in spec layer |
| **Migration status at any moment** | Weekly status call with the project manager | GitLab: X of Y epics complete, Z in progress, W signed off |
| **Compliance evidence** | Custom artefacts built per audit request | Shifu business markdown exists from day one — it is the audit artefact |
| **Engagement entry point** | Multi-year contract, full estate commitment | Phase 1: 1 Epic, 6 months — bounded risk, proven value before scaling |
| **Scale** | Grow consultant team linearly | 3 HC per app, 8–15 apps/year — predictable resource model |

---

### Business Objectives

| Horizon | Objective |
|---|---|
| **3 months** | BlackJack pipeline end-to-end complete; factory team can demo live to a prospect |
| **6 months** | First client Phase 1 engagement active; 1 Epic migrated, signed off, tracked in GitLab |
| **12 months** | Phase 1 + Phase 2 complete for first client; second engagement initiated; engagement model documented and repeatable |
| **2+ years** | Factory running at 8–15 applications/year; recognised modernisation practice with reference clients and real delivery metrics |

---

## MVP Scope

### MVP Definition — BlackJack End-to-End

**The MVP is the complete factory pipeline running end-to-end on the BlackJack COBOL application.**

BlackJack corpus:
- 8 COBOL modules (`.cbl`)
- 3 copybooks (`.cpy`)
- < 1,500 lines of code total
- Mimicked technical debts: realistic patterns (GOTOs, nested PERFORMs, REDEFINES, legacy I/O) that exercise the pipeline's handling of real-world complexity

Success = every agent in the pipeline produces its correct output and the full chain completes from raw COBOL → verified migrated code → GitLab Epics closed.

---

### Core Features (MVP — must work)

**Infrastructure**
- `delta-macros-mcp` server: loads macro markdown files, exposes `get_macro`, `search_macros`, `list_categories` tools; callable by any agent
- SQLite database: all core tables + spec layer tables initialised and populated through the pipeline run
- Glossary: manually configured for BlackJack (maps field names to business terms)

**Viper — COBOL Structural Analyst** *(per module, parallelisable)*
- Phase 1 static pre-pass: IDENTIFICATION/DATA/PROCEDURE DIVISION parsing, paragraph call graph, COPY/CALL/SQL/CICS/delta-macro extraction, complexity scoring (Low/Medium/High), semantic cluster formation
- Phase 2 AI analysis per cluster: plain-English description, data transformations, business rules in conditionals, anti-pattern flagging
- Output: analysis markdown per module + SQLite records

**Crane — Dependency Mapper** *(across all 8 modules)*
- Step 1 regex extraction: COPY/CALL/SQL/CICS/file operations across all modules; deduplication
- Step 2 AI analysis: circular dependencies, dead code, subsystem groupings, migration order recommendation
- Output: Mermaid dependency graph + dependency markdown + SQLite `dependencies` + `metrics` tables

**Shifu — Business Logic Extractor** *(per module)*
- Consumes Viper + Crane outputs
- Business markdown: purpose, use cases, business rules, data entities (with glossary business names)
- Spec layer population: all 8 `spec_*` SQLite tables written
- Output: business markdown per module + fully populated spec layer

**Oogway — Migration Architect** *(existing BMAD agent)*
- Consumes spec layer; produces target architecture and migration strategy
- One target language for MVP (Java or Python — TBD per team preference)

**Tigress — PM** *(existing BMAD agent)*
- Creates GitLab Epics (one per subsystem) and Issues (one per module) with complexity/type labels
- Updates GitLab README with live migration status table

**Po — Dev** *(existing BMAD agent)*
- Consumes spec layer + Oogway architecture; generates target-language code per module

**Tai Lung — QA** *(existing BMAD agent)*
- Validates generated code against original behaviour and Shifu business rules
- Signs off each Epic; triggers Epic completion review in GitLab

**Monkey — SM** *(existing BMAD agent)*
- Sprint planning and GitLab Milestone tracking

---

### Out of Scope for MVP

| Feature | Rationale | When |
|---|---|---|
| Multi-language target output | One target language for MVP | Phase 2 |
| JCL context analysis | No JCL in BlackJack corpus | Client Phase 1 if needed |
| Automated glossary generation | Manual glossary sufficient for BlackJack | Future |
| Parallel Viper processing at scale | 8 modules runs fine sequentially | Scale phase |
| Client onboarding documentation | Factory must work before we document how to sell it | Post-MVP |
| Custom web dashboard / UI | GitLab is the dashboard for MVP | Future |
| Behavioural equivalence formal proof | Tai Lung validates behaviour; formal proof framework deferred | Future |
| Multi-client simultaneous engagements | Single pipeline focus for MVP | Scale phase |
| JIRA / Azure DevOps integration | GitLab only for MVP | Future per client need |

---

### MVP Success Criteria

The MVP is complete when all of the following are true:

- [ ] All 8 BlackJack modules have Viper analysis docs (markdown + SQLite)
- [ ] Crane produces the full dependency graph with Mermaid diagram and migration order
- [ ] All 8 modules have Shifu business markdown with extracted business rules
- [ ] SQLite spec layer fully populated (all `spec_*` tables have data)
- [ ] Oogway has produced a target migration architecture document
- [ ] GitLab: Epics created, Issues labelled, README shows migration status table
- [ ] Po has generated target-language code for all 8 modules
- [ ] Tai Lung has validated each module and signed off each Epic
- [ ] Full pipeline can be demonstrated live — COBOL input to GitLab Epic closed in a single session

---

### Future Vision

**Near-term (post-MVP, client Phase 1 ready):**
- Second target language support
- JCL context analysis for clients with job stream dependencies
- Client engagement playbook: onboarding guide, glossary template, delta macro doc template
- Parallel Viper processing for larger estates
- Automated complexity-based sprint sizing

**Medium-term (factory at scale):**
- AI-assisted glossary suggestion — Viper proposes business name mappings, Alex confirms
- Behavioural equivalence testing framework in Tai Lung — the compliance differentiator for regulated industries
- Factory metrics dashboard — aggregated view across all client engagements
- JIRA / Azure DevOps integration for clients not on GitLab

**Long-term (factory as platform):**
- BMAD mainframe modernisation expansion pack — contribute agents back to BMAD ecosystem
- RPG, PL/I support alongside COBOL — wider legacy language coverage
- Multi-cloud pipeline configuration for clients with data residency requirements
- Factory-as-a-Service — multiple simultaneous client estates with isolation
