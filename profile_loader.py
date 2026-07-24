"""
Profile loader for AI Personal Content Waterfall.

Ugo's deliverable: knowledge-base preparation.

Discovers and loads representative communication profiles from
``knowledge_base/profiles/*.md``. Any ``.md`` dropped into that folder becomes available
automatically — no code change needed to add profiles later (the 5-profile cap is a
curation choice, not a technical limit).

Per rag_decision.md, a selected profile is injected directly into the prompt (no
retrieval). Selection is an explicit choice — e.g. a Gradio dropdown wired by the app
layer — not a semantic search.

Typical use in the app layer:

    from profile_loader import list_profiles, load_profile
    from prompts import build_prompt

    choices = list_profiles()                 # {slug: display_name} for the dropdown
    profile = load_profile(selected_slug)     # Markdown text of the chosen profile
    prompt = build_prompt("linkedin", profile, source_material)
"""

from pathlib import Path

PROFILES_DIR = Path(__file__).parent / "knowledge_base" / "profiles"


def _display_name(md_path: Path) -> str:
    """Human label for a profile: its first H1 heading, else a prettified filename."""
    try:
        for line in md_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    except OSError:
        pass
    return md_path.stem.replace("_", " ").replace("-", " ").title()


def list_profiles(profiles_dir=PROFILES_DIR) -> dict:
    """
    Return available profiles as an ordered ``{slug: display_name}`` mapping.

    ``slug`` is the filename without extension; pass it to ``load_profile``.
    """
    directory = Path(profiles_dir)
    return {p.stem: _display_name(p) for p in sorted(directory.glob("*.md"))}


def load_profile(name: str, profiles_dir=PROFILES_DIR) -> str:
    """
    Load a profile's Markdown text by slug (filename without ``.md``).

    Raises ``ValueError`` if the profile does not exist.
    """
    directory = Path(profiles_dir)
    md_path = directory / f"{name}.md"
    if not md_path.is_file():
        available = ", ".join(list_profiles(directory)) or "(none found)"
        raise ValueError(f"Unknown profile '{name}'. Available: {available}.")
    return md_path.read_text(encoding="utf-8")
