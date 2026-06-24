"""Streamlit app for Monologue Generator."""

import random

import streamlit as st

from prompts import build_monologue_prompt
from generator import generate_monologue
from utils import validate_inputs, clean_response

from components.hero import render_hero
from components.sidebar import render_sidebar, LANGUAGE_MAP
from components.parser import parse_response
from components.output_tabs import render_output_tabs
from components.cards import render_character_card

LOADING_MESSAGES = [
    "Building Character...",
    "Finding Emotional Truth...",
    "Writing Scene...",
    "Generating Monologue...",
    "Preparing Acting Notes...",
]

MOBILE_CSS = """
<style>
@media (max-width: 768px) {
    .stButton > button {
        font-size: 0.9rem;
        padding: 0.5rem 1rem;
    }
    .stSelectbox, .stTextInput, .stTextArea {
        font-size: 14px;
    }
    h1 { font-size: 1.8rem !important; }
    h2 { font-size: 1.4rem !important; }
    h3 { font-size: 1.2rem !important; }
    .monologue-reader { padding: 1rem !important; }
    .perf-grid { grid-template-columns: 1fr !important; }
}
</style>
"""


def render_empty_state():
    """Display the empty state before monologue generation."""
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 12px;
            border: 2px dashed #444;
            margin: 2rem 0;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎭</div>
            <h3 style="color: #e94560; margin-bottom: 0.5rem;">Ready to Create?</h3>
            <p style="color: #999; font-size: 1.1rem; max-width: 500px; margin: 0 auto;">
                Your generated monologue will appear here. Choose a character, emotion,
                and situation, then click <strong>Generate Monologue</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title="Monologue Generator",
        page_icon="🎭",
        layout="wide",
    )
    
    st.markdown(MOBILE_CSS, unsafe_allow_html=True)
    
    # Render hero
    render_hero()
    
    # Render sidebar and get inputs
    inputs, api_key, model, temperature = render_sidebar()
    
    # Generate button
    if st.button("Generate Monologue", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar.")
            return
        
        language_mapped = LANGUAGE_MAP.get(inputs["language"], inputs["language"])
        
        if not validate_inputs(
            language=language_mapped,
            archetype=inputs["archetype"],
            emotion=inputs["emotion"],
            age_range=inputs["age_range"],
            medium=inputs["medium"],
            emotional_intensity=inputs["intensity"],
            situation=inputs["situation"],
            spoken_to=inputs["spoken_to"],
            extra=inputs["extra"],
            target_words=inputs["word_count"],
        ):
            st.error("Please fill in all required fields (Situation and Spoken To).")
            return
        
        prompt = build_monologue_prompt(
            archetype=inputs["archetype"],
            emotion=inputs["emotion"],
            age_range=inputs["age_range"],
            medium=inputs["medium"],
            intensity=inputs["intensity"],
            situation=inputs["situation"],
            spoken_to=inputs["spoken_to"],
            language=language_mapped,
            word_count=inputs["word_count"],
            extra_instructions=inputs["extra"],
        )
        
        with st.spinner(random.choice(LOADING_MESSAGES)):
            result = generate_monologue(
                prompt=prompt,
                api_key=api_key,
                model=model,
                temperature=temperature,
            )
        
        if result["success"]:
            st.success("Monologue generated successfully!")
            parsed_content = parse_response(result.get("content", ""))
            render_character_card(inputs, parsed_content)
            render_output_tabs(inputs, parsed_content)
        else:
            error_msg = result.get("error", "")
            if "api" in error_msg.lower() or "key" in error_msg.lower():
                friendly_error = (
                    "Unable to generate monologue. "
                    "Please verify your API key or try again in a moment."
                )
            elif "timeout" in error_msg.lower():
                friendly_error = (
                    "Request timed out. "
                    "Please try again with a shorter monologue or different settings."
                )
            else:
                friendly_error = (
                    "Unable to generate monologue. "
                    "Please verify your API key or try again in a moment."
                )
            st.error(friendly_error)
    else:
        render_empty_state()


if __name__ == "__main__":
    main()