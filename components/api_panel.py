"""API key management and demo mode for Monologue Generator."""

import streamlit as st

from utils.parser import parse_response

DEMO_MONOLOGUES = [
    {
        "archetype": "Hero",
        "emotion": "Hope",
        "age_range": "Young Adult",
        "medium": "Film",
        "language": "English",
        "intensity": 7,
        "situation": "Standing before a broken army, rallying them for one final battle against overwhelming odds.",
        "spoken_to": "Fellow soldiers",
        "word_count": 250,
        "monologue": (
            "I know what you're thinking. You're thinking we're finished.\n\n"
            "You look out at this field and see graves. I see the reason we fight.\n\n"
            "Every scar on my body tells a story of someone who believed the world "
            "could be better. My father died believing it. My mother raised me on that belief.\n\n"
            "They want us to kneel. They want us to forget who we are. But I've tasted "
            "freedom, and I'll be damned if I swallow it back down.\n\n"
            "So stand up. Pick up your swords. Not because victory is promised — it isn't — "
            "but because surrender is death. And I'd rather die on my feet than live on my knees.\n\n"
            "Tomorrow, we ride. Not for glory. Not for gold. For every soul that can't fight for itself.\n\n"
            "That's what heroes do. We fight when no one else will."
        ),
    },
    {
        "archetype": "Villain",
        "emotion": "Grief",
        "age_range": "Adult",
        "medium": "Film",
        "language": "English",
        "intensity": 9,
        "situation": "Alone in a dark room after learning their child was killed in the crossfire of their own war.",
        "spoken_to": "Themselves",
        "word_count": 250,
        "monologue": (
            "They told me the cost of power was everything.\n\n"
            "I laughed. I thought they meant sacrifice — time, comfort, allies.\n\n"
            "I didn't know they meant my little girl would die because I chose pride over peace.\n\n"
            "She used to bring me flowers from the garden. Wild ones. She said they were magic, "
            "that they could heal anything. I should have believed her.\n\n"
            "Now I sit here with blood on my hands that no amount of washing will remove. "
            "I built an empire on a foundation of bones, and tonight I finally counted them.\n\n"
            "There's no redemption for what I am. No forgiveness waiting at the end.\n\n"
            "But I'll tell you this — whoever told my daughter to run, whoever pulled that trigger, "
            "they'll learn what a father's grief looks like. And it looks like the end of their world."
        ),
    },
    {
        "archetype": "Comedian",
        "emotion": "Joy",
        "age_range": "Young Adult",
        "medium": "Theatre",
        "language": "English",
        "intensity": 4,
        "situation": "Performing stand-up for the first time at a small open mic night, discovering they love making people laugh.",
        "spoken_to": "Audience",
        "word_count": 250,
        "monologue": (
            "Okay, okay — so this is terrifying. Standing up here with a microphone is basically "
            "public speaking with better lighting.\n\n"
            "My therapist said I should 'put myself out there.' I said, 'Doc, the last time I put "
            "myself out there, I got rejected by a Roomba.'\n\n"
            "A Roomba. It literally turned around and went the other direction. I felt that.\n\n"
            "But you know what? You're laughing. And that... that feels like the opposite of every "
            "bad date I've ever been on. Which is all of them.\n\n"
            "Dating apps are just job interviews where nobody reads your resume. 'Tell me about "
            "yourself.' Ma'am, I'm here for a margarita, not a performance review.\n\n"
            "But right now? Right here? This is the first time in my life I've felt like I belong "
            "somewhere that isn't my couch.\n\n"
            "So thank you for laughing. Seriously. You just made a broken person feel whole. "
            "And that's the best joke I've told all night."
        ),
    },
    {
        "archetype": "Lover",
        "emotion": "Love",
        "age_range": "Adult",
        "medium": "OTT",
        "language": "Hinglish",
        "intensity": 8,
        "situation": "Confessing love to their best friend at a wedding, realizing they've been in love all along.",
        "spoken_to": "Best friend",
        "word_count": 250,
        "monologue": (
            "Tumhe pata hai, aaj maine dekha ki tumne kitni der tak us ladki ko dekha.\n"
            "Aur maine socha — kabhi kisi ne mujhe aise dekha hai?\n\n"
            "Phir mujhe yaad aaya — haan, tumne dekha hai. Jab main roti thi, jab main "
            "pagal ho rahi thi, jab main khud pe bharosa kho rahi thi. Tum wahan the.\n\n"
            "Aur main tumhe chupke se pyaar karti rahi. Chupke se. Kyunki tumhari dosti "
            "itni keemti hai ki main khatam nahi kar sakti.\n\n"
            "Lekin aaj jab tum muskuraye us ladki ke liye, tab mujhe laga ki agar maine "
            "aaj nahi boli, toh kal bohot der ho jayegi.\n\n"
            "Tum mera sabse khaas dost ho. Aur agar tum mujhe nahi chaahte, toh bhi theek hai. "
            "Main theek rahungi. Par ek baar keh doon — pyaar karta hoon tumse. Haan, us tarah.\n\n"
            "Ab bolo. Kya tum bhi?"
        ),
    },
    {
        "archetype": "Mentor",
        "emotion": "Regret",
        "age_range": "Elderly",
        "medium": "Film",
        "language": "English",
        "intensity": 6,
        "situation": "Apologizing to a former student for pushing them too hard, after seeing them succeed despite the pressure.",
        "spoken_to": "Former student",
        "word_count": 250,
        "monologue": (
            "You know, I've spent thirty years teaching kids like you. And I thought I knew "
            "what I was doing.\n\n"
            "I pushed you because I saw something in you. talent. Fire. The kind of thing that "
            "doesn't come along twice. And I told myself the harshness was necessary.\n\n"
            "But I was wrong.\n\n"
            "You didn't succeed because of my methods. You succeeded in spite of them. "
            "And that's on me.\n\n"
            "I watched your film last night. You've surpassed everything I ever taught you. "
            "Everything I thought I knew about this craft, you've gone beyond it.\n\n"
            "And I owe you an apology. For the nights you cried. For the doubt I planted. "
            "For making you feel like you were never enough.\n\n"
            "You were always enough. I was just too proud to see it.\n\n"
            "Go make your masterpiece, kid. And don't let anyone — especially not a stubborn "
            "old teacher — tell you what you can't do."
        ),
    },
]


def get_api_key():
    """Retrieve the API key from session state."""
    return st.session_state.get("gemini_api_key", "")


def render_api_panel():
    """Render the API key panel in the sidebar.

    Returns the current API key (string).
    """
    api_key = get_api_key()

    with st.sidebar:
        st.header("API Key")
        new_key = st.text_input(
            "Gemini API Key",
            value=api_key,
            type="password",
            help="Get your API key from https://aistudio.google.com/apikey",
            key="api_key_input",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save Key", use_container_width=True):
                if new_key:
                    st.session_state.gemini_api_key = new_key
                    st.success("Key saved!")
                else:
                    st.warning("Enter a key first.")
        with col2:
            if api_key and st.button("Clear Key", use_container_width=True):
                st.session_state.gemini_api_key = ""
                st.rerun()

    return new_key if new_key else api_key


def render_demo_mode():
    """Render demo mode selector and return selected sample dict or None."""
    with st.sidebar:
        st.divider()
        st.subheader("Demo Mode")
        st.caption("No API key? Try sample monologues without calling Gemini.")
        demo_idx = st.selectbox(
            "Choose a demo",
            range(len(DEMO_MONOLOGUES)),
            format_func=lambda i: (
                f"{DEMO_MONOLOGUES[i]['archetype']} — {DEMO_MONOLOGUES[i]['emotion']}"
            ),
        )

    if st.button("Try Demo Example", type="primary", use_container_width=True):
        return DEMO_MONOLOGUES[demo_idx]
    return None
