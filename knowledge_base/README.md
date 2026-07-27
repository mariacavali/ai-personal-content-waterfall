# Knowledge Base

Ugo's deliverable: knowledge-base preparation.

The app combines **two** knowledge sources for every generation. Per `rag_decision.md`,
both are injected **directly into the prompt** (direct context injection) — no vector
store, no retrieval.

## 1. Primary KB — Communication Profile

Defines **how** generated content should be written: writing style, tone, audience,
example content, and messaging priorities. Small, stable, and loaded from a local file.

- `communication_profile.md` — a fill-in **template** documenting the profile structure.
- `profiles/` — a curated library of **ready-to-use representative profiles**
  (founder, consultant, nonprofit, researcher, public affairs, populist political, beauty &
  lifestyle creator). The populist and beauty-creator profiles are generic *style* archetypes,
  not models of any real person. The user picks one at
  runtime; only the selected profile is injected. Add more by dropping a new `.md` into
  `profiles/` — `../profile_loader.py` discovers it automatically (no code change). Started
  with 5 profiles by choice, not by limit.

Load them via `../profile_loader.py`:

```python
from profile_loader import list_profiles, load_profile
choices  = list_profiles()            # {slug: display_name} — feed a Gradio dropdown
profile  = load_profile("founder")    # Markdown text of the chosen profile
```

## 2. Secondary KB — Contextual Source Material (per session, user-uploaded)

Defines **what** to write about: a single uploaded document (report, notes, article,
etc.) provided at runtime through the Gradio upload. It is **not** stored here — it is
read on the fly by `../document_reader.py` (`read_uploaded_file`), which extracts text
from PDF / DOCX / TXT.

## Flow

```
profiles/<chosen>.md  ─►  profile_loader.load_profile()  ─┐
                                                          ├─►  prompts.build_prompt(platform, profile, source)  ─►  OpenAI  ─►  blog / linkedin / instagram
uploaded file ─► document_reader.read_uploaded_file() ────┘
```

## Context-size guard (from the RAG decision)

If `profile + source` ever exceeds a safe token budget, apply the documented **RAG-lite
fallback**: chunk/summarize the *source* only, keeping the profile intact. This path is
documented but not built for the MVP.
