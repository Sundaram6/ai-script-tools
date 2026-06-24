"""Character summary card component for Monologue Generator."""

import streamlit as st


def render_character_card(inputs: dict, parsed_content: dict):
    """Render a character summary card.
    
    Args:
        inputs: Dictionary of user inputs (archetype, emotion, medium, etc.)
        parsed_content: Parsed content from response (may contain character_profile).
    """
    # Extract character name from parsed content if available
    character_profile = parsed_content.get("character_profile", {})
    character_name = character_profile.get("name", "Generated Character") if character_profile else "Generated Character"
    
    # Get age from profile or use age_range from inputs
    age = character_profile.get("age", inputs.get("age_range", "N/A"))
    
    archetype = inputs.get("archetype", "N/A")
    emotion = inputs.get("emotion", "N/A")
    medium = inputs.get("medium", "N/A")
    
    # Create card with styled HTML
    st.markdown(
        f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        ">
            <h3 style="margin-top: 0; color: #333;">🎭 {character_name}</h3>
            <p style="margin: 5px 0;"><strong>Age:</strong> {age}</p>
            <p style="margin: 5px 0;"><strong>Archetype:</strong> {archetype}</p>
            <p style="margin: 5px 0;"><strong>Emotion:</strong> {emotion}</p>
            <p style="margin: 5px 0;"><strong>Medium:</strong> {medium}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )