import json
import time
from google import genai
from google.genai import types
import streamlit as st

# ── PAGE CONFIG ─────────────────────────────────────
st.set_page_config(
    page_title="Script Generator",
    page_icon="🎬",
    layout="centered"
)

# ── STYLES ──────────────────────────────────────────
st.markdown("""
    <style>
    .scene-box {
        background-color: #1a1a1a;
        color: #f0f0f0;
        padding: 2rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    .field-label {
        font-size: 11px;
        font-weight: 600;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 4px;
    }
    .field-value {
        font-size: 15px;
        color: #f0f0f0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────
st.title("🎬 Script Generator")
st.caption("Powered by Gemini · Bollywood Showrunner Mode")
st.divider()

# ── SIDEBAR CONTROLS ────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Paste your API key here"
    )

    model_choice = st.selectbox(
        "Model",
        options=[
            "models/gemini-2.0-flash-lite",
            "models/gemini-2.5-flash-lite",
            "models/gemini-2.5-flash",
            "models/gemini-2.5-pro",
        ],
        index=0
    )

    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Lower = more focused. Higher = more creative and unpredictable."
    )

    persona = st.selectbox(
        "Showrunner Persona",
        options=[
            "Bollywood Veteran",
            "Indie Art House Director",
            "Noir Crime Writer",
            "Rom-Com Specialist",
            "Custom..."
        ]
    )

    if persona == "Custom...":
        custom_persona = st.text_area(
            "Write your own persona",
            placeholder="You are a..."
        )
    
    st.divider()
    st.caption("Built with Streamlit + Gemini API")

# ── PERSONA MAP ──────────────────────────────────────
PERSONAS = {
    "Bollywood Veteran": """
You are a veteran Bollywood showrunner with 20 years of experience.
You write ONLY in industry-standard Indian screenplay format.
Your dialogue is sharp, authentic, and often switches between Hindi and English naturally.
Scene headings are precise. You never break character. You never add commentary.
""",
    "Indie Art House Director": """
You are an award-winning Indian indie film director known for slow cinema.
Your scenes are sparse, poetic, and heavy with silence and subtext.
Dialogue is minimal. Every object in the scene means something.
You write in standard screenplay format. No commentary after the scene.
""",
    "Noir Crime Writer": """
You are a hardboiled noir crime writer working in the Mumbai underworld genre.
Your dialogue is clipped, dangerous, and full of dark irony.
Scenes are atmospheric — rain, shadows, moral ambiguity.
Standard screenplay format only. No commentary.
""",
    "Rom-Com Specialist": """
You are a Bollywood rom-com writer with a gift for witty, warm dialogue.
Your scenes are charming, funny, and emotionally honest.
Characters feel real — awkward, lovable, and flawed.
Standard screenplay format only. No commentary.
"""
}

# ── MAIN INPUT ──────────────────────────────────────
st.subheader("Your Scene Brief")

user_request = st.text_area(
    "What is the scene about?",
    placeholder="e.g. A struggling actor gets his first big break...",
    height=100
)

extra_notes = st.text_input(
    "Any specific instructions? (optional)",
    placeholder="e.g. Set it in 1990s Mumbai. Make the dialogue funnier."
)

generate_btn = st.button("🎬 Generate Scene", use_container_width=True, type="primary")

# ── GENERATION LOGIC ────────────────────────────────
def get_system_instruction(persona, custom_persona=""):
    if persona == "Custom...":
        return custom_persona
    return PERSONAS.get(persona, PERSONAS["Bollywood Veteran"])

def generate_scene(api_key, model, temperature, system_instruction, user_request, extra_notes):
    client = genai.Client(api_key=api_key)

    prompt = f"""
Write a short scene based on: {user_request}
{f"Additional notes: {extra_notes}" if extra_notes else ""}

Return ONLY valid JSON, no extra text:
{{
  "scene_heading": "INT./EXT. LOCATION - TIME OF DAY",
  "character_name": "NAME IN CAPS",
  "character_description": "Age, one striking detail",
  "logline": "One sentence about what the scene is really about",
  "scene_text": "Full formatted scene here"
}}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature
                ),
                contents=prompt
            )
            return response.text

        except Exception as e:
            if "429" in str(e):
                wait = 30 * (attempt + 1)
                st.warning(f"Quota hit. Retrying in {wait} seconds... (attempt {attempt + 1}/3)")
                time.sleep(wait)
            else:
                st.error(f"Error: {e}")
                return None

    st.error("All retries failed. Try a different model or wait a few minutes.")
    return None

# ── OUTPUT ──────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not user_request:
        st.error("Please write what your scene is about.")
    else:
        system_instruction = get_system_instruction(persona, 
            custom_persona if persona == "Custom..." else "")

        with st.spinner("Generating your scene..."):
            raw_text = generate_scene(
                api_key, model_choice, temperature,
                system_instruction, user_request, extra_notes
            )

        if raw_text:
            # Clean JSON
            clean_text = raw_text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("```")[1]
                if clean_text.startswith("json"):
                    clean_text = clean_text[4:]

            try:
                data = json.loads(clean_text.strip())

                # Metadata row
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<p class="field-label">Scene</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="field-value">{data["scene_heading"]}</p>', unsafe_allow_html=True)
                    st.markdown('<p class="field-label">Character</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="field-value">{data["character_name"]} — {data["character_description"]}</p>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<p class="field-label">Logline</p>', unsafe_allow_html=True)
                    st.markdown(f'<p class="field-value">{data["logline"]}</p>', unsafe_allow_html=True)

                st.divider()

                # Scene text
                st.markdown("**Scene**")
                st.markdown(f'<div class="scene-box">{data["scene_text"]}</div>', unsafe_allow_html=True)

                st.divider()

                # Download button
                full_output = f"""SCENE: {data['scene_heading']}
CHARACTER: {data['character_name']} — {data['character_description']}
LOGLINE: {data['logline']}

{data['scene_text']}"""

                st.download_button(
                    label="⬇️ Download Scene",
                    data=full_output,
                    file_name="scene.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except json.JSONDecodeError:
                st.error("Couldn't parse the response. Raw output below:")
                st.code(raw_text)