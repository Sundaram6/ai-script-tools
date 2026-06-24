"""Hero section component for Monologue Generator."""

import streamlit as st


def render_hero():
    """Render the hero header with branding."""
    st.markdown(
        """
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='font-size: 2.5em; margin-bottom: 0.2em;'>🎭 Monologue Generator AI</h1>
            <p style='font-size: 1.2em; color: #666; margin-top: 0;'>
                Generate original audition-ready monologues, character breakdowns,
                emotional beats, and performance notes in seconds.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )