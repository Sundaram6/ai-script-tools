"""Download and copy functionality for Monologue Generator."""

import streamlit as st


def copy_monologue(text: str) -> None:
    """Display a button to copy just the monologue text.

    Args:
        text: The monologue text to copy.
    """
    if st.button("📋 Copy Monologue", key="copy_monologue", help="Copy monologue text to clipboard"):
        st.session_state["copy_text"] = text
        st.toast("Monologue copied to clipboard!", icon="✅")


def copy_full_output(parsed_content: dict) -> None:
    """Display a button to copy all sections of the output.

    Args:
        parsed_content: The parsed content dictionary.
    """
    full_text = _format_full_output(parsed_content)
    if st.button("📋 Copy Full Output", key="copy_full_output", help="Copy all output sections to clipboard"):
        st.session_state["copy_text"] = full_text
        st.toast("Full output copied to clipboard!", icon="✅")


def download_monologue_txt(text: str, filename: str = "monologue.txt") -> None:
    """Display a download button for monologue in TXT format.

    Args:
        text: The monologue text to download.
        filename: The default filename for the download.
    """
    st.download_button(
        label="💾 Download TXT",
        data=text,
        file_name=filename,
        mime="text/plain",
        key="download_monologue_txt",
    )


def download_full_output_txt(parsed_content: dict, filename: str = "monologue_full_output.txt") -> None:
    """Display a download button for full output in TXT format.

    Args:
        parsed_content: The parsed content dictionary.
        filename: The default filename for the download.
    """
    full_text = _format_full_output(parsed_content)
    st.download_button(
        label="💾 Download Full TXT",
        data=full_text,
        file_name=filename,
        mime="text/plain",
        key="download_full_txt",
    )


def _format_full_output(parsed_content: dict) -> str:
    """Format all sections into a single text output.

    Args:
        parsed_content: The parsed content dictionary.

    Returns:
        Formatted string with all sections.
    """
    sections = []

    monologue = parsed_content.get("monologue", {})
    if monologue.get("text"):
        sections.append("=== MONOLOGUE ===\n")
        sections.append(monologue["text"])
        sections.append("\n")

    breakdown = parsed_content.get("character_breakdown", {})
    if breakdown:
        sections.append("\n=== CHARACTER BREAKDOWN ===\n")
        for key in ["objective", "obstacle", "stakes", "secret", "animal_reference"]:
            label = key.replace("_", " ").title()
            sections.append(f"{label}: {breakdown.get(key, 'N/A')}")
        traits = breakdown.get("five_defining_traits", [])
        if traits:
            sections.append("\nFive Defining Traits:")
            for trait in traits:
                sections.append(f"  - {trait}")
        sections.append("\n")

    beats = parsed_content.get("emotional_beats", {})
    if beats:
        sections.append("\n=== EMOTIONAL BEATS ===\n")
        for key, value in beats.items():
            label = key.replace("_", " ").title()
            sections.append(f"{label}: {value}")
        sections.append("\n")

    notes = parsed_content.get("performance_notes", {})
    if notes:
        sections.append("\n=== PERFORMANCE NOTES ===\n")
        for key in ["voice", "pacing", "body_language", "eye_focus", "breathing_notes"]:
            label = key.replace("_", " ").title()
            sections.append(f"{label}: {notes.get(key, 'N/A')}")
        sections.append("\n")

    return "".join(sections)
