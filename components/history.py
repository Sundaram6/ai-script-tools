"""History system for Monologue Generator."""

import streamlit as st


def init_history():
    """Initialize history in session state if not exists."""
    if "history" not in st.session_state:
        st.session_state.history = []


def add_to_history(inputs: dict, parsed_content: dict) -> None:
    """Add a generation to history (keep last 10).
    
    Args:
        inputs: The input parameters used for generation.
        parsed_content: The parsed output content.
    """
    init_history()
    
    entry = {
        "inputs": inputs.copy(),
        "parsed_content": parsed_content,
    }
    
    st.session_state.history.append(entry)
    
    # Keep only last 10
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[-10:]


def render_history_button():
    """Render history button in top-right corner."""
    init_history()
    
    # Create a container for the button in the top-right
    col1, col2 = st.columns([1, 0.2])
    with col2:
        if st.button("📜 History", key="history_button", help="View generation history"):
            st.session_state.show_history = not st.session_state.get("show_history", False)
            st.rerun()


def render_history_panel():
    """Render the history panel if enabled."""
    init_history()
    
    if not st.session_state.get("show_history", False):
        return
    
    if not st.session_state.history:
        st.info("No history yet. Generate some monologues to see them here!")
        return
    
    st.markdown("### 📜 Generation History")
    st.markdown(f"*Last {len(st.session_state.history)} generations*")
    
    for i, entry in enumerate(reversed(st.session_state.history)):
        idx = len(st.session_state.history) - i
        inputs = entry["inputs"]
        parsed = entry["parsed_content"]
        
        monologue_text = parsed.get("monologue", {}).get("text", "No monologue text")
        preview = monologue_text[:100] + "..." if len(monologue_text) > 100 else monologue_text
        
        with st.expander(f"#{idx} - {inputs.get('archetype', 'Unknown')} ({inputs.get('emotion', 'Unknown')})"):
            st.markdown(f"**Archetype:** {inputs.get('archetype', 'N/A')}")
            st.markdown(f"**Emotion:** {inputs.get('emotion', 'N/A')}")
            st.markdown(f"**Age:** {inputs.get('age_range', 'N/A')}")
            st.markdown(f"**Medium:** {inputs.get('medium', 'N/A')}")
            st.markdown("---")
            st.markdown(preview)
            
            if st.button(f"Load #{idx}", key=f"load_history_{idx}"):
                st.session_state.last_result = entry
                st.session_state.show_history = False
                st.rerun()


def get_history_count() -> int:
    """Get the number of items in history."""
    init_history()
    return len(st.session_state.history)