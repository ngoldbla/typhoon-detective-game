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

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🎮 Navigation")

        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()

        if st.button("📋 All Cases", use_container_width=True):
            st.session_state.current_page = 'cases'
            st.rerun()

        if st.button("➕ New Case", use_container_width=True):
            st.session_state.current_page = 'new_case'
            st.rerun()

        st.markdown("---")
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

        st.metric("Total Cases", total_cases)
        st.metric("Solved Cases", solved_cases)

        if total_cases > 0:
            st.progress(solved_cases / total_cases)

    # Main content area - route to different pages
    if st.session_state.current_page == 'home':
        show_home_page()
    elif st.session_state.current_page == 'cases':
        show_cases_page()
    elif st.session_state.current_page == 'new_case':
        show_new_case_page()
    elif st.session_state.current_page == 'case_details':
        show_case_details_page()
    elif st.session_state.current_page == 'suspect_interview':
        show_suspect_interview_page()
    elif st.session_state.current_page == 'clue_examination':
        show_clue_examination_page()
    elif st.session_state.current_page == 'solve_case':
        show_solve_case_page()
    elif st.session_state.current_page == 'how_to_play':
        show_how_to_play_page()

def show_home_page():
    """Display the home page"""
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
                    st.session_state.current_page = 'case_details'
                    st.session_state.selected_case_id = active_case['id']
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🆕 Start New Case", use_container_width=True):
                st.session_state.current_page = 'new_case'
                st.rerun()

        with col_b:
            if st.button("📚 How to Play", use_container_width=True):
                st.session_state.current_page = 'how_to_play'
                st.rerun()

def show_cases_page():
    """Display all cases"""
    st.markdown('<h2 class="sub-header">📋 All Cases</h2>', unsafe_allow_html=True)

    if not st.session_state.cases:
        st.info("No cases yet! Start a new case to begin your detective journey.")
        if st.button("Create Your First Case"):
            st.session_state.current_page = 'new_case'
            st.rerun()
        return

    # Search and filter
    search = st.text_input("🔍 Search cases...", placeholder="Enter case title or description")

    # Display cases
    for case in st.session_state.cases:
        if search.lower() in case['title'].lower() or search.lower() in case['description'].lower():
            with st.container():
                st.markdown('<div class="comic-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([3, 1])

                with col1:
                    status = "✅ SOLVED" if case.get('solved', False) else "🔍 ACTIVE"
                    st.markdown(f"### {case['title']} {status}")
                    st.markdown(f"_{case['description'][:200]}..._")

                    # Show progress
                    total_clues = len(case.get('clues', []))
                    examined = len([c for c in case.get('clues', []) if c['id'] in st.session_state.examined_clues])
                    total_suspects = len(case.get('suspects', []))
                    interviewed = len([s for s in case.get('suspects', []) if s['id'] in st.session_state.interviewed_suspects])

                    st.markdown(f"🧩 Clues: {examined}/{total_clues} | 👥 Suspects: {interviewed}/{total_suspects}")

                with col2:
                    if st.button("View Case", key=f"view_{case['id']}", use_container_width=True):
                        st.session_state.current_page = 'case_details'
                        st.session_state.selected_case_id = case['id']
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

def show_new_case_page():
    """Page for creating a new case"""
    st.markdown('<h2 class="sub-header">➕ Generate New Case</h2>', unsafe_allow_html=True)

    st.info("⚠️ This feature requires OpenAI API integration. Set up the Python libraries first.")

    with st.form("new_case_form"):
        st.markdown("### 🎨 Customize Your Mystery")

        difficulty = st.select_slider(
            "Difficulty Level",
            options=["very_easy", "easy", "medium"],
            value="easy"
        )

        theme = st.selectbox(
            "Theme",
            options=["school", "home", "playground", "pet", "toy", "random"],
            index=5
        )

        location = st.text_input("Location (optional)", placeholder="e.g., Elementary School")

        time_of_day = st.selectbox(
            "Time of Day",
            options=["morning", "afternoon", "evening", "random"],
            index=3
        )

        submitted = st.form_submit_button("🎲 Generate Mystery", use_container_width=True)

        if submitted:
            st.warning("Case generation requires implementing the OpenAI integration in the next steps.")
            # Placeholder for now
            st.session_state.current_page = 'cases'
            st.rerun()

def show_case_details_page():
    """Display detailed case information"""
    case_id = st.session_state.get('selected_case_id')
    if not case_id:
        st.error("No case selected")
        return

    case = next((c for c in st.session_state.cases if c['id'] == case_id), None)
    if not case:
        st.error("Case not found")
        return

    st.markdown(f'<h2 class="sub-header">{case["title"]}</h2>', unsafe_allow_html=True)

    # Case description
    st.markdown('<div class="comic-card">', unsafe_allow_html=True)
    st.markdown("### 📖 Case Description")
    st.markdown(case['description'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🧩 Clues", "👥 Suspects", "✅ Solve"])

    with tab1:
        st.markdown("### 🧩 Clues")
        for clue in case.get('clues', []):
            with st.container():
                st.markdown('<div class="suspect-card">', unsafe_allow_html=True)
                st.markdown(f"**{clue['description']}**")

                if clue['id'] in st.session_state.examined_clues:
                    st.success("✓ Examined")
                else:
                    if st.button("🔍 Examine Clue", key=f"examine_{clue['id']}"):
                        st.session_state.current_page = 'clue_examination'
                        st.session_state.selected_clue_id = clue['id']
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("### 👥 Suspects")
        for suspect in case.get('suspects', []):
            with st.container():
                st.markdown('<div class="suspect-card">', unsafe_allow_html=True)
                st.markdown(f"**{suspect['name']}** - {suspect['role']}")
                st.markdown(f"_{suspect['alibi']}_")

                if suspect['id'] in st.session_state.interviewed_suspects:
                    st.success("✓ Interviewed")
                else:
                    if st.button("💬 Interview", key=f"interview_{suspect['id']}"):
                        st.session_state.current_page = 'suspect_interview'
                        st.session_state.selected_suspect_id = suspect['id']
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### ✅ Ready to Solve?")
        if st.button("Submit Solution", use_container_width=True):
            st.session_state.current_page = 'solve_case'
            st.rerun()

def show_suspect_interview_page():
    """Interview a suspect"""
    st.markdown('<h2 class="sub-header">💬 Suspect Interview</h2>', unsafe_allow_html=True)
    st.info("⚠️ This feature requires OpenAI API integration.")

def show_clue_examination_page():
    """Examine a clue"""
    st.markdown('<h2 class="sub-header">🔍 Clue Examination</h2>', unsafe_allow_html=True)
    st.info("⚠️ This feature requires OpenAI API integration.")

def show_solve_case_page():
    """Solve the case"""
    st.markdown('<h2 class="sub-header">✅ Solve the Case</h2>', unsafe_allow_html=True)
    st.info("⚠️ This feature requires OpenAI API integration.")

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
