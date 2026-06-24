"""Sidebar component for Monologue Generator."""

import streamlit as st

# Constants
ARCHETYPES = [
    "Hero",
    "Villain",
    "Lover",
    "Mentor",
    "Rebel",
    "Comedian",
    "Broken Soul",
    "Gangster",
]

EMOTIONS = [
    "Love",
    "Fear",
    "Anger",
    "Grief",
    "Hope",
    "Regret",
    "Jealousy",
    "Joy",
]

MEDIUMS = ["Film", "OTT", "TV Serial", "Theatre", "Commercial"]

AGE_RANGES = ["Child", "Teen", "Young Adult", "Adult", "Senior"]

LANGUAGES = ["Hindi", "English", "Hinglish"]

WORD_COUNTS = [100, 250, 500, 750]

LANGUAGE_MAP = {
    "Hindi": "Hindi Film",
    "English": "English Theatre",
    "Hinglish": "Hinglish (Mixed)",
}

MODELS = ["gemini-2.5-flash", "gemini-2.5-pro"]


def render_sidebar():
    """Render the settings sidebar.
    
    Returns:
        Tuple of (model, temperature)
    """
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Model", MODELS, index=0)
        temperature = st.slider("Temperature", 0.0, 2.0, 1.2, 0.1)
    
    return model, temperature