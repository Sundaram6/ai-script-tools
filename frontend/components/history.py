"""History system for Monologue Generator."""

import streamlit as st
from services import api_client

def init_history():
    """No longer needed, backend manages history."""
    pass

def add_to_history(inputs: dict, parsed_content: dict) -> None:
    """No longer needed, backend manages history."""
    pass

def render_history_button():
    """Render history button in top-right corner."""
    col1, col2 = st.columns([1, 0.2])
    with col2:
        if st.button("📜 History", key="history_button", help="View generation history"):
            st.session_state.show_history = not st.session_state.get("show_history", False)
            st.rerun()

def render_history_panel():
    """Render the history panel if enabled."""
    if not st.session_state.get("show_history", False):
        return
    
    history_items = api_client.get_history(limit=10)
    
    if not history_items:
        st.info("No history yet. Generate some monologues to see them here!")
        return
    
    st.markdown("### 📜 Generation History")
    st.markdown(f"*Last {len(history_items)} generations*")
    
    for i, entry in enumerate(history_items):
        idx = entry.get('id', i)
        
        monologue_text = entry.get("monologue", "No monologue text")
        preview = monologue_text[:100] + "..." if len(monologue_text) > 100 else monologue_text
        
        with st.expander(f"#{idx} - {entry.get('character_name', 'Unknown')}"):
            st.markdown(f"**Gender:** {entry.get('gender', 'N/A')}")
            st.markdown(f"**Age:** {entry.get('age', 'N/A')}")
            st.markdown(f"**Language:** {entry.get('language', 'N/A')}")
            st.markdown(f"**Created:** {entry.get('created_at', 'N/A')}")
            st.markdown("---")
            st.markdown(preview)
            
            if st.button(f"Load #{idx}", key=f"load_history_{idx}"):
                # Reconstruct inputs and parsed_content for the app to display
                inputs = {
                    "gender": entry.get('gender', ''),
                    "age_range": entry.get('age', ''),
                    "language": entry.get('language', ''),
                }
                parsed_content = {
                    "character_profile": {"name": entry.get("character_name", "")},
                    "monologue": {"text": entry.get("monologue", "")},
                    "performance_notes": {"voice": entry.get("acting_notes", "")}
                }
                st.session_state.last_result = {
                    "inputs": inputs,
                    "parsed_content": parsed_content
                }
                st.session_state.show_history = False
                st.rerun()

def get_history_count() -> int:
    """Get the number of items in history."""
    items = api_client.get_history(limit=1)
    return 1 if items else 0