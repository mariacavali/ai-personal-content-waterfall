"""
Platform-specific prompt templates for AI Personal Content Waterfall.

Ugo's deliverable: prompt-engineering support.

Each builder combines the project's two knowledge sources into a single prompt:
  - communication_profile : HOW the author writes (voice, tone, audience, priorities)
  - source_material       : WHAT to write about (the uploaded contextual document)

Per rag_decision.md, both knowledge sources are injected directly into the prompt
(direct context injection) rather than retrieved from a vector store. These builders
are model-agnostic strings; the app layer (generator) passes them to the OpenAI client.
"""

SYSTEM_ROLE = (
    "You are a communication assistant that rewrites source material into "
    "platform-specific content while faithfully preserving the author's personal "
    "communication style. Rules: (1) match the author's voice as described in the "
    "communication profile; (2) never invent facts, names, figures, or claims that are "
    "not supported by the source material; (3) if the source material is thin, stay "
    "faithful and concise rather than padding."
)


def _context_block(communication_profile: str, source_material: str) -> str:
    """Shared two-knowledge-base context block used by every platform prompt."""
    return (
        "=== AUTHOR COMMUNICATION PROFILE (how to write) ===\n"
        f"{communication_profile.strip()}\n\n"
        "=== SOURCE MATERIAL (what to write about) ===\n"
        f"{source_material.strip()}"
    )


def build_blog_prompt(communication_profile: str, source_material: str) -> str:
    return f"""{_context_block(communication_profile, source_material)}

=== TASK ===
Write a BLOG ARTICLE based only on the source material, in the author's voice.

Return Markdown with:
- An engaging title (H1).
- A short introduction that frames why this matters to the reader.
- 2–4 sections, each with a descriptive H2 subheading.
- A closing section with a takeaway or call to action.

Length: roughly 500–800 words. Keep it substantive, well-structured, and true to the
author's tone and messaging priorities. Do not use clickbait.
"""


def build_linkedin_prompt(communication_profile: str, source_material: str) -> str:
    return f"""{_context_block(communication_profile, source_material)}

=== TASK ===
Write a LINKEDIN POST based only on the source material, in the author's voice.

Constraints:
- Open with a strong first line that works as a standalone hook (no "In this post...").
- Short, scannable paragraphs (1–3 sentences each), separated by blank lines.
- Professional but personal; reflect the author's tone and key messaging priorities.
- End with a light call to action or a question to invite engagement.
- 1–3 relevant hashtags on the final line.

Length: roughly 150–300 words. No clickbait, no emoji spam.
"""


def build_instagram_prompt(communication_profile: str, source_material: str) -> str:
    return f"""{_context_block(communication_profile, source_material)}

=== TASK ===
Write an INSTAGRAM CAPTION based only on the source material, in the author's voice.

Constraints:
- Start with an attention-grabbing first line.
- Concise and punchy, with short lines and deliberate line breaks for readability.
- Use emojis only if they fit the author's brand described in the profile (sparingly).
- End with a clear call to action.
- 3–8 relevant hashtags on the final line.

Length: roughly 60–150 words in the caption body (excluding hashtags).
"""


# Registry so the app can iterate over platforms cleanly.
PLATFORM_BUILDERS = {
    "blog": build_blog_prompt,
    "linkedin": build_linkedin_prompt,
    "instagram": build_instagram_prompt,
}


def build_prompt(platform: str, communication_profile: str, source_material: str) -> str:
    """Dispatch to the correct platform builder. Raises on unknown platform."""
    try:
        builder = PLATFORM_BUILDERS[platform.lower()]
    except KeyError:
        raise ValueError(
            f"Unknown platform '{platform}'. "
            f"Expected one of: {', '.join(PLATFORM_BUILDERS)}."
        )
    return builder(communication_profile, source_material)
