"""All Cases Page - Browse and manage your detective cases"""

import streamlit as st
from lib.database import get_all_cases, delete_case, update_case_status


# Page configuration
st.set_page_config(
    page_title="All Cases - Emerson's Detective Game",
    page_icon="📋",
    layout="wide"
)


def load_custom_css():
    """Load custom CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

    :root {
        --primary-color: #FF6B35;
        --secondary-color: #F7931E;
        --bg-light: #FFF9F0;
    }

    .main {
        background-color: var(--bg-light);
    }

    .detective-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF9F0 100%);
        border: 4px solid var(--primary-color);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 5px 5px 0px var(--secondary-color);
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        border: 3px solid #2C3E50;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        box-shadow: 3px 3px 0px #2C3E50;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# Load CSS
load_custom_css()


# Header
st.markdown("""
<h1 style="font-family: 'Bangers', cursive; color: #FF6B35; text-align: center; font-size: 2.5rem;">
    📋 All Detective Cases
</h1>
""", unsafe_allow_html=True)


# Load cases from database
cases = get_all_cases()

if not cases:
    st.markdown("""
    <div class="detective-card" style="text-align: center; padding: 3rem;">
        <h2 style="color: #F7931E; font-family: 'Comic Neue', cursive;">🔍 No cases yet!</h2>
        <p style="font-size: 1.2rem; font-family: 'Comic Neue', cursive;">
            Start your detective journey by creating your first mystery case.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆕 Create Your First Case", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🆕_New_Case.py")
else:
    # Filter and search controls
    filter_col1, filter_col2 = st.columns([3, 1])

    with filter_col1:
        search = st.text_input("🔍 Search cases...", placeholder="Enter case title or description")

    with filter_col2:
        show_archived = st.checkbox("Show Archived", value=False)

    st.markdown("---")

    # Display cases
    filtered_count = 0
    for case in cases:
        # Filter by archived status
        is_archived = case.get('archived', False)
        if not show_archived and is_archived:
            continue

        # Filter by search
        if search.lower() and search.lower() not in case['title'].lower() and search.lower() not in case['description'].lower():
            continue

        filtered_count += 1

        st.markdown('<div class="detective-card">', unsafe_allow_html=True)

        # Status display
        if is_archived:
            status_emoji = "📦"
            status_text = "ARCHIVED"
        elif case.get('solved', False):
            status_emoji = "✅"
            status_text = "SOLVED"
        else:
            status_emoji = "🔍"
            status_text = "ACTIVE"

        st.markdown(f"### {status_emoji} {case['title']}")
        st.caption(f"**Status:** {status_text} | **Difficulty:** {case.get('difficulty', 'medium').title()}")
        st.markdown(f"_{case['description'][:200]}..._")

        # Action buttons
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

        with col_btn1:
            if st.button("🔍 Investigate", key=f"view_{case['id']}", use_container_width=True):
                st.session_state.selected_case_id = case['id']
                st.switch_page("pages/3_🔍_Case_Details.py")

        with col_btn2:
            if not is_archived:
                if st.button("📦 Archive", key=f"archive_{case['id']}", use_container_width=True):
                    update_case_status(case['id'], archived=True)
                    st.rerun()
            else:
                if st.button("📂 Unarchive", key=f"unarchive_{case['id']}", use_container_width=True):
                    update_case_status(case['id'], archived=False)
                    st.rerun()

        with col_btn3:
            if case.get('solved'):
                st.success("✅ Solved", icon="✅")
            else:
                st.info("🔍 Unsolved")

        with col_btn4:
            if st.button("🗑️ Delete", key=f"delete_{case['id']}", use_container_width=True):
                if st.session_state.get(f'confirm_delete_{case["id"]}'):
                    delete_case(case['id'])
                    st.session_state[f'confirm_delete_{case["id"]}'] = False
                    st.rerun()
                else:
                    st.session_state[f'confirm_delete_{case["id"]}'] = True
                    st.warning("Click again to confirm deletion")

        st.markdown('</div>', unsafe_allow_html=True)

    if filtered_count == 0:
        st.info("No cases match your search criteria.")

# Navigation
st.markdown("---")
col_back, col_new = st.columns(2)

with col_back:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("streamlit_app.py")

with col_new:
    if st.button("🆕 New Case", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🆕_New_Case.py")
