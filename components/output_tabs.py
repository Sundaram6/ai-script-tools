"""Output tabs component for Monologue Generator."""

import streamlit as st

from components.downloads import (
    copy_monologue,
    copy_full_output,
    download_monologue_txt,
    download_full_output_txt,
)


_MONOLOGUE_CSS = """
<style>
/* --- Monologue reading experience --- */
.monologue-reader {
    max-width: 680px;
    margin: 0 auto;
    padding: 1.5rem 2rem;
    background: #1a1a2e;
    border-radius: 8px;
    border-left: 4px solid #e94560;
}
.monologue-reader p,
.monologue-reader .monologue-text {
    font-size: 1.25rem;
    line-height: 1.9;
    letter-spacing: 0.02em;
    color: #e0e0e0;
    white-space: pre-wrap;
}

/* --- Emotional beat vertical progression --- */
.beat-progress {
    display: flex;
    flex-direction: column;
    gap: 0;
    max-width: 520px;
    margin: 1rem auto;
}
.beat-step {
    display: flex;
    align-items: stretch;
}
.beat-line {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 36px;
    flex-shrink: 0;
}
.beat-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.85rem;
    color: #fff;
    flex-shrink: 0;
    z-index: 1;
}
.beat-connector {
    width: 2px;
    flex-grow: 1;
    min-height: 20px;
    background: #444;
}
.beat-card {
    flex: 1;
    background: #16213e;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin: 0.35rem 0;
    border-left: 3px solid #e94560;
}
.beat-label {
    font-weight: 700;
    font-size: 0.95rem;
    color: #e94560;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.beat-text {
    font-size: 0.9rem;
    color: #ccc;
    margin-top: 0.25rem;
}

/* --- Performance notes cards --- */
.perf-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 0.5rem;
}
.perf-card {
    background: #16213e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    border-top: 3px solid #e94560;
}
.perf-card-header {
    font-weight: 700;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #e94560;
    margin-bottom: 0.4rem;
}
.perf-card-body {
    font-size: 0.95rem;
    color: #ddd;
    line-height: 1.5;
}
</style>
"""

_BEAT_COLORS = ["#e94560", "#f58840", "#f5d142", "#42b883", "#5c7cfa"]
_BEAT_LABELS = [
    "Vulnerability",
    "Resistance",
    "Anger",
    "Collapse",
    "Acceptance",
]


def render_output_tabs(inputs: dict, parsed_content: dict):
    """Render the output workspace with 5 tabs.

    Args:
        inputs: Dictionary of user inputs.
        parsed_content: Parsed content from response.
    """
    st.markdown(_MONOLOGUE_CSS, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎬 Monologue",
        "🧠 Character Breakdown",
        "🎭 Emotional Beats",
        "🎤 Performance Notes",
        "📄 Full Output",
    ])

    with tab1:
        _render_monologue(parsed_content)

    with tab2:
        _render_breakdown(parsed_content)

    with tab3:
        _render_beats(parsed_content)

    with tab4:
        _render_performance_notes(parsed_content)

    with tab5:
        _render_full_output(parsed_content)


def _render_monologue(parsed_content: dict):
    monologue = parsed_content.get("monologue", {})
    if not monologue:
        st.info("No monologue generated.")
        return

    text = monologue.get("text", "No text generated")
    st.markdown(
        f'<div class="monologue-reader"><div class="monologue-text">{text}</div></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        copy_monologue(text)
    with col2:
        download_monologue_txt(text)


def _render_breakdown(parsed_content: dict):
    breakdown = parsed_content.get("character_breakdown", {})
    if not breakdown:
        st.info("No character breakdown available.")
        return

    st.subheader("Character Breakdown")
    for key in ["objective", "obstacle", "stakes", "secret", "animal_reference"]:
        label = key.replace("_", " ").title()
        st.write(f"**{label}:** {breakdown.get(key, 'N/A')}")

    traits = breakdown.get("five_defining_traits", [])
    if traits:
        st.write("**Five Defining Traits:**")
        for trait in traits:
            st.write(f"  - {trait}")


def _render_beats(parsed_content: dict):
    beats = parsed_content.get("emotional_beats", {})
    if not beats:
        st.info("No emotional beats available.")
        return

    st.subheader("Emotional Beats")

    beat_keys = list(beats.keys())
    html_parts = ['<div class="beat-progress">']

    for idx, key in enumerate(beat_keys):
        label = _BEAT_LABELS[idx] if idx < len(_BEAT_LABELS) else key.replace("_", " ").title()
        color = _BEAT_COLORS[idx % len(_BEAT_COLORS)]
        is_last = idx == len(beat_keys) - 1

        html_parts.append('<div class="beat-step">')
        html_parts.append('<div class="beat-line">')
        html_parts.append(
            f'<div class="beat-dot" style="background:{color};">{idx + 1}</div>'
        )
        if not is_last:
            html_parts.append(
                f'<div class="beat-connector" style="background:{color}55;"></div>'
            )
        html_parts.append("</div>")  # beat-line
        html_parts.append(
            f'<div class="beat-card" style="border-left-color:{color};">'
            f'<div class="beat-label" style="color:{color};">{label}</div>'
            f'<div class="beat-text">{beats[key]}</div>'
            f"</div>"
        )
        html_parts.append("</div>")  # beat-step

    html_parts.append("</div>")
    st.markdown("\n".join(html_parts), unsafe_allow_html=True)


def _render_performance_notes(parsed_content: dict):
    notes = parsed_content.get("performance_notes", {})
    if not notes:
        st.info("No performance notes available.")
        return

    st.subheader("Performance Notes")

    card_fields = [
        ("voice", "Voice"),
        ("pacing", "Pacing"),
        ("body_language", "Body Language"),
        ("eye_focus", "Eye Focus"),
        ("breathing_notes", "Breathing"),
    ]

    # Build two-column grid
    html_parts = ['<div class="perf-grid">']
    for field_key, label in card_fields:
        value = notes.get(field_key, "N/A")
        html_parts.append(
            '<div class="perf-card">'
            f'<div class="perf-card-header">{label}</div>'
            f'<div class="perf-card-body">{value}</div>'
            "</div>"
        )
    html_parts.append("</div>")
    st.markdown("\n".join(html_parts), unsafe_allow_html=True)


def _render_full_output(parsed_content: dict):
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

        col1, col2 = st.columns(2)
        with col1:
            copy_full_output(parsed_content)
        with col2:
            download_full_output_txt(parsed_content)
    else:
        st.info("No output available.")