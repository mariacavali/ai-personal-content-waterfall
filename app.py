"""
AI Personal Content Waterfall — starter Gradio app.

STARTER SCAFFOLD, adapted from Maria and Elza's MoveFlow-Learning-Walk pipeline.
App development is Maria's deliverable — this is a runnable base to take over and polish,
not a finished app. It wires the existing building blocks together:

    profile dropdown  <- profile_loader.list_profiles / load_profile
    source text       <- document_reader.read_uploaded_file  (or pasted text)
    generation        <- generator.generate_for_platform  (prompts.build_prompt + OpenAI)

Run:
    pip install -r requirements.txt
    # add OPENAI_API_KEY to a local .env  (never commit it)
    python app.py
"""

import gradio as gr

from document_reader import read_uploaded_file
from profile_loader import list_profiles, load_profile
from generator import generate_for_platform

# Dropdown choices as (display name, slug) tuples.
_PROFILE_CHOICES = [(name, slug) for slug, name in list_profiles().items()]
_DEFAULT_PROFILE = _PROFILE_CHOICES[0][1] if _PROFILE_CHOICES else None


def _resolve_source(uploaded_file, pasted_text):
    if pasted_text and pasted_text.strip():
        return pasted_text.strip()
    if uploaded_file:
        return read_uploaded_file(uploaded_file)
    return ""


def generate(profile_slug, uploaded_file, pasted_text):
    """Return (blog, linkedin, instagram) content for the chosen profile + source."""
    if not profile_slug:
        msg = "⚠️ Pick a communication profile first."
        return msg, msg, msg

    try:
        source = _resolve_source(uploaded_file, pasted_text)
    except Exception as err:
        msg = f"⚠️ Could not read the uploaded file: {err}"
        return msg, msg, msg

    if not source.strip():
        msg = "⚠️ Upload a document or paste some text first."
        return msg, msg, msg

    profile = load_profile(profile_slug)

    try:
        blog = generate_for_platform("blog", profile, source)
        linkedin = generate_for_platform("linkedin", profile, source)
        instagram = generate_for_platform("instagram", profile, source)
    except Exception as err:
        msg = f"⚠️ Generation failed: {err}"
        return msg, msg, msg

    return blog, linkedin, instagram


with gr.Blocks(title="AI Personal Content Waterfall") as demo:
    gr.Markdown(
        "# AI Personal Content Waterfall\n"
        "Turn one source into a blog post, a LinkedIn post, and an Instagram caption — "
        "in a chosen communication voice.\n\n"
        "> 🚧 Starter scaffold — adapted from the MoveFlow pipeline, to be owned & finished by Maria."
    )

    with gr.Row():
        with gr.Column():
            profile_dd = gr.Dropdown(
                choices=_PROFILE_CHOICES,
                value=_DEFAULT_PROFILE,
                label="Communication profile (voice)",
            )
            with gr.Tabs():
                with gr.Tab("Upload document"):
                    uploaded_file = gr.File(
                        label="PDF, DOCX, or TXT",
                        file_types=[".pdf", ".docx", ".txt"],
                        type="filepath",
                    )
                with gr.Tab("Paste text"):
                    pasted_text = gr.Textbox(
                        label="Source material",
                        lines=10,
                        placeholder="Paste the source content here...",
                    )
            generate_btn = gr.Button("Generate content", variant="primary")

        with gr.Column():
            blog_out = gr.Textbox(label="Blog article", lines=12, show_copy_button=True)
            linkedin_out = gr.Textbox(label="LinkedIn post", lines=8, show_copy_button=True)
            instagram_out = gr.Textbox(label="Instagram caption", lines=6, show_copy_button=True)

    generate_btn.click(
        fn=generate,
        inputs=[profile_dd, uploaded_file, pasted_text],
        outputs=[blog_out, linkedin_out, instagram_out],
    )


if __name__ == "__main__":
    demo.launch()
