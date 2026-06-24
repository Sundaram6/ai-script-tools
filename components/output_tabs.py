"""Output tabs component for Monologue Generator."""

import streamlit as st

from .cards import render_character_card


def render_output_tabs(inputs: dict, parsed_content: dict):
    """Render the output workspace with 5 tabs.
    
    Args:
        inputs: Dictionary of user inputs.
        parsed_content: Parsed content from response.
    """
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎬 Monologue",
        "🧠 Character Breakdown",
        "🎭 Emotional Beats",
        "🎤 Performance Notes",
        "📄 Full Output",
    ])
    
    with tab1:
        st.subheader("Character Summary")
        render_character_card(inputs, parsed_content)
        
        monologue = parsed_content.get("monologue", {})
        if monologue:
            st.subheader("Monologue")
            st.text_area(
                "Generated Monologue",
                value=monologue.get("text", "No text generated"),
                height=400,
                disabled=True,
                label_visibility="collapsed",
            )
        else:
            st.info("No monologue generated.")
    
    with tab2:
        breakdown = parsed_content.get("character_breakdown", {})
        if breakdown:
            st.subheader("Character Breakdown")
            st.write(f"**Objective:** {breakdown.get('objective', 'N/A')}")
            st.write(f"**Obstacle:** {breakdown.get('obstacle', 'N/A')}")
            st.write(f"**Stakes:** {breakdown.get('stakes', 'N/A')}")
            st.write(f"**Secret:** {breakdown.get('secret', 'N/A')}")
            st.write(f"**Animal Reference:** {breakdown.get('animal_reference', 'N/A')}")
            
            traits = breakdown.get("five_defining_traits", [])
            if traits:
                st.write("**Five Defining Traits:**")
                for trait in traits:
                    st.write(f"  - {trait}")
        else:
            st.info("No character breakdown available.")
    
    with tab3:
        beats = parsed_content.get("emotional_beats", {})
        if beats:
            st.subheader("Emotional Beats")
            for beat_name, beat_text in beats.items():
                st.write(f"**{beat_name.replace('_', ' ').title()}:** {beat_text}")
        else:
            st.info("No emotional beats available.")
    
    with tab4:
        notes = parsed_content.get("performance_notes", {})
        if notes:
            st.subheader("Performance Notes")
            st.write(f"**Voice:** {notes.get('voice', 'N/A')}")
            st.write(f"**Pacing:** {notes.get('pacing', 'N/A')}")
            st.write(f"**Body Language:** {notes.get('body_language', 'N/A')}")
            st.write(f"**Eye Focus:** {notes.get('eye_focus', 'N/A')}")
            st.write(f"**Breathing Notes:** {notes.get('breathing_notes', 'N/A')}")
        else:
            st.info("No performance notes available.")
    
    with tab5:
        st.subheader("Full Output")
        full_output = parsed_content.get("full_output", "")
        if full_output:
            st.text_area(
                "Full Response",
                value=full_output,
                height=400,
                disabled=True,
                label_visibility="collapsed",
            )
        else:
            st.info("No output available.")