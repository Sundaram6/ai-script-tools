"""Quick preset chips for common monologue themes."""

import streamlit as st

# Preset themes with corresponding situation, emotion, and optional archetype
PRESETS = [
    {
        "name": "Broken Heart",
        "situation": "A person grappling with the pain of a broken heart after a painful breakup",
        "emotion": "Grief",
        "archetype": "Broken Soul",
    },
    {
        "name": "Betrayal",
        "situation": "Confronting a trusted friend who has betrayed your confidence",
        "emotion": "Anger",
        "archetype": "Rebel",
    },
    {
        "name": "Father-Son Conflict",
        "situation": "A heated argument between father and son about life choices and expectations",
        "emotion": "Anger",
        "archetype": "Rebel",
    },
    {
        "name": "Dreamer",
        "situation": "A person sharing their ambitious dreams with a skeptical audience",
        "emotion": "Hope",
        "archetype": "Hero",
    },
    {
        "name": "Revenge",
        "situation": "Planning and executing a revenge plot against someone who wronged you",
        "emotion": "Anger",
        "archetype": "Villain",
    },
    {
        "name": "Lost Love",
        "situation": "Reflecting on a love that was lost due to circumstances beyond control",
        "emotion": "Regret",
        "archetype": "Lover",
    },
    {
        "name": "Success",
        "situation": "Celebrating a hard-won success after overcoming numerous obstacles",
        "emotion": "Joy",
        "archetype": "Hero",
    },
    {
        "name": "Failure",
        "situation": "Coming to terms with a significant failure and what it means for the future",
        "emotion": "Regret",
        "archetype": "Broken Soul",
    },
]


def render_presets():
    """Render quick preset chips.
    
    Returns:
        Boolean indicating if a preset was clicked.
    """
    st.markdown("### Quick Presets")
    # Use columns for layout
    cols = st.columns(len(PRESETS))
    preset_clicked = False
    
    for idx, preset in enumerate(PRESETS):
        with cols[idx]:
            if st.button(preset["name"], key=f"preset_{idx}"):
                # Set session state for advanced options fields
                st.session_state["adv_situation"] = preset["situation"]
                st.session_state["adv_emotion"] = preset["emotion"]
                st.session_state["adv_archetype"] = preset["archetype"]
                preset_clicked = True
                st.rerun()
    
    return preset_clicked