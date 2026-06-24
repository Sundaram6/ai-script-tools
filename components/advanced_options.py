"""Collapsible advanced options for power users."""

import streamlit as st

# Import constants from sidebar to keep consistent
from components.sidebar import (
    ARCHETYPES,
    EMOTIONS,
    MEDIUMS,
    WORD_COUNTS,
)


def render_advanced_options() -> dict:
    """Render collapsible advanced options section.
    
    Returns:
        Dict with advanced options values.
    """
    with st.expander("Advanced Options ▼", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            archetype = st.selectbox("Archetype", ARCHETYPES, key="adv_archetype")
            emotion = st.selectbox("Emotion", EMOTIONS, key="adv_emotion")
            medium = st.selectbox("Medium", MEDIUMS, key="adv_medium")
        
        with col2:
            word_count = st.selectbox("Word Count", WORD_COUNTS, index=2, key="adv_word_count")
            situation = st.text_input(
                "Situation",
                placeholder="A son confronting his father after years of abandonment",
                key="adv_situation",
            )
            spoken_to = st.text_input(
                "Spoken To",
                placeholder="Father",
                key="adv_spoken_to",
            )
        
        # Additional advanced options
        intensity = st.slider("Emotional Intensity", 1, 10, 5, key="adv_intensity")
        extra = st.text_area(
            "Extra Instructions (optional)",
            placeholder="Add any specific notes or requirements...",
            height=100,
            key="adv_extra",
        )
    
    return {
        "archetype": archetype,
        "emotion": emotion,
        "medium": medium,
        "word_count": word_count,
        "situation": situation,
        "spoken_to": spoken_to,
        "intensity": intensity,
        "extra": extra,
    }