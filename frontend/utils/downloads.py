"""Download and copy functionality for Monologue Generator."""

import streamlit as st
from fpdf import FPDF


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

    monologue = parsed_content.get("monologue") or {}
    if monologue.get("text"):
        sections.append("=== MONOLOGUE ===\n")
        sections.append(monologue["text"])
        sections.append("\n")

    breakdown = parsed_content.get("character_breakdown") or {}
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

    beats = parsed_content.get("emotional_beats") or {}
    if beats:
        sections.append("\n=== EMOTIONAL BEATS ===\n")
        for key, value in beats.items():
            label = key.replace("_", " ").title()
            sections.append(f"{label}: {value}")
        sections.append("\n")

    notes = parsed_content.get("performance_notes") or {}
    if notes:
        sections.append("\n=== PERFORMANCE NOTES ===\n")
        for key in ["voice", "pacing", "body_language", "eye_focus", "breathing_notes"]:
            label = key.replace("_", " ").title()
            sections.append(f"{label}: {notes.get(key, 'N/A')}")
        sections.append("\n")

    return "".join(sections)


def download_monologue_pdf(text: str, filename: str = "monologue.pdf") -> None:
    """Display a download button for monologue in PDF format.
    
    Args:
        text: The monologue text to download.
        filename: The default filename for the download.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Monologue", ln=True, align="C")
    pdf.ln(10)
    
    # Add monologue text
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    
    st.download_button(
        label="📄 Download PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        key="download_monologue_pdf",
    )


def download_full_output_pdf(parsed_content: dict, filename: str = "monologue_full_output.pdf") -> None:
    """Display a download button for full output in PDF format.
    
    Args:
        parsed_content: The parsed content dictionary.
        filename: The default filename for the download.
    """
    full_text = _format_full_output(parsed_content)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, txt="Monologue - Full Output", ln=True, align="C")
    pdf.ln(10)
    
    # Add full output text
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=full_text)
    
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    
    st.download_button(
        label="📄 Download Full PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        key="download_full_pdf",
    )


def render_generate_another_button():
    """Render a button to generate another version."""
    if st.button("🔄 Generate Another Version", key="generate_another", 
                 help="Generate another version with same settings"):
        st.session_state.generate_another = True
        st.rerun()
