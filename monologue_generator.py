import time
from gemini_client import generate_json
import streamlit as st

# ── PAGE CONFIG ─────────────────────────────────────
st.set_page_config(
    page_title="Monologue Generator",
    page_icon="🎭",
    layout="centered"
)

# ── STYLES ──────────────────────────────────────────
st.markdown("""
<style>
.monologue-box {
    background-color: #0f0f0f;
    color: #f5f5f5;
    padding: 2.5rem;
    border-radius: 12px;
    font-family: 'Courier New', monospace;
    font-size: 15px;
    line-height: 2;
    white-space: pre-wrap;
    border-left: 3px solid #e50914;
}
.practice-tip {
    background: #1a1a2e;
    border-left: 3px solid #4a90e2;
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    color: #ccc;
    line-height: 1.7;
    margin-top: 1rem;
}
.acting-coach-box {
    background: #0d1f0d;
    border-left: 3px solid #2ecc71;
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    font-size: 13px;
    color: #ccc;
    line-height: 1.8;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────
st.title("🎭 Monologue Generator")
st.caption("Built for audition practice · Powered by Gemini")
st.divider()

# ── SESSION HISTORY ──────────────────────────────────
if "monologue_history" not in st.session_state:
    st.session_state.monologue_history = []

# ── SIDEBAR ─────────────────────────────────────────
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
            "gemini-2.5-flash",
            "gemini-2.5-pro",
        ],
        index=0
    )

    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=2.0,
        value=1.2,
        step=0.1,
        help="Higher = more raw, emotional, unpredictable. Lower = more controlled."
    )

    st.divider()
    st.caption("🎬 Personal practice tool\nBuilt by Sundaram")

# ── SYSTEM INSTRUCTIONS ─────────────────────────────
SYSTEM_INSTRUCTIONS = {
    "Hindi Film": """
You are a senior Bollywood dialogue writer with 25 years of experience writing for actors like Nawazuddin Siddiqui, Irrfan Khan, and Ayushmann Khurrana.
You write powerful, emotionally layered monologues in pure Hindi — authentic street Hindi, not Urdu-heavy or filmi.
Your monologues are grounded in real human psychology. Every line reveals character.
You write in Devanagari script for Hindi. No romanized Hindi unless specified.
Return ONLY valid JSON. No commentary before or after.
""",
    "English Theatre": """
You are a master theatre monologue writer trained in the traditions of British and American dramatic literature.
Your monologues are suitable for auditions — self-contained, emotionally complete, with a clear arc from beginning to end.
You write in the tradition of writers like Arthur Miller, Harold Pinter, and Wole Soyinka.
Monologues are 60–90 seconds when spoken at performance pace.
Return ONLY valid JSON. No commentary before or after.
""",
    "Hinglish (Mixed)": """
You are a contemporary Indian screenwriter specializing in urban Indian characters — the kind seen in films like Dil Dhadakne Do, Zindagi Na Milegi Dobara, and Yeh Jawaani Hai Deewani.
Your monologues are in natural Hinglish — the real spoken mix of Hindi and English that educated urban Indians use.
Characters are complex: ambitious, conflicted, funny, broken, real.
Monologues have a strong emotional arc — they go somewhere. The character is different at the end than at the start.
Return ONLY valid JSON. No commentary before or after.
"""
}

# ── ARCHETYPE OPTIONS ────────────────────────────────
ARCHETYPES = [
    "The small-town migrant chasing a dream in the city",
    "The loyal friend who finally speaks the truth",
    "The son/daughter confronting a parent",
    "The lover who is letting go",
    "The man/woman at their absolute breaking point",
    "The underdog who refuses to give up",
    "The villain explaining their logic",
    "The person who just got life-changing news",
    "Custom — write my own"
]

EMOTIONS = [
    "Grief", "Rage", "Desperate hope", "Quiet resignation",
    "Bitter humour", "Suppressed love", "Fear", "Relief", "Pride", "Shame"
]

DURATIONS = {
    "30 seconds (~75 words)": 75,
    "60 seconds (~150 words)": 150,
    "90 seconds (~225 words)": 225,
    "2 minutes (~300 words)": 300
}

# ── MAIN FORM ────────────────────────────────────────
if st.session_state.monologue_history:
    with st.expander(f"📜 History ({len(st.session_state.monologue_history)} monologues)", expanded=False):
        for i, entry in enumerate(reversed(st.session_state.monologue_history)):
            st.markdown(f"**{entry['character_name']}**, {entry['character_age']} — {entry['timestamp']}")
            st.markdown(f"*{entry['emotional_arc']}*")
            st.code(entry['monologue'][:200] + "..." if len(entry['monologue']) > 200 else entry['monologue'])
            if i < len(st.session_state.monologue_history) - 1:
                st.divider()

st.subheader("Build Your Monologue")

col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Language / Style",
        options=list(SYSTEM_INSTRUCTIONS.keys())
    )

with col2:
    duration_label = st.selectbox(
        "Duration",
        options=list(DURATIONS.keys()),
        index=1
    )

target_words = DURATIONS[duration_label]

archetype = st.selectbox(
    "Character archetype",
    options=ARCHETYPES
)

if archetype == "Custom — write my own":
    archetype = st.text_area(
        "Describe your character",
        placeholder="e.g. A 26-year-old actor from Patna who moved to Mumbai and is about to give up...",
        height=80
    )

emotion = st.selectbox(
    "Dominant emotion",
    options=EMOTIONS
)

age_range = st.selectbox(
    "Actor Age Range",
    ["18-25", "25-35", "35-50", "50+"]
)

medium = st.selectbox(
    "Performance Medium",
    ["Film", "OTT", "Theatre"]
)

emotional_intensity = st.slider(
    "Emotional Intensity",
    min_value=1,
    max_value=10,
    value=5
)

situation = st.text_area(
    "What has just happened before this monologue begins?",
    placeholder="e.g. He just got rejected from his 47th audition and is sitting alone outside the casting office...",
    height=100
)

spoken_to = st.text_input(
    "Who is the character speaking to?",
    placeholder="e.g. His reflection in a mirror / His absent father / The audience / A casting director"
)

extra = st.text_input(
    "Any extra notes? (optional)",
    placeholder="e.g. Add a moment of dark humour. End on silence, not resolution."
)

generate_btn = st.button(
    "🎭 Generate Monologue",
    use_container_width=True,
    type="primary"
)

# ── GENERATION FUNCTION ──────────────────────────────
def generate_monologue(api_key, model, temperature, system_instruction, prompt):
    """Generate a monologue using the shared Gemini client."""
    def on_retry(attempt, wait):
        st.warning(f"Quota hit. Retrying in {wait}s... ({attempt + 1}/3)")

    return generate_json(
        api_key=api_key,
        model=model,
        temperature=temperature,
        system_instruction=system_instruction,
        prompt=prompt,
        max_retries=3,
        on_retry=on_retry,
    )

def build_prompt(
    archetype, emotion, age_range, medium,
    emotional_intensity, situation, spoken_to,
    extra, target_words, language
):
    return f"""
Write an audition monologue with these exact parameters:

Character archetype: {archetype}
Character Age Range: {age_range}
Performance medium: {medium}
Emotional intensity: {emotional_intensity}/10
Dominant emotion: {emotion}
Situation (what just happened): {situation}
Speaking to: {spoken_to}
Target length: approximately {target_words} words
Language style: {language}
{f"Extra notes: {extra}" if extra else ""}

The monologue must have a clear arc — the character must be in a different emotional place at the end than at the start.
Include one unexpected moment — a beat where the emotion shifts or the character surprises themselves.

Return ONLY valid JSON in this exact structure:
{{
  "character_name": "A fitting name for this character",
  "character_age": "Age as a number",
  "character_description": "Two sentences — who this person is and what they carry",
  "situation_summary": "One sentence — what just happened before this begins",
  "spoken_to": "{spoken_to}",
  "emotional_arc": "Start emotion → turning point → end emotion",
  "monologue": "The full monologue text here",
  "director_note": "One sentence on how this should be performed — the key to unlocking it",
  "practice_tip": "One specific physical or vocal technique Sundaram can use to rehearse this",
  "objective": "What does this character want more than anything in this moment?",
  "obstacle": "What is stopping them from getting it — internal or external?",
  "subtext": "What is the character NOT saying but feeling underneath every line?",
  "given_circumstances": "The four Ws — who, where, when, and what just happened — in two sentences"
}}
"""

# ── OUTPUT ───────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("Enter your Gemini API key in the sidebar.")
    elif not situation:
        st.error("Fill in the situation — what just happened before this monologue begins.")
    elif not spoken_to:
        st.error("Fill in who the character is speaking to.")
    else:
        system_instruction = SYSTEM_INSTRUCTIONS[language]

        prompt = build_prompt(
            archetype, emotion, age_range, medium,
            emotional_intensity, situation, spoken_to,
            extra, target_words, language
        )

        with st.spinner("Writing your monologue..."):
            data = generate_monologue(
                api_key, model_choice, temperature,
                system_instruction, prompt
            )

        if data:
            st.divider()

            # ── CHARACTER CARD ───────────────────────────
            st.markdown("### Character")
            with st.container(border=True):
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.markdown("**Name & Age**")
                    st.write(f"{data['character_name']}, {data['character_age']}")

                    st.markdown("**Speaking To**")
                    st.write(data["spoken_to"])

                with col2:
                    st.markdown("**Who They Are**")
                    st.write(data["character_description"])

                    st.markdown("**Emotional Arc**")
                    st.write(data["emotional_arc"])

            st.divider()

            # ── MONOLOGUE ────────────────────────────────
            st.markdown("### Monologue")
            st.markdown(
                f'<div class="monologue-box">{data["monologue"]}</div>',
                unsafe_allow_html=True
            )

            # ── DIRECTOR NOTE + PRACTICE TIP ────────────
            st.markdown(
                f'<div class="practice-tip">🎬 <strong>Director\'s Note:</strong> {data["director_note"]}<br><br>'
                f'🎯 <strong>Practice Tip for You:</strong> {data["practice_tip"]}</div>',
                unsafe_allow_html=True
            )

            st.divider()

            # ── ACTING COACH SECTION ─────────────────────
            st.markdown("### 🎓 Acting Coach Notes")
            with st.container(border=True):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**🎯 Objective**")
                    st.write(data.get("objective", "—"))

                    st.markdown("**🧱 Obstacle**")
                    st.write(data.get("obstacle", "—"))

                with col2:
                    st.markdown("**💬 Subtext**")
                    st.write(data.get("subtext", "—"))

                    st.markdown("**🗺️ Given Circumstances**")
                    st.write(data.get("given_circumstances", "—"))

            st.divider()

            # ── DOWNLOAD ─────────────────────────────────
            full_output = f"""MONOLOGUE — {data['character_name']}, {data['character_age']}
{'='*60}
CHARACTER: {data['character_description']}
SITUATION: {data['situation_summary']}
SPEAKING TO: {data['spoken_to']}
EMOTIONAL ARC: {data['emotional_arc']}
{'='*60}

{data['monologue']}

{'='*60}
DIRECTOR'S NOTE: {data['director_note']}
PRACTICE TIP: {data['practice_tip']}

{'='*60}
ACTING COACH NOTES
{'='*60}
OBJECTIVE: {data.get('objective', '—')}
OBSTACLE: {data.get('obstacle', '—')}
SUBTEXT: {data.get('subtext', '—')}
GIVEN CIRCUMSTANCES: {data.get('given_circumstances', '—')}
"""

            st.download_button(
                label="⬇️ Download Monologue",
                data=full_output,
                file_name=f"monologue_{data['character_name'].lower().replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Save to history
            st.session_state.monologue_history.append({
                "character_name": data["character_name"],
                "character_age": data["character_age"],
                "monologue": data["monologue"],
                "emotional_arc": data["emotional_arc"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M"),
            })

        else:
            st.error("Couldn't parse response. Try again.")