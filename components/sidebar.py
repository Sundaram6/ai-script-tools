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

AGE_RANGES = ["Child", "Teen", "Young Adult", "Adult", "Elderly"]

LANGUAGES = ["Hindi", "English", "Hinglish"]

WORD_COUNTS = [100, 250, 500, 750]

LANGUAGE_MAP = {
    "Hindi": "Hindi Film",
    "English": "English Theatre",
    "Hinglish": "Hinglish (Mixed)",
}

MODELS = ["gemini-2.5-flash", "gemini-2.5-pro"]


def render_sidebar():
    """Render the settings and input sidebar.
    
    Returns:
        Tuple of (inputs_dict, model, temperature)
    """
    with st.sidebar:
        st.header("Settings")
        model = st.selectbox("Model", MODELS, index=0)
        temperature = st.slider("Temperature", 0.0, 2.0, 1.2, 0.1)
        
        st.divider()
        
        # Character Section
        st.subheader("Character")
        archetype = st.selectbox("Character Archetype", ARCHETYPES)
        age_range = st.selectbox("Age Range", AGE_RANGES)
        language = st.selectbox("Language", LANGUAGES)
        
        st.divider()
        
        # Emotional Section
        st.subheader("Emotional")
        emotion = st.selectbox("Emotion", EMOTIONS)
        intensity = st.slider("Emotional Intensity", 1, 10, 5)
        situation = st.text_input(
            "Situation",
            placeholder="A son confronting his father after years of abandonment",
        )
        spoken_to = st.text_input(
            "Spoken To",
            placeholder="Father",
        )
        
        st.divider()
        
        # Performance Section
        st.subheader("Performance")
        medium = st.selectbox("Medium", MEDIUMS)
        word_count = st.selectbox("Word Count", WORD_COUNTS, index=2)
        extra = st.text_area(
            "Extra Instructions (optional)",
            placeholder="Add any specific notes or requirements...",
            height=100,
        )
    
    inputs = {
        "archetype": archetype,
        "emotion": emotion,
        "medium": medium,
        "intensity": intensity,
        "age_range": age_range,
        "language": language,
        "word_count": word_count,
        "situation": situation,
        "spoken_to": spoken_to,
        "extra": extra,
    }
    
    return inputs, model, temperature