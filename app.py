"""Streamlit app for Monologue Generator."""

import streamlit as st
import json

from prompts import build_monologue_prompt
from generator import generate_monologue
from utils import validate_inputs, clean_response

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
    """Render the settings sidebar."""
    st.sidebar.title("Settings")
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password",
        help="Get your API key from https://aistudio.google.com/apikey",
    )
    model = st.sidebar.selectbox("Model", MODELS, index=0)
    temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.2, 0.1)
    return api_key, model, temperature


def render_inputs():
    """Render the input form. Returns dict of user inputs."""
    st.title("Monologue Generator")
    st.markdown("Generate audition-ready monologues powered by Gemini AI.")

    col1, col2 = st.columns(2)

    with col1:
        archetype = st.selectbox("Character Archetype", ARCHETYPES)
        emotion = st.selectbox("Emotion", EMOTIONS)
        medium = st.selectbox("Medium", MEDIUMS)
        intensity = st.slider("Emotional Intensity", 1, 10, 5)
        age_range = st.selectbox("Age Range", AGE_RANGES)

    with col2:
        language = st.selectbox("Language", LANGUAGES)
        word_count = st.selectbox("Word Count", WORD_COUNTS, index=2)
        situation = st.text_input(
            "Situation",
            placeholder="A son confronting his father after years of abandonment",
        )
        spoken_to = st.text_input(
            "Spoken To",
            placeholder="Father",
        )
        extra = st.text_area(
            "Extra Instructions (optional)",
            placeholder="Add any specific notes or requirements...",
            height=100,
        )

    return {
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


def display_output(result):
    """Display the generated monologue in tabs."""
    content = result.get("content", {})

    if not isinstance(content, dict):
        st.warning("Response could not be parsed. Displaying raw output:")
        st.text(str(content))
        return

    tab1, tab2, tab3 = st.tabs(["Monologue", "Character Breakdown", "Performance Notes"])

    with tab1:
        monologue = content.get("monologue", {})
        profile = content.get("character_profile", {})
        beats = content.get("emotional_beats", {})

        if profile:
            st.subheader("Character Profile")
            st.write(f"**Name:** {profile.get('name', 'N/A')}")
            st.write(f"**Age:** {profile.get('age', 'N/A')}")
            st.write(f"**Background:** {profile.get('background', 'N/A')}")
            st.write(f"**Core Desire:** {profile.get('core_desire', 'N/A')}")
            st.write(f"**Biggest Fear:** {profile.get('biggest_fear', 'N/A')}")

        if monologue:
            st.subheader("Monologue")
            st.text_area(
                "Generated Monologue",
                value=monologue.get("text", "No text generated"),
                height=400,
                disabled=True,
                label_visibility="collapsed",
            )

        if beats:
            st.subheader("Emotional Beats")
            for beat_name, beat_text in beats.items():
                st.write(f"**{beat_name.replace('_', ' ').title()}:** {beat_text}")

    with tab2:
        breakdown = content.get("character_breakdown", {})
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

    with tab3:
        notes = content.get("performance_notes", {})
        if notes:
            st.subheader("Performance Notes")
            st.write(f"**Voice:** {notes.get('voice', 'N/A')}")
            st.write(f"**Pacing:** {notes.get('pacing', 'N/A')}")
            st.write(f"**Body Language:** {notes.get('body_language', 'N/A')}")
            st.write(f"**Eye Focus:** {notes.get('eye_focus', 'N/A')}")
            st.write(f"**Breathing Notes:** {notes.get('breathing_notes', 'N/A')}")


def main():
    st.set_page_config(
        page_title="Monologue Generator",
        page_icon="",
        layout="wide",
    )

    api_key, model, temperature = render_sidebar()
    inputs = render_inputs()

    if st.button("Generate Monologue", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar.")
            return

        language_mapped = LANGUAGE_MAP.get(inputs["language"], inputs["language"])

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

        with st.spinner("Generating your monologue..."):
            result = generate_monologue(
                prompt=prompt,
                api_key=api_key,
                model=model,
                temperature=temperature,
            )

        if result["success"]:
            st.success("Monologue generated successfully!")
            display_output(result)
        else:
            st.error(result.get("error", "Generation failed."))


if __name__ == "__main__":
    main()
