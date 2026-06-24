"""Streamlit app for Monologue Generator."""

import random

import streamlit as st

from prompts import build_monologue_prompt
from generator import generate_monologue
from utils import validate_inputs, clean_response

from components.hero import render_hero
from components.sidebar import render_sidebar, LANGUAGE_MAP
from components.parser import parse_response
from components.output_tabs import render_output_tabs

LOADING_MESSAGES = [
    "Building Character...",
    "Finding Emotional Truth...",
    "Writing Scene...",
    "Generating Monologue...",
    "Preparing Acting Notes...",
]


def main():
    st.set_page_config(
        page_title="Monologue Generator",
        page_icon="🎭",
        layout="wide",
    )
    
    # Render hero
    render_hero()
    
    # Render sidebar and get inputs
    inputs, api_key, model, temperature = render_sidebar()
    
    # Generate button
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
            render_output_tabs(inputs, parsed_content)
        else:
            st.error(result.get("error", "Generation failed."))


if __name__ == "__main__":
    main()