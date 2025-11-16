"""
Emerson's Detective Game - AI-Powered Mystery Solving for Kids
An interactive detective game powered by OpenAI
"""

import streamlit as st
from lib.database import get_all_cases, get_examined_clues, get_interviewed_suspects

# Page configuration with custom branding
st.set_page_config(
    page_title="Emerson's Detective Game",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Emerson's Detective Game\nSolve mysteries with AI assistance!"
    }
)


def load_custom_css():
    """Load custom CSS for light theme with proper branding"""
    st.markdown("""
    <style>
    /* Import fun fonts for the detective game */
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

    /* Light theme base colors */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #F7931E;
        --accent-color: #FDC830;
        --bg-light: #FFF9F0;
        --bg-white: #FFFFFF;
        --text-dark: #2C3E50;
        --text-medium: #5D6D7E;
        --border-color: #E8DCC4;
        --shadow: rgba(0, 0, 0, 0.1);
    }

    /* Main container styling */
    .main {
        background-color: var(--bg-light);
        background-image:
            repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.05) 10px, rgba(255,255,255,.05) 20px);
    }

    /* Header styles */
    .main-header {
        font-family: 'Bangers', cursive;
        color: var(--primary-color);
        font-size: clamp(2rem, 6vw, 4rem);
        text-align: center;
        text-shadow:
            3px 3px 0px var(--secondary-color),
            5px 5px 0px var(--accent-color);
        margin: 1rem 0;
        line-height: 1.1;
        letter-spacing: 2px;
    }

    .sub-header {
        font-family: 'Bangers', cursive;
        color: var(--secondary-color);
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        text-shadow: 2px 2px 0px var(--accent-color);
        margin: 0.5rem 0;
    }

    /* Card styles for light theme */
    .detective-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF9F0 100%);
        border: 4px solid var(--primary-color);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow:
            5px 5px 0px var(--secondary-color),
            10px 10px 20px var(--shadow);
        transition: transform 0.2s;
    }

    .detective-card:hover {
        transform: translateY(-2px);
        box-shadow:
            7px 7px 0px var(--secondary-color),
            12px 12px 25px var(--shadow);
    }

    /* Button styling for light theme */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        font-size: 1.1rem;
        border: 3px solid var(--text-dark);
        border-radius: 10px;
        padding: 0.75rem 2rem;
        box-shadow: 4px 4px 0px var(--text-dark);
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px var(--text-dark);
    }

    .stButton>button:active {
        transform: translate(4px, 4px);
        box-shadow: none;
    }

    /* Badge styling */
    .detective-badge {
        background: linear-gradient(135deg, var(--accent-color) 0%, var(--secondary-color) 100%);
        color: var(--text-dark);
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        border: 3px solid var(--text-dark);
        display: inline-block;
        font-weight: bold;
        font-family: 'Comic Neue', cursive;
        font-size: 1rem;
        box-shadow: 3px 3px 0px var(--text-dark);
        margin: 0.25rem;
    }

    /* Clue tag styling */
    .clue-tag {
        background-color: var(--secondary-color);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        border: 2px solid var(--text-dark);
        display: inline-block;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: bold;
        box-shadow: 2px 2px 0px var(--text-dark);
    }

    /* Sidebar styling for light theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFF9F0 0%, #FFE8CC 100%);
        border-right: 4px solid var(--primary-color);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-dark);
    }

    /* Metrics styling */
    [data-testid="metric-container"] {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        border: 3px solid var(--primary-color);
        box-shadow: 3px 3px 0px var(--secondary-color);
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: var(--primary-color);
        font-weight: bold;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-medium);
        font-weight: bold;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 3px solid var(--primary-color);
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1rem;
        font-weight: bold;
        color: var(--text-dark);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-light);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: white;
        border: 3px solid var(--border-color);
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        color: var(--text-dark);
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border: 3px solid var(--primary-color);
        border-radius: 10px;
        font-weight: bold;
        color: var(--text-dark);
    }

    .streamlit-expanderHeader:hover {
        background-color: var(--bg-light);
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 10px;
        border: 3px solid;
        padding: 1rem;
    }

    /* Success alerts */
    [data-baseweb="notification"][kind="success"] {
        background-color: #D4EDDA;
        border-color: #28A745;
    }

    /* Info alerts */
    [data-baseweb="notification"][kind="info"] {
        background-color: #D1ECF1;
        border-color: #17A2B8;
    }

    /* Warning alerts */
    [data-baseweb="notification"][kind="warning"] {
        background-color: #FFF3CD;
        border-color: #FFC107;
    }

    /* Error alerts */
    [data-baseweb="notification"][kind="error"] {
        background-color: #F8D7DA;
        border-color: #DC3545;
    }

    /* Mobile optimizations */
    @media screen and (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            text-shadow:
                2px 2px 0px var(--secondary-color),
                3px 3px 0px var(--accent-color);
        }

        .detective-card {
            padding: 1rem;
            border: 3px solid var(--primary-color);
            box-shadow: 3px 3px 0px var(--secondary-color);
        }

        .stButton>button {
            width: 100%;
            font-size: 1rem;
            padding: 0.75rem 1rem;
        }

        [data-testid="column"] {
            padding: 0.25rem !important;
        }

        /* Make images responsive */
        img {
            max-width: 100% !important;
            height: auto !important;
            border-radius: 10px;
        }
    }

    /* Tablet optimizations */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 3rem;
        }

        .detective-card {
            padding: 1.25rem;
        }
    }

    /* Image styling */
    img {
        border-radius: 15px;
        border: 4px solid var(--primary-color);
        box-shadow: 5px 5px 0px var(--secondary-color);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: var(--text-medium);
        font-family: 'Comic Neue', cursive;
        border-top: 3px solid var(--border-color);
    }
    </style>
    """, unsafe_allow_html=True)


def load_favicon_and_metadata():
    """Add custom favicon and metadata"""
    st.markdown("""
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔍</text></svg>">
    <meta name="description" content="Emerson's Detective Game - Solve mysteries with AI assistance. A fun, educational detective game for kids aged 7+">
    <meta name="keywords" content="detective game, mystery solving, AI game, educational game, kids game, interactive detective">
    <meta name="author" content="Emerson's Detective Game">
    <meta property="og:title" content="Emerson's Detective Game">
    <meta property="og:description" content="Solve exciting mysteries with AI assistance!">
    <meta property="og:type" content="website">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    """, unsafe_allow_html=True)


def init_session_state():
    """Initialize session state with database integration"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.active_case_id = None
        st.session_state.language = 'en'
        st.session_state.current_page = 'home'

        # Load cases from database
        st.session_state.cases = get_all_cases()


def show_home_page():
    """Display the home page"""
    # Show how to play if requested
    if st.session_state.get('show_how_to_play', False):
        show_how_to_play_page()
        if st.button("← Back to Home"):
            st.session_state.show_how_to_play = False
            st.rerun()
        return

    # Welcome section
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.markdown("""
        <div class="detective-card">
            <h2 style="color: #FF6B35; font-family: 'Comic Neue', cursive;">
                🕵️ Welcome, Detective! 🕵️
            </h2>
            <p style="font-size: 1.1rem; color: #2C3E50; font-family: 'Comic Neue', cursive;">
                Welcome to <strong>Emerson's Detective Game</strong>! Put on your detective hat
                and solve mysterious cases using your sharp mind and AI-powered investigation tools.
            </p>
            <h3 style="color: #F7931E; font-family: 'Comic Neue', cursive;">🎯 What You Can Do:</h3>
            <ul style="font-size: 1rem; color: #2C3E50; font-family: 'Comic Neue', cursive;">
                <li>✨ Solve child-friendly mysteries</li>
                <li>🤖 Interview AI-powered suspects</li>
                <li>🔬 Analyze clues with AI assistance</li>
                <li>📈 Track your detective progress</li>
                <li>🎨 Explore AI-generated mystery scenes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Active case section
        cases = get_all_cases()
        active_cases = [c for c in cases if not c.get('archived', False) and not c.get('solved', False)]

        if active_cases and st.session_state.active_case_id:
            active_case = next(
                (c for c in active_cases if c['id'] == st.session_state.active_case_id),
                None
            )
            if active_case:
                st.markdown("""
                <div class="detective-card">
                    <h3 style="color: #F7931E; font-family: 'Comic Neue', cursive;">
                        🎯 Continue Your Investigation
                    </h3>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"**{active_case['title']}**")
                st.markdown(f"_{active_case['description'][:150]}..._")

                # Show progress
                examined = len(get_examined_clues(active_case['id']))
                total_clues = len(active_case.get('clues', []))
                interviewed = len(get_interviewed_suspects(active_case['id']))
                total_suspects = len(active_case.get('suspects', []))

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f'<span class="detective-badge">🧩 {examined}/{total_clues} Clues</span>',
                              unsafe_allow_html=True)
                with col_b:
                    st.markdown(f'<span class="detective-badge">👥 {interviewed}/{total_suspects} Suspects</span>',
                              unsafe_allow_html=True)

                if st.button("🔍 Continue Case", key="continue_case", use_container_width=True):
                    st.session_state.selected_case_id = active_case['id']
                    st.switch_page("pages/3_🔍_Case_Details.py")

        # Quick actions
        st.markdown("<h3 style='color: #F7931E; font-family: \"Comic Neue\", cursive; margin-top: 2rem;'>🚀 Quick Actions</h3>",
                   unsafe_allow_html=True)

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("🆕 Start New Case", use_container_width=True, type="primary"):
                st.switch_page("pages/1_🆕_New_Case.py")

        with col_b:
            if st.button("📚 How to Play", use_container_width=True):
                st.session_state.show_how_to_play = True
                st.rerun()

        # Show recent cases if any
        if cases:
            st.markdown("<h3 style='color: #F7931E; font-family: \"Comic Neue\", cursive; margin-top: 2rem;'>📋 Your Cases</h3>",
                       unsafe_allow_html=True)

            if st.button("📋 View All Cases", use_container_width=True):
                st.switch_page("pages/2_📋_All_Cases.py")


def show_how_to_play_page():
    """Show how to play instructions"""
    st.markdown('<h2 class="sub-header">📚 How to Play Emerson\'s Detective Game</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="detective-card">
        <h3 style="color: #FF6B35; font-family: 'Comic Neue', cursive;">Welcome, Young Detective! 🕵️</h3>
        <p style="font-size: 1.1rem; font-family: 'Comic Neue', cursive;">
            This game is designed to help you become an amazing detective! Here's how to play:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="detective-card">
            <h4 style="color: #F7931E;">1️⃣ Start a New Case</h4>
            <ul style="font-family: 'Comic Neue', cursive;">
                <li>Click "🆕 New Case" to generate a mystery</li>
                <li>Choose the difficulty level you like</li>
                <li>Pick a fun theme (school, home, playground, etc.)</li>
                <li>Let AI create your unique mystery!</li>
            </ul>
        </div>

        <div class="detective-card">
            <h4 style="color: #F7931E;">2️⃣ Investigate Clues</h4>
            <ul style="font-family: 'Comic Neue', cursive;">
                <li>Examine all clues carefully</li>
                <li>Click "🔍 Examine" to analyze each clue</li>
                <li>AI will help you understand what they mean</li>
                <li>Look for connections between clues</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="detective-card">
            <h4 style="color: #F7931E;">3️⃣ Interview Suspects</h4>
            <ul style="font-family: 'Comic Neue', cursive;">
                <li>Talk to each suspect</li>
                <li>Ask probing questions</li>
                <li>Listen carefully to their answers</li>
                <li>Watch for suspicious behavior!</li>
            </ul>
        </div>

        <div class="detective-card">
            <h4 style="color: #F7931E;">4️⃣ Solve the Mystery</h4>
            <ul style="font-family: 'Comic Neue', cursive;">
                <li>Think about all the evidence</li>
                <li>Figure out who did it</li>
                <li>Select your evidence</li>
                <li>Submit your solution!</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="detective-card">
        <h4 style="color: #FF6B35;">🎯 Tips for Success</h4>
        <ul style="font-size: 1.1rem; font-family: 'Comic Neue', cursive;">
            <li>🧩 Examine ALL clues before solving</li>
            <li>👥 Interview ALL suspects</li>
            <li>🔗 Look for connections between clues and suspects</li>
            <li>💭 Think carefully about alibis and motives</li>
            <li>✨ Trust your detective instincts!</li>
        </ul>

        <h4 style="color: #FF6B35;">🏆 Have Fun!</h4>
        <p style="font-size: 1.1rem; font-family: 'Comic Neue', cursive;">
            Remember, every great detective started somewhere. Keep practicing and you'll get better and better!
            Each mystery is unique and created just for you by AI. Happy detecting! 🎉
        </p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point"""
    # Load custom styling and metadata
    load_custom_css()
    load_favicon_and_metadata()

    # Initialize session state with database
    init_session_state()

    # Header with custom branding
    st.markdown('''
    <h1 class="main-header">
        🔍 EMERSON'S DETECTIVE GAME 🔍
    </h1>
    ''', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")

        # Language selector
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

        # Statistics from database
        st.markdown("### 📊 Your Stats")

        cases = get_all_cases()
        total_cases = len(cases)
        solved_cases = len([c for c in cases if c.get('solved', False)])
        archived_cases = len([c for c in cases if c.get('archived', False)])
        active_cases = total_cases - archived_cases

        st.metric("Total Cases", total_cases)
        st.metric("Active Cases", active_cases)
        st.metric("Solved Cases", solved_cases)
        st.metric("Archived Cases", archived_cases)

        if total_cases > 0:
            progress = solved_cases / total_cases
            st.progress(progress)
            st.caption(f"{int(progress * 100)}% Cases Solved")

        st.markdown("---")

        # About section
        st.markdown("""
        <div style="font-family: 'Comic Neue', cursive; font-size: 0.9rem;">
            <strong>🎮 Emerson's Detective Game</strong><br>
            <em>Powered by AI</em><br>
            Version 2.0
        </div>
        """, unsafe_allow_html=True)

    # Main content
    show_home_page()

    # Custom footer
    st.markdown("""
    <div class="custom-footer">
        <strong>🔍 Emerson's Detective Game</strong><br>
        Solve mysteries, sharpen your mind, have fun! 🎉
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
