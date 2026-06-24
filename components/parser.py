"""Response parser component for Monologue Generator."""

import json
import re


def parse_response(response_text: str) -> dict:
    """Parse Gemini response into sections.
    
    Attempts to extract structured sections from the response.
    Falls back to Full Output if parsing fails.
    
    Args:
        response_text: Raw response text from Gemini.
        
    Returns:
        Dictionary with keys:
        - character_profile: dict or None
        - character_breakdown: dict or None
        - monologue: dict or None
        - emotional_beats: dict or None
        - performance_notes: dict or None
        - full_output: str (always present)
    """
    result = {
        "character_profile": None,
        "character_breakdown": None,
        "monologue": None,
        "emotional_beats": None,
        "performance_notes": None,
        "full_output": response_text,
    }
    
    if not response_text:
        return result
    
    # Try to parse as JSON first
    try:
        data = json.loads(response_text)
        if isinstance(data, dict):
            # Direct mapping from JSON keys
            key_mapping = {
                "character_profile": "character_profile",
                "character_breakdown": "character_breakdown",
                "monologue": "monologue",
                "emotional_beats": "emotional_beats",
                "performance_notes": "performance_notes",
            }
            for json_key, result_key in key_mapping.items():
                if json_key in data:
                    result[result_key] = data[json_key]
            return result
    except (json.JSONDecodeError, TypeError):
        pass
    
    # Try to parse sections from markdown-like text
    lines = response_text.split("\n")
    current_section = None
    section_content = []
    
    # Define section markers (case-insensitive)
    section_markers = {
        "character_profile": ["character profile", "character_profile"],
        "character_breakdown": ["character breakdown", "character_breakdown"],
        "monologue": ["monologue"],
        "emotional_beats": ["emotional beats", "emotional_beats"],
        "performance_notes": ["performance notes", "performance_notes"],
    }
    
    for line in lines:
        stripped = line.strip()
        lower_stripped = stripped.lower()
        
        # Check for section headers (lines starting with #)
        if stripped.startswith("#"):
            # Save previous section
            if current_section and section_content:
                result[current_section] = _parse_section_content(
                    current_section, "\n".join(section_content)
                )
                section_content = []
            
            # Identify new section
            current_section = None
            for section_key, markers in section_markers.items():
                for marker in markers:
                    if marker in lower_stripped:
                        current_section = section_key
                        break
                if current_section:
                    break
        elif current_section:
            section_content.append(line)
    
    # Save last section
    if current_section and section_content:
        result[current_section] = _parse_section_content(
            current_section, "\n".join(section_content)
        )
    
    # If no sections found, treat entire response as monologue
    if all(v is None for k, v in result.items() if k != "full_output"):
        result["monologue"] = {"text": response_text.strip()}
    
    return result


def _parse_section_content(section_type: str, content: str) -> dict:
    """Parse raw section content into structured dict.
    
    Args:
        section_type: Type of section (e.g., 'character_profile').
        content: Raw text content of the section.
        
    Returns:
        Parsed dictionary for the section.
    """
    content = content.strip()
    
    if section_type == "monologue":
        return {"text": content}
    
    # For other sections, try to parse key-value pairs
    result = {}
    current_key = None
    current_value_lines = []
    
    for line in content.split("\n"):
        stripped = line.strip()
        
        # Check for key: value pattern
        match = re.match(r"^\*\*(.+?)\*\*:?\s*(.*)$", stripped)
        if match:
            # Save previous key-value
            if current_key:
                result[current_key] = "\n".join(current_value_lines).strip()
            current_key = match.group(1).strip().lower().replace(" ", "_")
            current_value_lines = [match.group(2).strip()]
        elif current_key and stripped:
            current_value_lines.append(stripped)
    
    # Save last key-value
    if current_key:
        result[current_key] = "\n".join(current_value_lines).strip()
    
    # Handle list items for certain sections
    if section_type == "character_breakdown" and "five_defining_traits" in result:
        traits_text = result["five_defining_traits"]
        traits = [line.strip().lstrip("- ") for line in traits_text.split("\n") if line.strip().startswith("-")]
        if traits:
            result["five_defining_traits"] = traits
    
    return result if result else {"raw": content}