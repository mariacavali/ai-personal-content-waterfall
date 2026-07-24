"""
OpenAI generation for AI Personal Content Waterfall.

STARTER SCAFFOLD (app layer — Maria's deliverable). Combines the platform prompt from
`prompts.build_prompt` with the OpenAI Chat Completions call, following the pattern from the
team's MoveFlow-Learning-Walk `generator.py`.

The OpenAI client is created lazily so the UI can load without a key; generation then raises
a clear message if OPENAI_API_KEY is missing.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from prompts import build_prompt, SYSTEM_ROLE

MODEL = "gpt-4o-mini"  # configurable — any current OpenAI chat model

_client = None


def _get_client():
    global _client
    if _client is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Add it to a local .env file (never commit it)."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def generate_for_platform(platform, communication_profile, source_material, model=MODEL):
    """Generate content for one platform ('blog' | 'linkedin' | 'instagram')."""
    prompt = build_prompt(platform, communication_profile, source_material)
    response = _get_client().chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_ROLE},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def generate_all(communication_profile, source_material,
                 platforms=("blog", "linkedin", "instagram"), model=MODEL):
    """Convenience: generate all platforms, returning {platform: text}."""
    return {
        platform: generate_for_platform(platform, communication_profile, source_material, model)
        for platform in platforms
    }
