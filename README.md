# AI Personal Content Waterfall

> 🚧 **WORK IN PROGRESS — early scaffold, everything is subject to change.**
> The app itself is **not built yet**. Treat file contents as drafts to build on, not
> settled decisions. The one logged decision (`rag_decision.md`) is still **pending team
> ratification**. Nothing here is final.

An AI-powered content generator: turn a single source document into platform-specific posts
(blog, LinkedIn, Instagram) while preserving a chosen communication style. Gradio + OpenAI,
built as a 2-day bootcamp MVP.

## Current status

| Area | State | Owner |
|---|---|---|
| RAG research & decision (`rag_decision.md`) | Draft — **pending team ratification** | Ugo → team |
| Prompt builders (`prompts.py`) | Working, smoke-tested | Ugo |
| Profile loader (`profile_loader.py`) | Working, smoke-tested | Ugo |
| Communication profiles (`knowledge_base/profiles/`) | 6 draft profiles | Ugo |
| Document ingestion (`document_reader.py`) | Reused from prior project | Ugo → Maria |
| Gradio app (`app.py`), OpenAI wiring, `requirements.txt` | Not started | Maria |
| `agents.md` | Not started | Maria |
| Project docs / presentation | Tracked elsewhere | Elza |

## How the pieces fit

```
profiles/<chosen>.md ─► profile_loader.load_profile() ─┐
                                                       ├─► prompts.build_prompt(platform, profile, source) ─► OpenAI ─► blog / linkedin / instagram
uploaded file ─► document_reader.read_uploaded_file() ─┘
```

## For the team — how to work with this repo

**Maria (app development).** The building blocks below are ready to wire into `app.py` — you
shouldn't need to modify them, just call them:

```python
from profile_loader import list_profiles, load_profile   # dropdown choices + load one
from document_reader import read_uploaded_file            # Gradio upload path -> text
from prompts import build_prompt                          # -> prompt string for OpenAI

choices = list_profiles()                        # {slug: "Display Name"} for the dropdown
profile = load_profile(selected_slug)            # Markdown text of the chosen profile
source  = read_uploaded_file(uploaded_filepath)  # extracted text from PDF/DOCX/TXT
prompt  = build_prompt("linkedin", profile, source)   # platform: "blog" | "linkedin" | "instagram"
# then: client.chat.completions.create(..., messages=[{"role": "user", "content": prompt}])
```

Still to add on the app side: `requirements.txt` (gradio, openai, python-dotenv, pypdf,
python-docx), `app.py`, and OpenAI wiring. Keep your API key in a local `.env` — it's already
gitignored; never commit it.

**Elza (planning / docs / RAG decision).** `rag_decision.md` is the research write-up —
please review so we can ratify the direct-injection call together. The fuller project README
and documentation are yours to expand from this stub whenever you're ready.

**Adding or editing profiles.** Drop a new `.md` into `knowledge_base/profiles/` and the
loader picks it up automatically — no code change. Please don't rename or restructure the
existing profiles without a heads-up: the app selects them by filename slug.

**Working together (suggestion — Maria owns final repo conventions).** Small, focused commits;
a short branch per area (e.g. `app`, `docs`) with a quick PR is safest so we don't collide on
`main` during the sprint.

## Setup

```bash
pip install -r requirements.txt   # once requirements.txt is added with the app
```
