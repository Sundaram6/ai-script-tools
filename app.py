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
from components.presets import render_presets
from components.history import init_history, add_to_history, render_history_button, render_history_panel
from components.downloads import copy_monologue, copy_full_output, download_monologue_txt, download_full_output_txt, download_monologue_pdf, download_full_output_pdf, render_generate_another_button

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
    .card-selector { flex-direction: column; }
    .card-option { min-width: 100%; margin-bottom: 8px; }
    [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    .stColumn { width: 100% !important; }
    .block-container { padding: 1rem !important; }
}
.category-tabs {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 1.5rem 0;
}
.category-tab {
    padding: 0.7rem 1.5rem;
    border: 2px solid #444;
    background: #1a1a2e;
    color: #999;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
.category-tab:first-child {
    border-radius: 10px 0 0 10px;
}
.category-tab:last-child {
    border-radius: 0 10px 10px 0;
}
.category-tab:hover {
    border-color: #e94560;
    color: #fff;
}
.category-tab.active {
    border-color: #e94560;
    background: linear-gradient(135deg, #e94560 0%, #c81e45 100%);
    color: #fff;
    box-shadow: 0 0 12px rgba(233, 69, 96, 0.4);
}
.generate-btn-wrapper {
    text-align: center;
    margin: 2rem 0;
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
            <h3 style="color: #e94560; margin-bottom: 0.5rem;">Ready to Create</h3>
            <p style="color: #999; font-size: 1.1rem; max-width: 500px; margin: 0 auto;">
                Select age and gender, then let AI build a complete character and monologue for you.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


CATEGORIES = ["Random", "Film", "Theatre", "OTT"]


def render_category_tabs() -> str:
    """Render category tabs and return selected category."""
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Random"

    st.markdown("### Choose a Category")

    tab_cols = st.columns(4)
    for i, cat in enumerate(CATEGORIES):
        with tab_cols[i]:
            is_active = st.session_state.selected_category == cat
            active_class = "active" if is_active else ""
            st.markdown(
                f'<div class="category-tab {active_class}" style="text-align:center;">'
                f"<strong>{cat}</strong></div>",
                unsafe_allow_html=True,
            )
            if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                st.session_state.selected_category = cat
                st.rerun()

    return st.session_state.selected_category


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
    
    # Initialize history
    init_history()
    
    # Render hero
    render_hero()
    
    # Render history button in top-right
    render_history_button()
    
    # Render history panel if enabled
    render_history_panel()
    
    # Render API key panel and get key
    api_key = render_api_panel()
    
    # Render category tabs
    category = render_category_tabs()
    
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
        add_to_history(inputs, parsed_content)
        st.success("Demo monologue loaded!")
        render_character_card(inputs, parsed_content)
        render_output_tabs(inputs, parsed_content)
        render_footer()
        return
    
    # Generate button — large centered CTA
    st.markdown(
        '<div class="generate-btn-wrapper">'
        '<span style="font-size:0.9rem; color:#999;">Workflow: Category → Age + Gender + Language → Generate</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="text-align:center; margin-bottom:2rem;">',
        unsafe_allow_html=True,
    )
    generate_clicked = st.button(
        "✨ Generate Monologue",
        type="primary",
        use_container_width=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Check if "Generate Another Version" was clicked
    generate_another = st.session_state.get("generate_another", False)
    if generate_another:
        st.session_state.generate_another = False
        generate_clicked = True

    if generate_clicked:
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
                category=category,
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
                category=category,
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
            add_to_history(inputs, parsed_content)
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
            st.markdown("---")
            render_generate_another_button()
        else:
            render_empty_state()
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()