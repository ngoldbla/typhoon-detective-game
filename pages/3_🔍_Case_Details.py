"""Case Details Page"""

import streamlit as st
from lib.clue_analyzer import analyze_clue
from lib.suspect_analyzer import analyze_suspect, process_interview_question
from lib.case_solver import analyze_solution
from lib.types import Clue, Suspect, Case, Interview
from dataclasses import asdict


st.set_page_config(page_title="Case Details", page_icon="🔍", layout="wide")

# Initialize session state
if 'examined_clues' not in st.session_state:
    st.session_state.examined_clues = set()
if 'interviewed_suspects' not in st.session_state:
    st.session_state.interviewed_suspects = set()
if 'clue_analyses' not in st.session_state:
    st.session_state.clue_analyses = {}
if 'suspect_interviews' not in st.session_state:
    st.session_state.suspect_interviews = {}

# Get selected case
case_id = st.session_state.get('selected_case_id')

if not case_id:
    st.error("❌ No case selected")
    if st.button("← Back to Cases"):
        st.switch_page("pages/2_📋_All_Cases.py")
    st.stop()

# Find the case
case = next((c for c in st.session_state.get('cases', []) if c['id'] == case_id), None)

if not case:
    st.error("❌ Case not found")
    if st.button("← Back to Cases"):
        st.switch_page("pages/2_📋_All_Cases.py")
    st.stop()

# Display case header
st.title(f"🔍 {case['title']}")

# Case description
with st.expander("📖 Case Description", expanded=True):
    st.markdown(case['description'])
    st.markdown(f"**Location:** {case['location']}")
    st.markdown(f"**Difficulty:** {case['difficulty'].title()}")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🧩 Clues", "👥 Suspects", "✅ Solve Case"])

with tab1:
    st.markdown("### 🧩 Clues")

    if not case.get('clues'):
        st.info("No clues available for this case.")
    else:
        for clue_dict in case['clues']:
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    clue_emoji = clue_dict.get('emoji', '🔍')
                    st.markdown(f"{clue_emoji} **{clue_dict['title']}**")
                    st.markdown(f"_{clue_dict['description']}_")
                    st.caption(f"📍 Found at: {clue_dict['location']}")

                with col2:
                    if clue_dict['id'] in st.session_state.examined_clues:
                        st.success("✓ Examined")
                        if st.button("View Analysis", key=f"view_analysis_{clue_dict['id']}"):
                            analysis = st.session_state.clue_analyses.get(clue_dict['id'])
                            if analysis:
                                st.markdown("**Analysis:**")
                                st.info(analysis.get('summary', 'No summary available'))
                    else:
                        if st.button("🔍 Examine", key=f"examine_{clue_dict['id']}"):
                            with st.spinner("🔬 Analyzing clue..."):
                                try:
                                    # Convert dict to Clue object
                                    clue_obj = Clue(**clue_dict)
                                    case_obj = Case(
                                        id=case['id'],
                                        title=case['title'],
                                        description=case['description'],
                                        summary=case.get('summary', ''),
                                        location=case.get('location', ''),
                                        difficulty=case.get('difficulty', 'medium')
                                    )
                                    suspects = [Suspect(**s) for s in case['suspects']]
                                    discovered_clues = [Clue(**c) for c in case['clues']]

                                    # Analyze clue
                                    analysis = analyze_clue(
                                        clue_obj,
                                        suspects,
                                        case_obj,
                                        discovered_clues,
                                        st.session_state.get('language', 'en')
                                    )

                                    # Store analysis
                                    st.session_state.clue_analyses[clue_dict['id']] = {
                                        'summary': analysis.summary,
                                        'connections': [asdict(c) for c in analysis.connections],
                                        'nextSteps': analysis.nextSteps
                                    }
                                    st.session_state.examined_clues.add(clue_dict['id'])

                                    st.success("✅ Clue analyzed!")
                                    st.rerun()

                                except Exception as e:
                                    st.error(f"Failed to analyze clue: {str(e)}")

                # Show analysis if examined
                if clue_dict['id'] in st.session_state.examined_clues:
                    analysis = st.session_state.clue_analyses.get(clue_dict['id'])
                    if analysis:
                        with st.expander("🔬 Analysis Details"):
                            st.markdown(f"**Summary:** {analysis['summary']}")

                            if analysis.get('connections'):
                                st.markdown("**Connections:**")
                                for conn in analysis['connections']:
                                    suspect_name = next(
                                        (s['name'] for s in case['suspects'] if s['id'] == conn['suspectId']),
                                        'Unknown'
                                    )
                                    st.markdown(f"- **{suspect_name}**: {conn['description']}")

                            if analysis.get('nextSteps'):
                                st.markdown("**Next Steps:**")
                                for step in analysis['nextSteps']:
                                    st.markdown(f"- {step}")

                st.markdown("---")

with tab2:
    st.markdown("### 👥 Suspects")

    if not case.get('suspects'):
        st.info("No suspects identified for this case.")
    else:
        for suspect_dict in case['suspects']:
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    suspect_emoji = suspect_dict.get('emoji', '👤')
                    st.markdown(f"{suspect_emoji} **{suspect_dict['name']}**")
                    st.markdown(f"_{suspect_dict['description']}_")
                    st.caption(f"**Alibi:** {suspect_dict['alibi']}")

                with col2:
                    if suspect_dict['id'] in st.session_state.interviewed_suspects:
                        st.success("✓ Interviewed")
                    else:
                        if st.button("💬 Interview", key=f"interview_{suspect_dict['id']}"):
                            st.session_state.selected_suspect_id = suspect_dict['id']
                            st.session_state.current_interview = suspect_dict['id']

                # Interview interface
                if st.session_state.get('current_interview') == suspect_dict['id']:
                    with st.expander("💬 Interview in Progress", expanded=True):
                        st.markdown(f"**Interviewing: {suspect_dict['name']}**")

                        # Get or create interview
                        if suspect_dict['id'] not in st.session_state.suspect_interviews:
                            st.session_state.suspect_interviews[suspect_dict['id']] = {
                                'questions': []
                            }

                        interview = st.session_state.suspect_interviews[suspect_dict['id']]

                        # Show previous Q&A
                        if interview['questions']:
                            st.markdown("**Previous Questions:**")
                            for qa in interview['questions']:
                                st.markdown(f"**Q:** {qa['question']}")
                                st.markdown(f"**A:** {qa['answer']}")
                                st.markdown("---")

                        # Ask new question
                        question = st.text_input("Ask a question:", key=f"question_input_{suspect_dict['id']}")

                        if st.button("Ask", key=f"ask_{suspect_dict['id']}"):
                            if question:
                                with st.spinner("💭 Thinking..."):
                                    try:
                                        suspect_obj = Suspect(**suspect_dict)
                                        case_obj = Case(
                                            id=case['id'],
                                            title=case['title'],
                                            description=case['description'],
                                            summary=case.get('summary', '')
                                        )
                                        clues = [Clue(**c) for c in case['clues']]

                                        # Process question
                                        answer = process_interview_question(
                                            question,
                                            suspect_obj,
                                            clues,
                                            case_obj,
                                            interview['questions'],
                                            st.session_state.get('language', 'en')
                                        )

                                        # Store Q&A
                                        interview['questions'].append({
                                            'question': question,
                                            'answer': answer
                                        })

                                        st.session_state.interviewed_suspects.add(suspect_dict['id'])
                                        st.rerun()

                                    except Exception as e:
                                        st.error(f"Failed to process question: {str(e)}")

                        if st.button("End Interview", key=f"end_{suspect_dict['id']}"):
                            st.session_state.current_interview = None
                            st.rerun()

                st.markdown("---")

with tab3:
    st.markdown("### ✅ Solve the Case")

    st.markdown("""
    Think you've figured it out? Select who you think did it, choose your evidence,
    and explain your reasoning!
    """)

    with st.form("solve_case_form"):
        # Select suspect
        suspect_options = {s['id']: s['name'] for s in case['suspects']}
        accused_id = st.selectbox(
            "Who do you think did it?",
            options=list(suspect_options.keys()),
            format_func=lambda x: suspect_options[x]
        )

        # Select evidence
        clue_options = {c['id']: c['title'] for c in case['clues']}
        evidence_ids = st.multiselect(
            "What evidence supports your theory?",
            options=list(clue_options.keys()),
            format_func=lambda x: clue_options[x]
        )

        # Reasoning
        reasoning = st.text_area(
            "Explain your reasoning:",
            placeholder="Why do you think this person did it? How does the evidence support your theory?"
        )

        submitted = st.form_submit_button("🎯 Submit Solution", use_container_width=True)

    # Handle form submission outside the form context
    if submitted:
        if not evidence_ids:
            st.error("Please select at least one piece of evidence!")
        elif not reasoning:
            st.error("Please explain your reasoning!")
        else:
            with st.spinner("🔍 Evaluating your solution..."):
                try:
                    case_obj = Case(
                        id=case['id'],
                        title=case['title'],
                        description=case['description'],
                        summary=case.get('summary', '')
                    )
                    suspects = [Suspect(**s) for s in case['suspects']]
                    clues = [Clue(**c) for c in case['clues']]

                    # Analyze solution
                    solution = analyze_solution(
                        case_obj,
                        suspects,
                        clues,
                        accused_id,
                        evidence_ids,
                        reasoning,
                        st.session_state.get('language', 'en')
                    )

                    # Show result
                    if solution.solved:
                        st.success("🎉 Congratulations! You solved the case!")
                        st.balloons()
                        case['solved'] = True
                    else:
                        st.warning("🤔 Not quite right. Keep investigating!")

                    st.markdown("### 📝 Verdict")
                    st.markdown(solution.narrative)

                    if solution.solved:
                        if st.button("🏠 Return Home"):
                            st.switch_page("streamlit_app.py")

                except Exception as e:
                    st.error(f"Failed to evaluate solution: {str(e)}")

# Back button
st.markdown("---")
if st.button("← Back to All Cases"):
    st.switch_page("pages/2_📋_All_Cases.py")
