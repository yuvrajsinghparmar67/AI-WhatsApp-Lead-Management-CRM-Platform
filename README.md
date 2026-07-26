# AI WhatsApp Lead Management & CRM


---

## Project Overview

Businesses receive far more customer messages than they can manage manually.
This platform combines a CRM, a WhatsApp-style inbox, an Admin Portal, and an
AI pipeline (Gemini 3.5 Flash + Gemini Embedding 2) so that every incoming
message is automatically triaged, every lead is automatically scored, every
agent gets AI-suggested replies grounded in real business knowledge (RAG),
and every business fact the AI relies on is something an admin actually
configured — not something the model invented.

## 📸 Screenshots

<table>
  <tr>
    <td align="center">
      <img src="Screenshot%20(244).png" width="420"><br>
      <b>Sign Up Page</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(245).png" width="420"><br>
      <b>Admin Inbox page</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(246).png" width="420"><br>
      <b>Lead Pipeline</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(247).png" width="420"><br>
      <b>Analytics 1</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(248).png" width="420"><br>
      <b>Analytics 2</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(249).png" width="420"><br>
      <b>Business Info 1</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(250).png" width="420"><br>
      <b>Business Info 2</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(251).png" width="420"><br>
      <b>Adding Product or Service</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(252).png" width="420"><br>
      <b>Knowledge Base and Documents</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(253).png" width="420"><br>
      <b>Team Members and Roles Page</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(254).png" width="420"><br>
      <b>FAQ Page</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(255).png" width="420"><br>
      <b>Business Rules</b>
    </td>
  </tr>

  <tr>
    <td align="center">
      <img src="Screenshot%20(256).png" width="420"><br>
      <b>AI Settings</b>
    </td>
    <td align="center">
      <img src="Screenshot%20(257).png" width="420"><br>
      <b>Follow Up Rules</b>
    </td>
  </tr>
</table>



## The message pipeline

Customer messages never go directly to Gemini. Every inbound message passes through:

```
Customer → Messaging Layer → Lead Management → Knowledge Retrieval →
Business Rules → Gemini 3.5 Flash → Reply Generation → CRM Update →
Analytics → Dashboard
```

| Stage | Where it lives | Status |
|---|---|---|
| Messaging Layer | `messaging/` — `MessagingProvider` / `SimulatedWhatsAppProvider` | ✅ |
| Lead Management | `services/contact_service.py`, `conversation_service.py` | ✅ |
| Knowledge Retrieval | `ai/retrieval/` — searches past conversations *and* the knowledge base/company profile | ✅ |
| **Business Rules** | `services/business_rule_service.py` + `models/business_rule.py` | guardrails (mandatory constraints injected into every suggested reply) and automation rules (deterministic overrides applied after AI analysis, admin's rule always wins) |
| Gemini 3.5 Flash | `ai/providers/gemini_provider.py` | ✅ |
| Reply Generation | `services/ai_pipeline_service.py` | ✅ |
| CRM Update | writes to `Contact` / `Conversation` | ✅ |
| Analytics | `services/analytics_service.py` | ✅ |
| Dashboard | `/analytics` | ✅ |

## Admin Portal roadmap

The Admin Portal (`/admin`) is built to show its real, honest shape: all
areas are visible in the nav; built ones are clickable, areas that already
exist elsewhere in the app link out instead of duplicating that UI, and
everything else is clearly marked "coming in a later milestone" rather than
hidden.

| Area | Status |
|---|---|
| Business Information |  ✅ 
| Knowledge Base & Documents |  ✅ 
| Products, Services & Pricing |  ✅ 
| FAQs |  ✅ 
| Business Rules | ✅ 
| AI Settings + Prompt Settings | ✅ 
| Team Members + Roles & Permissions |  ✅ 
| Follow-up Rules |  ✅ 
| Customer Database enhancements |  ✅ 
| Lead Pipeline |  ✅ 
| Analytics |  ✅ 

## Features

**Implemented so far:**
- Production-grade project architecture (backend + frontend + DB, cleanly separated)
- FastAPI backend with JWT auth (register/login), health check, PostgreSQL via SQLAlchemy, Alembic migrations wired up — Milestone 1
- Abstract `MessagingProvider` interface with a working `SimulatedWhatsAppProvider`, and an abstract `AIProvider` interface with a working `GeminiProvider` 
- Dedicated `ai/prompts/` folder — no prompt is ever hardcoded in a route 
- Core CRM data layer: Contacts, Conversations, Messages with real REST endpoints and a service layer 
- A `/simulate/inbound` endpoint standing in for a real WhatsApp webhook — lets the whole pipeline (contact creation → conversation → message) be exercised without WhatsApp Business API credentials 
- A real, WhatsApp-style inbox UI: conversation list with live previews, a message thread with bubbles, a reply composer, and a "Simulate incoming message" panel so the demo is self-contained 
- Initial Alembic migration for all four tables
- **AI analysis pipeline**: every inbound message (real or simulated) triggers a single structured Gemini call that infers intent, lead status, priority, sentiment, estimated budget, a confidence score, and a running summary — written straight onto the Contact/Conversation rows 
- **AI Insights panel** in the inbox: shows the live summary, intent, sentiment, estimated budget, and confidence for the open conversation 
- **On-demand suggested replies**: a sparkle button in the composer drafts a reply grounded in the conversation transcript, which the agent can edit before sending — kept on-demand rather than automatic to keep AI usage proportional to actual need 
- The AI pipeline fails soft: a missing `GEMINI_API_KEY` or a provider outage never blocks a message from being saved — it just leaves the AI fields stale until the next successful analysis
- **Semantic search & RAG (Gemini Embedding 2)**: every inbound message is embedded and stored; agents can run an on-demand "Find similar conversations" search from the AI Insights panel, and Suggested Replies are automatically grounded in similar past conversations when relevant, with the UI showing how many were used 
- **Lead pipeline board** at `/contacts`: every contact grouped into draggable Kanban columns (New/Qualified/Nurturing/Won/Lost) by their AI-assigned `lead_status`. Dragging a card PATCHes a manual override that sticks until the next AI analysis pass. Clicking a card opens a detail drawer (priority, sentiment, estimated budget, AI confidence) with a deep link straight back to that contact's inbox conversation 
- **Analytics dashboard** at `/analytics`: total contacts/conversations, average first-response time, lead funnel, priority and sentiment breakdowns, and a 14-day inbound-vs-outbound message volume trend — all from one aggregate `GET /analytics/overview` call, rendered with hand-rolled, dependency-free bar/line charts
- **Auth is now real end-to-end**: `/contacts`, `/conversations`, and `/analytics` require a valid JWT (`GET /auth/me` resolves the logged-in agent); the frontend has Login/Register screens (React Hook Form) and every app route is behind `ProtectedRoute`, which redirects to `/login` if there's no session and again if a token expires mid-session. The sidebar shows the logged-in agent with a logout control. `/simulate/inbound` deliberately stays open, since in production it would be a WhatsApp webhook authenticated by Meta's own signature/verify-token scheme, not an agent's login 
- **Deployment**: multi-stage Dockerfiles for both backend (FastAPI/uvicorn) and frontend (Vite build served by nginx, with SPA fallback routing), a full-stack `docker-compose.yml` (db + backend + frontend), and a GitHub Actions CI pipeline that runs backend unit tests, builds the frontend production bundle, and builds both Docker images on every push/PR
- A small backend unit test suite (`backend/tests/`) covering password hashing/JWT round-trips, cosine similarity edge cases, and the tolerant AI-JSON parser — the first tests in the project, added specifically so CI has something real to run
- **Admin Portal** at `/admin`, with a nav covering all 16 planned areas (see roadmap above)
- **Business Information**: admin-editable business name, address, phone, email, website, and a structured 7-day business hours editor. This is fed directly into the AI's suggested-reply prompt as an always-available, authoritative context block — closing the gap where the AI previously had no way to correctly answer "what are your hours"
- **Knowledge Base & Documents**: admins can type in structured entries (e.g. a pricing plan) or upload PDF/DOCX/TXT files. Uploads are parsed (`pypdf`, `python-docx`), split into overlapping chunks, and each chunk is embedded (Gemini Embedding 2) — the same chunking-for-RAG pattern used for messages, just applied to company facts. Suggested replies now search this knowledge base and can answer pricing/policy questions confidently when a relevant chunk exists, while a separate "similar past conversations" block stays supplementary/tone-only
- Knowledge base uploads deliberately do NOT fail soft (unlike the message pipeline): if embedding a document fails, the admin gets an error, not a silently-broken, unsearchable document
- **Products, Services & Pricing** at `/admin`: a single structured catalog (not three separate list pages — pricing without an item, or an item without a price, isn't a distinct thing worth its own screen). Each item (name, type, price, currency, billing period, description, features) is re-embedded on every save, so a suggested reply answering "how much is X" always reflects the current price, not a stale one. Inactive items are excluded from what the AI can retrieve
- **FAQs** at `/admin`: structured question/answer pairs, kept separate from the free-form knowledge base since an FAQ is a deliberate, complete unit (a specific question the business has chosen a specific answer for), not an arbitrary document slice. Embedded from question+answer together, so semantic search matches however a customer actually phrases it, not just the admin's exact wording — the suggested-reply prompt now has five context tiers total 
- **Business Rules** at `/admin` — the pipeline stage that was previously missing, now built as two things: **guardrails** (free-text mandatory constraints, e.g. "never promise refunds," injected into every suggested reply as the highest-priority instruction — explicitly told to override even the customer's own request if they conflict) and **automation rules** (structured if/then conditions on the AI's own analysis fields, e.g. "if sentiment is negative → set priority to urgent," applied deterministically right after AI analysis so an admin's explicit policy always wins over the AI's own guess for that field). Both are wired into the actual pipeline, not just displayed in the UI
- **AI Settings** at `/admin`: chat model name and temperature are now runtime-configurable (no redeploy) and actually flow into every Gemini call; an **auto-analysis toggle** lets an admin pause automatic lead scoring entirely; a **RAG toggle** lets an admin turn off catalog/FAQ/knowledge-base/similar-conversation retrieval for suggested replies while keeping business rules and the company profile active (those are direct lookups, not retrieval). The embedding model is deliberately NOT exposed as editable — swapping it would silently break semantic search for every existing embedding until a full re-embed, which is a real migration, not a settings toggle 
- **Prompt Settings** at `/admin`: the actual system prompts the pipeline runs (Conversation Analysis, Suggested Reply) are now admin-editable with one-click reset to the code default. An explicit warning is shown for the Conversation Analysis prompt, since it drives automatic lead scoring and must keep instructing the model to return the documented JSON shape — editing that away fails soft (nothing crashes) but silently stops lead scoring from updating 
- **Team Members & Roles** at `/admin` — two fixed roles (`admin`, `agent`), and this is where the security model actually changes: every Admin Portal endpoint now requires `role == "admin"` server-side (a new `require_admin` dependency, returning 403 for a logged-in-but-unauthorized agent, distinct from 401 for not-logged-in-at-all). Agents keep full access to Inbox/Contacts/Analytics — the normal CRM workflow — but the Admin Portal nav item is hidden for them, and the route itself shows a clear "admin access required" message rather than broken panels if visited directly. The first account ever registered automatically becomes admin; every account after that starts as an agent until promoted. An admin can't demote or deactivate their own account (enforced server-side, not just in the UI) — the one CRM-specific safety rule this needed. "Roles & Permissions" was requested as a separate area but is the same screen: two fixed roles, not a configurable permission matrix, so assigning a role here IS the permissions system 
- **Follow-up Rules** at `/admin` — the first *time-based* pipeline stage: every other stage reacts to an inbound message, this one reacts to silence. An admin defines a rule (idle hours threshold, optional lead-status filter, message template with a `{display_name}` placeholder), and a new in-process **scheduler** (APScheduler's `AsyncIOScheduler`, started/stopped via a FastAPI `lifespan` handler — see `app/scheduler/`) checks every open conversation on a fixed interval. A conversation is "due" when its last message is inbound (still unanswered), idle longer than the rule's threshold, and the contact isn't already Won/Lost. Each send writes a `FollowUpLog` row, which both drives the admin's "recent activity" feed and prevents the same rule from messaging the same conversation twice for one quiet period. A **"Run now"** button lets an admin fire the check on demand instead of waiting for the scheduler's next tick — useful for demos and for verifying a new rule immediately
- **Customer Database enhancements** on the existing Lead Pipeline/Contacts screen (`/contacts`) — a search box (name or phone, debounced client-side so it doesn't hit the API on every keystroke) plus priority and sentiment filters, all applied server-side via new query params on `GET /contacts`. Lead status isn't a filter here — the Kanban columns already segment by status, so filtering by it too would be redundant. A **CSV export** button downloads exactly what's currently filtered (name, phone, lead status, priority, sentiment, estimated budget, confidence score, timestamps) via a new `GET /contacts/export` endpoint — since the JWT lives in `localStorage` rather than a cookie, the download goes through an authenticated `fetch` → `Blob` → object URL rather than a plain link, so it works the same way every other authenticated request in this app already does 

**Known limitations / natural next steps** (honest, not hidden):
- Search/filter/export on the Customer Database load the full matching result set in one request — fine at demo scale, but a real deployment with thousands of contacts would want pagination on `GET /contacts` (and probably a background-generated export for very large CSVs) rather than returning everything at once.
- The CSV export is a synchronous request-response — it builds the whole file in memory and streams it back in one call. That's fine for hundreds or low thousands of contacts; a much larger database would want to generate the export as a background job and let the admin download it when ready, rather than holding the HTTP request open.
- The scheduler runs in-process inside the single backend instance (APScheduler's `AsyncIOScheduler`, started in `main.py`'s `lifespan`) — fine at one replica, but two backend instances would both run the same job and could double-send a follow-up right at the edge of the dedup window. A multi-instance deployment would want to move this to an external scheduler (e.g. Celery beat, or plain cron) hitting a dedicated endpoint, so only one process ever fires a given tick.
- Follow-up messages are plain templates with a single `{display_name}` placeholder — they're not AI-generated and don't read the conversation transcript the way a suggested reply does. Grounding the follow-up text in the actual conversation (like Suggested Replies do) is the natural next step once this needs to feel less like a form letter.
- A rule can only be scoped by idle hours and lead status — there's no way yet to exclude a specific contact, cap how many follow-ups a contact can receive in total, or stop the sequence once a human agent has looked at the conversation (even without replying).
- There's no invite-only signup — registration is still open to anyone with the URL, and new accounts self-serve in as an agent. A real deployment handling actual customer data would want to close registration or require an invite token/admin approval before going live; this wasn't built because there's no email-sending infrastructure in the project yet to make invites practical.
- Automation rules only trigger off the AI's own analysis fields (intent/sentiment/priority) run on inbound messages — they still don't share a rule engine with Follow-up Rules' time-based trigger; unifying the two into one rules system is a reasonable future consolidation.
- Guardrails are prompt-level instructions, not hard-enforced filters — a sufficiently unusual customer message could still, in principle, get the model to bend a rule. A production system handling something high-stakes (e.g. real financial/legal commitments) would want a second pass validating the AI's output against the rules, not just instructing it upfront.
- Prompt Settings has no version history or diff view — saving overwrites the previous custom text with no way to see what changed or roll back to a specific prior edit (only reset-to-code-default, which loses any custom edit entirely)
- Moving AI analysis to a background task/queue instead of the current synchronous call, once message volume matters
- Swapping the brute-force Python cosine-similarity search for pgvector's indexed ANN search once conversation volume is large enough for it to matter
- Pushing the analytics aggregation queries into SQL window functions / a materialized view once message volume makes the current in-Python approach slow
- Test coverage is intentionally minimal (pure unit tests only) — no integration tests against a real database or end-to-end tests against the API/UI yet
- Migrations run as a manual deploy step (`alembic upgrade head`), not automatically on container start, to avoid multiple replicas racing to migrate the same database — fine for one backend instance, worth revisiting (e.g. a dedicated migration job) before scaling to several
- No rate limiting, request logging middleware, or error tracking (Sentry, etc.) wired in yet

## Architecture

```
                     ┌────────────────────┐
                     │   React Frontend    │
                     │ (Vite + Tailwind)   │
                     └─────────┬───────────┘
                               │ REST (JWT)
                     ┌─────────▼───────────┐
                     │   FastAPI Backend    │
                     │  api / services layer│
                     └───┬───────────┬──────┘
                         │           │
              ┌──────────▼──┐   ┌────▼─────────────┐
              │ AIProvider   │   │ MessagingProvider │
              │ (interface)  │   │ (interface)        │
              └──────┬───────┘   └────────┬───────────┘
                     │                    │
            ┌────────▼────────┐  ┌────────▼─────────────┐
            │ GeminiProvider   │  │ SimulatedWhatsApp     │
            │ (Gemini 3.5      │  │ Provider (WhatsApp    │
            │ Flash + Embed 2) │  │ Business API later)   │
            └──────────────────┘  └───────────────────────┘

                     ┌────────────────────┐
                     │     PostgreSQL      │
                     └────────────────────┘
```

Both the AI backend and the messaging channel sit behind abstract interfaces
(`AIProvider`, `MessagingProvider`). Business logic and API routes depend only
on those interfaces — swapping Gemini for another model, or the simulator for
the real WhatsApp Business API, means adding one new class and flipping a
config value, not rewriting the CRM.

## Folder Structure

```
whatsapp-crm-ai/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI entrypoint
│   │   ├── core/                  # config, logging, security (JWT/hashing)
│   │   ├── db/                    # SQLAlchemy base + session
│   │   ├── models/                # ORM models (User, Contact, Conversation, Message, BusinessRule, FollowUpRule, FollowUpLog, ...)
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   ├── api/v1/endpoints/      # health, auth (incl. /me), contacts, conversations, simulator, analytics, users — plus company, knowledge_base, catalog, faq, business_rules, follow_up_rules, ai_settings, prompt_settings (all admin-only via require_admin). health/auth/simulator are open; contacts/conversations/analytics require any logged-in user.
│   │   ├── services/               # contact_service, conversation_service, messaging_service, ai_pipeline_service, analytics_service, company_service, knowledge_base_service, catalog_service, faq_service, business_rule_service, follow_up_rule_service, ai_settings_service, prompt_settings_service, user_service
│   │   ├── scheduler/              # APScheduler wiring (setup.py) + the recurring job body (jobs.py) - runs Follow-up Rules on a timer, started/stopped via main.py's lifespan handler
│   │   ├── knowledge_base/         # parsers.py (PDF/DOCX/TXT text extraction), chunking.py (splits text for embedding)
│   │   ├── ai/
│   │   │   ├── providers/         # AIProvider interface + GeminiProvider + factory
│   │   │   ├── prompts/           # intent_detection, conversation_analysis, suggested_reply — every prompt lives here, never in routes
│   │   │   ├── schemas.py         # Pydantic model the AI's JSON response is parsed into
│   │   │   ├── utils.py           # tolerant JSON parsing for AI responses
│   │   │   ├── embeddings/        # embed_text() - wraps AIProvider.generate_embedding
│   │   │   └── retrieval/         # cosine similarity + semantic search over embedded messages (RAG)
│   │   └── messaging/             # MessagingProvider interface + SimulatedWhatsAppProvider
│   ├── alembic/                    # DB migrations
│   ├── tests/                      # pytest unit tests (security, similarity, AI JSON parsing, follow-up rule matching, CSV export)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── context/               # AuthContext - session state, login/logout
│   │   ├── components/auth/       # ProtectedRoute
│   │   ├── components/ui/         # base UI primitives (Button, Badge, Avatar, ...)
│   │   ├── components/layout/     # Layout, Sidebar, ThemeToggle
│   │   ├── features/inbox/        # inbox feature: components/ + hooks/ (conversations, messages)
│   │   ├── features/pipeline/     # lead pipeline board: Kanban columns, drag-and-drop, contact drawer
│   │   ├── features/analytics/    # analytics dashboard: hooks + hand-rolled bar/line chart components
│   │   ├── features/admin/        # Admin Portal: nav, Business Info, Catalog, FAQs, Knowledge Base, Business Rules, Follow-up Rules, AI Settings, Prompt Settings, Team Members panels
│   │   ├── pages/                 # route-level screens (Login, Register, Inbox, Contacts, Analytics, Admin, SystemStatus)
│   │   ├── routes/                # route table
│   │   ├── hooks/                 # app-wide custom hooks (useDarkMode, useDebouncedValue, ...)
│   │   ├── lib/                   # api client, formatting utils
│   │   └── styles/                # Tailwind entrypoint + design tokens
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── .env.example
├── .github/workflows/ci.yml        # backend tests + frontend build + Docker image builds
├── docker-compose.yml              # full stack: db + backend + frontend
└── README.md
```

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for PostgreSQL) — or a local PostgreSQL instance

### 1. Start the database
```bash
docker compose up -d
```

### 2. Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in SECRET_KEY and GEMINI_API_KEY
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000` — interactive docs at `http://localhost:8000/docs`.

### 3. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Frontend runs at `http://localhost:5173`.

## Testing This Milestone

1. `docker compose up -d`, then in `backend/`: `uvicorn app.main:app --reload` (no new migration or dependency this milestone — Customer Database enhancements only add query params and a new route on top of the existing `contacts` table); `npm run dev` in `frontend/`.
2. Go to **Contacts** (`/contacts`, also linked from Admin Portal → Customer Database). With several contacts across different names/phone numbers/priorities/sentiments (simulate a few inbound conversations first if your database is empty), type part of a name or phone number into the search box — the board should narrow to matching contacts only, and typing shouldn't fire a request on every keystroke (check the Network tab: requests should wait until you pause typing).
3. Use the **priority** and **sentiment** dropdowns, alone and combined with the search box — the board (and each column's count) should reflect the combined filter. Clear filters with the **Clear filters** link and confirm everything comes back.
4. Click **Export CSV** with no filters applied — a file named `contacts-<timestamp>.csv` should download containing every contact; open it and confirm the columns (Name, Phone Number, Lead Status, Priority, Sentiment, Estimated Budget, Confidence Score, Created At, Updated At) and row count match what's in the database.
5. Apply a search term and/or a priority/sentiment filter, then click **Export CSV** again — the downloaded file should contain only the filtered contacts, not the full list.
6. Confirm drag-and-drop between pipeline columns still works exactly as before, and still works while a filter is active (dragging a filtered-in card to a new column should update it normally).
7. Log out and hit `GET /api/v1/contacts/export` directly (e.g. `curl` with no `Authorization` header) — it should 401, the same as every other Contacts endpoint; the export isn't a public link.
8. Everything from Milestones 1-15 still works unchanged.

Running everything natively (via `uvicorn --reload` and `npm run dev`) or via `docker compose up --build` both still work as described in Milestone 8.

## Environment Variables

**Backend (`backend/.env`)**

| Variable | Description |
|---|---|
| `SECRET_KEY` | Random secret used to sign JWTs |
| `DATABASE_URL` | PostgreSQL connection string |
| `AI_PROVIDER` | Which `AIProvider` implementation to use (`gemini`) |
| `GEMINI_API_KEY` | Google GenAI API key |
| `GEMINI_CHAT_MODEL` / `GEMINI_EMBEDDING_MODEL` | Model names |
| `MESSAGING_PROVIDER` | Which `MessagingProvider` implementation to use (`simulated`) |
| `FOLLOW_UP_SCHEDULER_ENABLED` | Whether the Follow-up Rules background scheduler runs at all (`true`/`false`) |
| `FOLLOW_UP_SCHEDULER_INTERVAL_MINUTES` | How often the scheduler checks conversations for due follow-ups |
| `CORS_ORIGINS` | Comma-separated allowed origins for the frontend |

**Frontend (`frontend/.env`)**

| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the backend API |

## Deployment

### Run the whole stack in Docker

```bash
cp backend/.env.example backend/.env    # fill in SECRET_KEY and GEMINI_API_KEY
docker compose up --build
```
This builds and runs `db` + `backend` + `frontend` together. Backend: `http://localhost:8000`. Frontend: `http://localhost:5173`. Then run migrations once against the running database:
```bash
docker compose exec backend alembic upgrade head
```

### Deploying to a real host

The two Dockerfiles (`backend/Dockerfile`, `frontend/Dockerfile`) are host-agnostic — they'll work as-is on Render, Railway, Fly.io, ECS, or any platform that builds from a Dockerfile. In outline:

1. Provision a managed PostgreSQL instance and set `DATABASE_URL` on the backend service to point at it.
2. Deploy `backend/Dockerfile` as a web service; set `SECRET_KEY`, `GEMINI_API_KEY`, and `CORS_ORIGINS` (your deployed frontend's URL) as environment variables. Set `DEBUG=false`.
3. Run `alembic upgrade head` against the production database as a one-off release step (most platforms have a "release command" or "pre-deploy command" hook for exactly this) — deliberately not baked into the container's own startup, to avoid multiple replicas racing to migrate at once.
4. Deploy `frontend/Dockerfile`, passing `--build-arg VITE_API_BASE_URL=https://your-backend-domain/api/v1` at build time (Vite bakes this into the static bundle, so it can't be an ordinary runtime env var).

### CI

`.github/workflows/ci.yml` runs on every push/PR to `main`: backend unit tests (`pytest`), a real frontend production build (`npm run build`) — the first time this project's frontend is actually compiled rather than just hand-reviewed — and a build of both Docker images, so a broken Dockerfile or build step fails CI before it fails a deploy.

## Future Improvements

All 8 planned milestones are complete: architecture → core CRM/inbox → AI
pipeline → semantic search/RAG → lead pipeline board → analytics → auth →
deployment. The Admin Portal's own 8-milestone roadmap (Milestones 9-16)
is also complete, ending with Follow-up Rules' scheduler and Customer
Database search/filter/export — all 16 milestones total. See "Known
limitations / natural next steps" under Features above for the honest
list of what a real production hardening pass would tackle next
(background AI processing, pgvector, broader test coverage,
observability, pagination at scale).

## License

MIT
