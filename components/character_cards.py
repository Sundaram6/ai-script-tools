"""Card-based selectors for Gender, Age, and Language."""

import streamlit as st


GENDER_OPTIONS = [
    {"label": "Male", "icon": "👨"},
    {"label": "Female", "icon": "👩"},
]

AGE_OPTIONS = [
    {"label": "Child", "icon": "👶"},
    {"label": "Teen", "icon": "🧑"},
    {"label": "Young Adult", "icon": "🧑‍🎓"},
    {"label": "Adult", "icon": "🧑‍💼"},
    {"label": "Senior", "icon": "👴"},
]

LANGUAGE_OPTIONS = [
    {"label": "Hindi", "icon": "🇮🇳"},
    {"label": "English", "icon": "🇬🇧"},
    {"label": "Hinglish", "icon": "🌏"},
]

CARD_CSS = """
<style>
.card-selector {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin: 10px 0;
}
.card-option {
    flex: 1;
    min-width: 100px;
    padding: 15px 10px;
    border: 2px solid #333;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #1a1a2e;
}
.card-option:hover {
    border-color: #e94560;
    background: #16213e;
}
.card-option.selected {
    border-color: #e94560;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    box-shadow: 0 0 10px rgba(233, 69, 96, 0.3);
}
.card-icon {
    font-size: 2rem;
    margin-bottom: 5px;
}
.card-label {
    font-size: 0.9rem;
    font-weight: 600;
    color: #fff;
}
</style>
"""


def _render_card_group(options: list, key_prefix: str) -> str:
    """Render a group of selectable cards and return selected value.
    
    Args:
        options: List of dicts with 'label' and 'icon' keys
        key_prefix: Unique prefix for streamlit keys
        
    Returns:
        Selected label string
    """
    st.markdown(CARD_CSS, unsafe_allow_html=True)
    
    cols = st.columns(len(options))
    selected = None
    
    for i, option in enumerate(options):
        with cols[i]:
            btn_key = f"{key_prefix}_{option['label']}"
            is_selected = st.session_state.get(btn_key, False)
            
            selected_class = "selected" if is_selected else ""
            
            if st.button(
                f"{option['icon']} {option['label']}",
                key=btn_key,
                use_container_width=True,
            ):
                # Clear other selections in this group
                for opt in options:
                    st.session_state[f"{key_prefix}_{opt['label']}"] = False
                st.session_state[btn_key] = True
                st.rerun()
    
    # Get selected value
    for option in options:
        if st.session_state.get(f"{key_prefix}_{option['label']}", False):
            selected = option["label"]
            break
    
    # Default to first option if nothing selected
    if selected is None:
        selected = options[0]["label"]
        st.session_state[f"{key_prefix}_{options[0]['label']}"] = True
    
    return selected


def render_character_cards() -> dict:
    """Render card-based selectors for Gender, Age, and Language.
    
    Returns:
        Dict with 'gender', 'age', and 'language' keys
    """
    st.subheader("Character")
    
    # Gender cards
    st.markdown("**Gender**")
    gender = _render_card_group(GENDER_OPTIONS, "gender")
    
    # Age cards
    st.markdown("**Age Range**")
    age = _render_card_group(AGE_OPTIONS, "age")
    
    # Language cards
    st.markdown("**Language**")
    language = _render_card_group(LANGUAGE_OPTIONS, "language")
    
    return {
        "gender": gender,
        "age": age,
        "language": language,
    }
