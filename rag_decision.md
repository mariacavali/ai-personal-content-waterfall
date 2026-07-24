# RAG Decision

**Project:** AI Personal Content Waterfall
**Author of research:** Ugo Ahukannah
**Status:** Research complete — recommendation for team ratification (Elza, Maria, Ugo)
**Date:** 2026-07-24

---

## 1. Purpose

This document records the team's evaluation of whether to use **Retrieval-Augmented
Generation (RAG)** in the MVP, the reasoning behind the decision, and the implementation
approach we will follow. It closes the "RAG Research" task and feeds the shared "RAG
Decision".

## 2. What RAG is (in one paragraph)

RAG is a pattern where, instead of relying only on what the model already knows, you
**retrieve** the most relevant pieces of an external corpus at query time and **inject**
them into the prompt as context. In its full form it means: split documents into chunks,
embed each chunk into a vector, store the vectors in a vector database, embed the incoming
query, retrieve the top-k most similar chunks, and pass those to the model. Its whole reason
to exist is handling corpora **too large to fit in the model's context window**.

## 3. Our actual use case

We have two knowledge sources per generation:

| Knowledge base | Contents | Typical size |
|---|---|---|
| **Communication profile** (primary) | writing style, tone, audience, example content, messaging priorities | Small, stable — comfortably a few hundred to low-thousand tokens |
| **Contextual source material** (secondary) | one uploaded document / report / notes per session | Variable, but a single source per run |

Key facts that drive the decision:

- Generation is **single-session and single-source** — the user uploads material and we
  generate from *that*, not from a growing archive of thousands of documents.
- The communication profile is **small and fixed**.
- Our target model (OpenAI GPT-4o class) has a **~128k-token context window** — large enough
  to hold the full profile plus a typical uploaded document directly.
- Project scope **explicitly excludes databases** and production infrastructure, and the
  cost objective is to **minimise API usage**.

## 4. Options considered

**Option A — Direct context injection ("no RAG").**
Put the full communication profile and the full source material straight into the prompt.
Retrieval is unnecessary because everything fits in context.
*Effort:* minimal — prompt assembly only. *Fits MVP scope and timeframe:* yes.

**Option B — Full vector RAG.**
Chunk + embed the source material, store in a vector DB (e.g. Chroma/FAISS), retrieve top-k
at generation time.
*Effort:* high for a 2-day MVP — adds embeddings, a vector store, chunking strategy, and
retrieval tuning. *Conflicts with:* the "no database" scope exclusion and the cost/time
objectives. Adds an embeddings API call per run with little quality gain at our corpus size.

**Option C — Hybrid / RAG-lite (fallback only).**
Default to Option A, but if an uploaded document is **larger than the context budget**,
fall back to a lightweight in-memory retrieval step (chunk the single document, embed, keep
only the most relevant chunks). No persistent vector DB.
*Effort:* moderate; only pays off for oversized inputs, which are out of the common path for
this MVP.

## 5. Recommendation

**Adopt Option A (direct context injection) for the MVP. Do not implement full vector RAG.**

Rationale:

1. **The corpus fits in context.** RAG's core benefit — selecting from a corpus too big to
   fit — does not apply to a single small profile plus one source document.
2. **Scope alignment.** Full RAG needs a vector store; the project scope explicitly excludes
   databases. Option A stays inside the agreed boundary.
3. **Time and cost.** Option A ships within the two-day window and avoids extra embedding API
   calls, directly serving the Time and Cost objectives.
4. **Quality is driven by prompting, not retrieval, here.** Preserving the author's voice
   depends on how well we structure the profile and platform-specific prompts — Ugo's
   prompt-engineering work — not on retrieval machinery.
5. **It is a pattern the team has already shipped.** Maria and Elza's earlier project
   (`eerele-art/MoveFlow-Learning-Walk`) does document-to-content generation with exactly
   this approach: `document_reader.py` extracts the full text of an uploaded PDF/DOCX/TXT,
   and `generator.py` injects that whole text directly into the prompt (OpenAI, no
   embeddings, no vector store, no retrieval). It shipped and worked. We are reusing a
   validated pattern, not inventing one under time pressure.

We document Option C as a **known, deliberate fallback** and Option B as a **future
enhancement** for when the contextual knowledge base grows into a large, reusable archive.

## 6. Implementation approach (Option A)

- Load the communication profile from a local file (e.g. `knowledge_base/profile.md`) into a
  system/context block.
- Read the user-uploaded source material (via the Gradio upload) into a context block.
  **Reuse `document_reader.py` from `MoveFlow-Learning-Walk` almost verbatim** — it already
  extracts text from PDF/DOCX/TXT and matches our stack (`pypdf`, `python-docx`).
- Apply **platform-specific prompt templates** (blog / LinkedIn / Instagram) that reference
  both blocks — same `client.chat.completions.create(...)` shape used in that project's
  `generator.py`.
- Guard the context size: if profile + source exceeds a safe token budget, trigger the
  Option C fallback (truncate/summarise or chunk-and-select the source only).

**Reusable stack (proven in the prior repo):** `gradio`, `openai`, `python-dotenv`, `pypdf`,
`python-docx`.

## 7. Future enhancements (out of scope for MVP)

- Persistent vector store if the contextual KB becomes a large, reusable corpus across many
  sessions.
- Semantic retrieval across a user's document history.
- Caching of embeddings to control cost at scale.

**Note on the multi-profile feature.** The MVP ships a small, curated library of
representative communication profiles (see `knowledge_base/profiles/`, selected explicitly
via the UI). This stays pure direct context injection — the chosen profile `.md` is loaded
whole into the prompt, and selection is an explicit dropdown, not a search. If that library
ever grew large (dozens or more profiles), *semantic* selection among profiles would be the
point at which RAG-lite earns its place. So the feature is fully consistent with this
decision, and also marks the concrete threshold that would later justify revisiting it.

## 8. Decision log

| Date | Decision | Owner |
|---|---|---|
| 2026-07-24 | MVP uses direct context injection (Option A); full RAG deferred | Team (proposed by Ugo) |
