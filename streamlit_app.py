"""
Typhoon Detective Game - Streamlit Version
An AI-powered interactive detective mystery game for children (ages 7+)
"""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Typhoon Detective Game",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css = """
    <style>
    /* Comic book theme styles */
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

    .main-header {
        font-family: 'Bangers', cursive;
        color: #FFD700;
        font-size: 3rem;
        text-align: center;
        text-shadow: 3px 3px 0px #FF8E00, 6px 6px 0px #000;
        margin-bottom: 2rem;
    }

    .sub-header {
        font-family: 'Bangers', cursive;
        color: #FF8E00;
        font-size: 2rem;
        text-shadow: 2px 2px 0px #000;
    }

    .comic-card {
        background-color: #16213e;
        border: 4px solid #FFD700;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transform: rotate(-0.5deg);
        box-shadow: 5px 5px 0px rgba(0, 0, 0, 0.3);
    }

    .stButton>button {
        background-color: #FFD700;
        color: #1a1a2e;
        font-weight: bold;
        border: 3px solid #000;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        box-shadow: 3px 3px 0px #000;
        transition: all 0.2s;
    }

    .stButton>button:hover {
        transform: translate(2px, 2px);
        box-shadow: 1px 1px 0px #000;
    }

    .detective-badge {
        background: linear-gradient(135deg, #FFD700 0%, #FF8E00 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 2px solid #000;
        display: inline-block;
        font-weight: bold;
        color: #1a1a2e;
    }

    .clue-tag {
        background-color: #FF8E00;
        color: #fff;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        border: 2px solid #000;
        display: inline-block;
        margin: 0.2rem;
        font-size: 0.9rem;
    }

    .suspect-card {
        background-color: #0f3460;
        border: 3px solid #FFD700;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f3460;
        border-right: 4px solid #FFD700;
    }

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #FFD700;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.cases = []
        st.session_state.active_case_id = None
        st.session_state.language = 'en'
        st.session_state.current_page = 'home'
        st.session_state.clue_analyses = {}
        st.session_state.suspect_interviews = {}
        st.session_state.examined_clues = set()
        st.session_state.interviewed_suspects = set()

# Main app
def main():
    load_css()
    init_session_state()

    # Header
    st.markdown('<h1 class="main-header">🔍 TYPHOON DETECTIVE GAME 🔍</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        language = st.selectbox(
            "Language",
            options=['en', 'th'],
            format_func=lambda x: "🇺🇸 English" if x == 'en' else "🇹🇭 ไทย",
            index=0 if st.session_state.language == 'en' else 1
        )

        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Stats")
        total_cases = len(st.session_state.cases)
        solved_cases = len([c for c in st.session_state.cases if c.get('solved', False)])
        archived_cases = len([c for c in st.session_state.cases if c.get('archived', False)])
        active_cases = total_cases - archived_cases

        st.metric("Total Cases", total_cases)
        st.metric("Active Cases", active_cases)
        st.metric("Solved Cases", solved_cases)
        st.metric("Archived Cases", archived_cases)

        if total_cases > 0:
            st.progress(solved_cases / total_cases)

    # Main content - home page
    show_home_page()

def show_home_page():
    """Display the home page"""
    # Show how to play if requested
    if st.session_state.get('show_how_to_play', False):
        show_how_to_play_page()
        if st.button("← Back to Home"):
            st.session_state.show_how_to_play = False
            st.rerun()
        return

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="comic-card">', unsafe_allow_html=True)
        st.markdown("## Welcome, Detective! 🕵️")
        st.markdown("""
        Welcome to the **Typhoon Detective Game**! Put on your detective hat and solve
        mysterious cases using your sharp mind and AI-powered investigation tools.

        ### 🎯 What's New?
        - Solve child-friendly mysteries
        - Interview AI-powered suspects
        - Analyze clues with AI assistance
        - Track your detective progress
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Active case section
        if st.session_state.active_case_id:
            active_case = next(
                (c for c in st.session_state.cases if c['id'] == st.session_state.active_case_id),
                None
            )
            if active_case and not active_case.get('solved', False):
                st.markdown('<div class="comic-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 Continue Your Investigation")
                st.markdown(f"**{active_case['title']}**")
                st.markdown(f"_{active_case['description'][:150]}..._")

                if st.button("Continue Case", key="continue_case", use_container_width=True):
                    st.session_state.selected_case_id = active_case['id']
                    st.switch_page("pages/3_🔍_Case_Details.py")
                st.markdown('</div>', unsafe_allow_html=True)

        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🆕 Start New Case", use_container_width=True):
                st.switch_page("pages/1_🆕_New_Case.py")

        with col_b:
            if st.button("📚 How to Play", use_container_width=True):
                st.session_state.show_how_to_play = True
                st.rerun()


def show_how_to_play_page():
    """Show how to play instructions"""
    st.markdown('<h2 class="sub-header">📚 How to Play</h2>', unsafe_allow_html=True)

    st.markdown("""
    ### Welcome, Young Detective! 🕵️

    This game is designed to help you become an amazing detective! Here's how to play:

    #### 1️⃣ Start a New Case
    - Click "New Case" to generate a mystery
    - Choose the difficulty and theme you like

    #### 2️⃣ Investigate
    - **Examine Clues**: Look at all the clues carefully
    - **Interview Suspects**: Ask questions to find the truth
    - Use AI to help analyze what you find!

    #### 3️⃣ Solve the Mystery
    - Think about what you learned
    - Figure out who did it and why
    - Submit your solution!

    ### 🎯 Tips for Success
    - Examine ALL clues before solving
    - Interview ALL suspects
    - Look for connections between clues
    - Trust your detective instincts!

    ### 🏆 Have Fun!
    Remember, every great detective started somewhere. Keep practicing and you'll get better!
    """)

if __name__ == "__main__":
    main()
