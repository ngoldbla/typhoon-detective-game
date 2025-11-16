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
    # Filter and search controls
    filter_col1, filter_col2 = st.columns([3, 1])

    with filter_col1:
        search = st.text_input("🔍 Search cases...", placeholder="Enter case title or description")

    with filter_col2:
        show_archived = st.checkbox("Show Archived", value=False)

    st.markdown("---")

    # Display cases
    for case in st.session_state.cases:
        # Filter by archived status
        is_archived = case.get('archived', False)
        if not show_archived and is_archived:
            continue

        # Filter by search
        if search.lower() and search.lower() not in case['title'].lower() and search.lower() not in case['description'].lower():
            continue

        with st.container():
            # Show thumbnail if available
            if case.get('imageUrl') and case['imageUrl'] != "/case-file.png":
                col_img, col_content, col_btn = st.columns([1, 3, 1])
                with col_img:
                    st.image(case['imageUrl'], use_container_width=True)
                col1, col2 = col_content, col_btn
            else:
                col1, col2 = st.columns([4, 1])

            with col1:
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

                # Archive/Unarchive button
                if is_archived:
                    if st.button("📤 Unarchive", key=f"unarchive_{case['id']}", use_container_width=True):
                        case['archived'] = False
                        st.rerun()
                else:
                    if st.button("📦 Archive", key=f"archive_{case['id']}", use_container_width=True):
                        case['archived'] = True
                        st.rerun()

                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{case['id']}", use_container_width=True, type="secondary"):
                    st.session_state.cases = [c for c in st.session_state.cases if c['id'] != case['id']]
                    # Clean up related data
                    st.session_state.examined_clues = {clue_id for clue_id in st.session_state.examined_clues
                                                       if not any(clue['id'] == clue_id for clue in case.get('clues', []))}
                    st.session_state.interviewed_suspects = {suspect_id for suspect_id in st.session_state.interviewed_suspects
                                                             if not any(suspect['id'] == suspect_id for suspect in case.get('suspects', []))}
                    st.rerun()

            st.markdown("---")
