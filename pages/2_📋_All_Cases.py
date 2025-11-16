"""All Cases Page"""

import streamlit as st


st.set_page_config(page_title="All Cases", page_icon="📋", layout="wide")

st.title("📋 All Detective Cases")

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []

if 'examined_clues' not in st.session_state:
    st.session_state.examined_clues = set()

if 'interviewed_suspects' not in st.session_state:
    st.session_state.interviewed_suspects = set()

if not st.session_state.cases:
    st.info("🔍 No cases yet! Start your detective journey by creating your first case.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆕 Create Your First Case", use_container_width=True, type="primary"):
            st.switch_page("pages/1_🆕_New_Case.py")
else:
    # Search functionality
    search = st.text_input("🔍 Search cases...", placeholder="Enter case title or description")

    st.markdown("---")

    # Display cases
    for case in st.session_state.cases:
        # Filter by search
        if search.lower() and search.lower() not in case['title'].lower() and search.lower() not in case['description'].lower():
            continue

        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                status_emoji = "✅" if case.get('solved', False) else "🔍"
                status_text = "SOLVED" if case.get('solved', False) else "ACTIVE"

                st.markdown(f"### {status_emoji} {case['title']}")
                st.markdown(f"_{case['description'][:200]}..._")

                # Progress
                total_clues = len(case.get('clues', []))
                examined = len([c for c in case.get('clues', []) if c['id'] in st.session_state.examined_clues])
                total_suspects = len(case.get('suspects', []))
                interviewed = len([s for s in case.get('suspects', []) if s['id'] in st.session_state.interviewed_suspects])

                progress_col1, progress_col2, progress_col3 = st.columns(3)
                with progress_col1:
                    st.metric("Status", status_text)
                with progress_col2:
                    st.metric("Clues", f"{examined}/{total_clues}")
                with progress_col3:
                    st.metric("Suspects", f"{interviewed}/{total_suspects}")

            with col2:
                if st.button("View Case", key=f"view_{case['id']}", use_container_width=True):
                    st.session_state.selected_case_id = case['id']
                    st.switch_page("pages/3_🔍_Case_Details.py")

            st.markdown("---")
