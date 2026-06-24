"""Streamlit app for Monologue Generator."""

import random

import streamlit as st

from prompts import build_monologue_prompt, build_smart_monologue_prompt
from generator import generate_monologue
from utils import validate_inputs, clean_response

from components.hero import render_hero
from components.sidebar import render_sidebar, LANGUAGE_MAP
from components.api_panel import render_api_panel, render_demo_mode
from components.parser import parse_response
from components.output_tabs import render_output_tabs
from components.cards import render_character_card
from components.character_cards import render_character_cards
from components.advanced_options import render_advanced_options

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


def render_footer():
    """Render minimal branding footer."""
    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 2rem 0;
            color: #666;
            font-size: 0.9rem;
            border-top: 1px solid #333;
            margin-top: 2rem;
        ">
            Monologue Generator AI — Built for Actors, Performers, and Storytellers
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
    
    # Initialize session state for last result
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    
    # Render hero
    render_hero()
    
    # Render API key panel and get key
    api_key = render_api_panel()
    
    # Render character cards on main page
    character_selections = render_character_cards()
    
    # Render sidebar and get model settings
    model, temperature = render_sidebar()
    
    # Render advanced options on main page
    advanced_options = render_advanced_options()
    
    # Create inputs dict from advanced options
    inputs = advanced_options.copy()
    
    # Update inputs with character card selections
    inputs["gender"] = character_selections["gender"]
    inputs["age_range"] = character_selections["age"]
    inputs["language"] = character_selections["language"]
    
    # Demo mode
    demo_monologue = render_demo_mode()
    if demo_monologue:
        inputs["archetype"] = demo_monologue["archetype"]
        inputs["emotion"] = demo_monologue["emotion"]
        inputs["age_range"] = demo_monologue["age_range"]
        inputs["medium"] = demo_monologue["medium"]
        inputs["language"] = demo_monologue["language"]
        inputs["intensity"] = demo_monologue["intensity"]
        inputs["situation"] = demo_monologue["situation"]
        inputs["spoken_to"] = demo_monologue["spoken_to"]
        inputs["word_count"] = demo_monologue["word_count"]
        parsed_content = parse_response(demo_monologue["monologue"])
        st.session_state.last_result = {
            "inputs": inputs,
            "parsed_content": parsed_content,
        }
        st.success("Demo monologue loaded!")
        render_character_card(inputs, parsed_content)
        render_output_tabs(inputs, parsed_content)
        render_footer()
        return
    
    # Generate button
    if st.button("Generate Monologue", type="primary", use_container_width=True):
        if not api_key:
            st.error(
                "Please enter your Gemini API Key in the sidebar, "
                "or try Demo Mode above."
            )
            return
        
        language_mapped = LANGUAGE_MAP.get(inputs["language"], inputs["language"])
        
        # Check if situation is empty to decide between smart or full generation
        situation_filled = inputs["situation"].strip()
        if not situation_filled:
            # Smart generation: user only provided gender, age, language
            prompt = build_smart_monologue_prompt(
                gender=inputs["gender"],
                age=inputs["age_range"],
                language=language_mapped,
            )
        else:
            # Full generation: validate all inputs
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
            # Store last result in session state
            st.session_state.last_result = {
                "inputs": inputs,
                "parsed_content": parsed_content,
            }
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
        if st.session_state.last_result:
            # Render last generated result
            last = st.session_state.last_result
            render_character_card(last["inputs"], last["parsed_content"])
            render_output_tabs(last["inputs"], last["parsed_content"])
        else:
            render_empty_state()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()