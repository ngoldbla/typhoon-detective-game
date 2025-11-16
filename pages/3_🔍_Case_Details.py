"""Case Details Page - Investigation Interface"""

import streamlit as st
from lib.clue_analyzer import analyze_clue
from lib.suspect_analyzer import analyze_suspect, process_interview_question
from lib.case_solver import analyze_solution
from lib.types import Clue, Suspect, Case
from lib.database import (
    get_case_by_id,
    get_examined_clues,
    get_interviewed_suspects,
    mark_clue_examined,
    mark_suspect_interviewed,
    save_clue_analysis,
    get_clue_analysis,
    save_interview,
    get_suspect_interviews,
    update_case_status,
    get_image_data
)
from lib.image_generator import get_image_data_uri
from lib.sample_questions import get_sample_questions_for_suspect
from dataclasses import asdict


# Page configuration
st.set_page_config(
    page_title="Case Investigation - Emerson's Detective Game",
    page_icon="🔍",
    layout="wide"
)


def load_custom_css():
    """Load the custom CSS (same as main app)"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

    :root {
        --primary-color: #FF6B35;
        --secondary-color: #F7931E;
        --accent-color: #FDC830;
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

    .sample-question-btn {
        background-color: #FFF9F0;
        border: 2px solid var(--secondary-color);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-family: 'Comic Neue', cursive;
        color: #2C3E50;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-block;
    }

    .sample-question-btn:hover {
        background-color: var(--accent-color);
        transform: translateY(-2px);
    }

    img {
        border-radius: 15px;
        border: 4px solid var(--primary-color);
        box-shadow: 5px 5px 0px var(--secondary-color);
    }

    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        font-family: 'Comic Neue', cursive;
    }

    .chat-question {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }

    .chat-answer {
        background-color: #F1F8E9;
        border-left: 4px solid #8BC34A;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# Load custom CSS
load_custom_css()


# Get selected case from database
case_id = st.session_state.get('selected_case_id')

if not case_id:
    st.error("❌ No case selected")
    if st.button("← Back to Cases"):
        st.switch_page("pages/2_📋_All_Cases.py")
    st.stop()

# Load case from database
case = get_case_by_id(case_id)

if not case:
    st.error("❌ Case not found in database")
    if st.button("← Back to Cases"):
        st.switch_page("pages/2_📋_All_Cases.py")
    st.stop()

# Load progress from database
examined_clues = get_examined_clues(case_id)
interviewed_suspects = get_interviewed_suspects(case_id)


# Display case header
st.markdown(f"""
<h1 style="font-family: 'Bangers', cursive; color: #FF6B35; text-align: center; font-size: 2.5rem;">
    🔍 {case['title']}
</h1>
""", unsafe_allow_html=True)


# Case description with image
with st.expander("📖 Case Description", expanded=True):
    # Try to load case image from database
    image_data = get_image_data('case', case_id)
    if image_data:
        data_uri = get_image_data_uri(image_data)
        st.markdown(f'<img src="{data_uri}" style="width: 100%; max-height: 400px; object-fit: cover;">',
                   unsafe_allow_html=True)
    elif case.get('imageUrl') and case['imageUrl'] not in ["/case-file.png", ""]:
        st.image(case['imageUrl'], use_container_width=True)

    st.markdown(f"""
    <div class="detective-card">
        <p style="font-size: 1.1rem;">{case['description']}</p>
        <p><strong>📍 Location:</strong> {case['location']}</p>
        <p><strong>⭐ Difficulty:</strong> {case['difficulty'].title()}</p>
    </div>
    """, unsafe_allow_html=True)


# Progress indicators
col_prog1, col_prog2 = st.columns(2)
with col_prog1:
    clue_count = len(examined_clues)
    total_clues = len(case.get('clues', []))
    st.metric("🧩 Clues Examined", f"{clue_count}/{total_clues}")

with col_prog2:
    suspect_count = len(interviewed_suspects)
    total_suspects = len(case.get('suspects', []))
    st.metric("👥 Suspects Interviewed", f"{suspect_count}/{total_suspects}")


# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["🧩 Clues", "👥 Suspects", "✅ Solve Case"])


with tab1:
    st.markdown("### 🧩 Examine Clues")

    if not case.get('clues'):
        st.info("No clues available for this case.")
    else:
        for clue_dict in case['clues']:
            with st.container():
                st.markdown('<div class="detective-card">', unsafe_allow_html=True)

                # Layout with image if available
                image_data = get_image_data('clue', clue_dict['id'])
                if image_data or clue_dict.get('imageUrl'):
                    col_img, col_content = st.columns([1, 2])
                    with col_img:
                        if image_data:
                            data_uri = get_image_data_uri(image_data)
                            st.markdown(f'<img src="{data_uri}" style="width: 100%;">',
                                       unsafe_allow_html=True)
                        elif clue_dict.get('imageUrl'):
                            st.image(clue_dict['imageUrl'], use_container_width=True)

                    with col_content:
                        clue_emoji = clue_dict.get('emoji', '🔍')
                        st.markdown(f"### {clue_emoji} {clue_dict['title']}")
                        st.markdown(f"_{clue_dict['description']}_")
                        st.caption(f"📍 Found at: {clue_dict['location']}")
                else:
                    clue_emoji = clue_dict.get('emoji', '🔍')
                    st.markdown(f"### {clue_emoji} {clue_dict['title']}")
                    st.markdown(f"_{clue_dict['description']}_")
                    st.caption(f"📍 Found at: {clue_dict['location']}")

                # Examine button
                if clue_dict['id'] in examined_clues:
                    st.success("✓ Already Examined")

                    # Show cached analysis
                    analysis = get_clue_analysis(clue_dict['id'])
                    if analysis:
                        with st.expander("🔬 View Analysis"):
                            st.markdown(f"**Summary:** {analysis['summary']}")

                            if analysis.get('connections'):
                                st.markdown("**Connections to Suspects:**")
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
                else:
                    if st.button("🔍 Examine This Clue", key=f"examine_{clue_dict['id']}"):
                        with st.spinner("🔬 Analyzing clue..."):
                            try:
                                # Convert to objects
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

                                # Analyze clue with AI
                                analysis = analyze_clue(
                                    clue_obj,
                                    suspects,
                                    case_obj,
                                    discovered_clues,
                                    st.session_state.get('language', 'en')
                                )

                                # Save to database
                                analysis_dict = {
                                    'summary': analysis.summary,
                                    'connections': [asdict(c) for c in analysis.connections],
                                    'nextSteps': analysis.nextSteps
                                }
                                save_clue_analysis(clue_dict['id'], analysis_dict)
                                mark_clue_examined(case_id, clue_dict['id'])

                                st.success("✅ Clue analyzed!")
                                st.rerun()

                            except Exception as e:
                                st.error(f"Failed to analyze clue: {str(e)}")

                st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.markdown("### 👥 Interview Suspects")

    if not case.get('suspects'):
        st.info("No suspects identified for this case.")
    else:
        for suspect_dict in case['suspects']:
            with st.container():
                st.markdown('<div class="detective-card">', unsafe_allow_html=True)

                # Layout with portrait if available
                image_data = get_image_data('suspect', suspect_dict['id'])
                if image_data or suspect_dict.get('imageUrl'):
                    col_img, col_content = st.columns([1, 2])
                    with col_img:
                        if image_data:
                            data_uri = get_image_data_uri(image_data)
                            st.markdown(f'<img src="{data_uri}" style="width: 100%;">',
                                       unsafe_allow_html=True)
                        elif suspect_dict.get('imageUrl'):
                            st.image(suspect_dict['imageUrl'], use_container_width=True)

                    with col_content:
                        suspect_emoji = suspect_dict.get('emoji', '👤')
                        st.markdown(f"### {suspect_emoji} {suspect_dict['name']}")
                        st.markdown(f"_{suspect_dict['description']}_")
                        st.caption(f"**Alibi:** {suspect_dict['alibi']}")
                else:
                    suspect_emoji = suspect_dict.get('emoji', '👤')
                    st.markdown(f"### {suspect_emoji} {suspect_dict['name']}")
                    st.markdown(f"_{suspect_dict['description']}_")
                    st.caption(f"**Alibi:** {suspect_dict['alibi']}")

                # Interview status
                if suspect_dict['id'] in interviewed_suspects:
                    st.success("✓ Already Interviewed")
                else:
                    st.info("💬 Not yet interviewed")

                # Interview button
                if st.button(f"💬 Interview {suspect_dict['name']}",
                           key=f"start_interview_{suspect_dict['id']}"):
                    st.session_state.current_interview = suspect_dict['id']
                    st.rerun()

                # Interview interface
                if st.session_state.get('current_interview') == suspect_dict['id']:
                    st.markdown("---")
                    st.markdown(f"### 💬 Interviewing: {suspect_dict['name']}")

                    # Get interview history from database
                    interview_history = get_suspect_interviews(suspect_dict['id'])

                    # Show previous Q&A
                    if interview_history:
                        st.markdown("**Previous Questions:**")
                        for qa in interview_history:
                            st.markdown(f"""
                            <div class="chat-message chat-question">
                                <strong>🕵️ You:</strong> {qa['question']}
                            </div>
                            <div class="chat-message chat-answer">
                                <strong>{suspect_emoji} {suspect_dict['name']}:</strong> {qa['answer']}
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown("---")

                    # Sample questions
                    st.markdown("**💡 Sample Questions (click to use):**")

                    sample_questions = get_sample_questions_for_suspect(
                        suspect_dict['name'],
                        suspect_dict['description'],
                        suspect_dict['alibi'],
                        case['description'],
                        st.session_state.get('language', 'en')
                    )

                    # Display sample questions as clickable buttons in a grid
                    cols = st.columns(2)
                    for idx, sample_q in enumerate(sample_questions[:6]):  # Show top 6
                        with cols[idx % 2]:
                            if st.button(f"💭 {sample_q}", key=f"sample_{suspect_dict['id']}_{idx}",
                                       use_container_width=True):
                                st.session_state[f'question_{suspect_dict["id"]}'] = sample_q
                                st.rerun()

                    # Ask custom question
                    st.markdown("**✏️ Or ask your own question:**")
                    question = st.text_input(
                        "Type your question:",
                        key=f"question_input_{suspect_dict['id']}",
                        value=st.session_state.get(f'question_{suspect_dict["id"]}', ''),
                        placeholder="What do you want to ask?"
                    )

                    col_ask, col_end = st.columns([2, 1])

                    with col_ask:
                        if st.button("📤 Ask Question", key=f"ask_{suspect_dict['id']}",
                                   use_container_width=True):
                            if question:
                                with st.spinner(f"💭 {suspect_dict['name']} is thinking..."):
                                    try:
                                        suspect_obj = Suspect(**suspect_dict)
                                        case_obj = Case(
                                            id=case['id'],
                                            title=case['title'],
                                            description=case['description'],
                                            summary=case.get('summary', ''),
                                            location=case.get('location', ''),
                                            difficulty=case.get('difficulty', 'medium')
                                        )
                                        clues = [Clue(**c) for c in case['clues']]

                                        # Get previous questions for context
                                        previous_qa = [
                                            {'question': qa['question'], 'answer': qa['answer']}
                                            for qa in interview_history
                                        ]

                                        # Process question with AI
                                        answer = process_interview_question(
                                            question,
                                            suspect_obj,
                                            clues,
                                            case_obj,
                                            previous_qa,
                                            st.session_state.get('language', 'en')
                                        )

                                        # Save to database
                                        save_interview(suspect_dict['id'], question, answer)
                                        mark_suspect_interviewed(case_id, suspect_dict['id'])

                                        # Clear question input
                                        if f'question_{suspect_dict["id"]}' in st.session_state:
                                            del st.session_state[f'question_{suspect_dict["id"]}']

                                        st.success("✅ Question asked!")
                                        st.rerun()

                                    except Exception as e:
                                        st.error(f"Failed to process question: {str(e)}")
                            else:
                                st.warning("Please enter a question first!")

                    with col_end:
                        if st.button("✅ End Interview", key=f"end_{suspect_dict['id']}",
                                   use_container_width=True):
                            st.session_state.current_interview = None
                            st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)


with tab3:
    st.markdown("### ✅ Solve the Mystery")

    # Check if case is already solved
    if case.get('solved'):
        st.success("🎉 This case has already been solved!")
        if st.button("🏠 Return Home"):
            st.switch_page("streamlit_app.py")
        st.stop()

    st.markdown("""
    <div class="detective-card">
        <p style="font-size: 1.1rem;">
            Think you've figured it out? Select who you think committed the crime,
            choose your supporting evidence, and explain your reasoning!
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("solve_case_form"):
        # Select suspect
        st.markdown("#### 🎯 Who did it?")
        suspect_options = {s['id']: f"{s.get('emoji', '👤')} {s['name']}"
                          for s in case['suspects']}
        accused_id = st.selectbox(
            "Select the culprit:",
            options=list(suspect_options.keys()),
            format_func=lambda x: suspect_options[x]
        )

        # Select evidence
        st.markdown("#### 📋 What evidence supports your theory?")
        clue_options = {c['id']: f"{c.get('emoji', '🔍')} {c['title']}"
                       for c in case['clues']}
        evidence_ids = st.multiselect(
            "Select the clues that prove your case:",
            options=list(clue_options.keys()),
            format_func=lambda x: clue_options[x]
        )

        # Reasoning
        st.markdown("#### 💭 Explain your reasoning:")
        reasoning = st.text_area(
            "Detective's Report:",
            placeholder="Explain your theory:\n• Why do you think this person did it?\n• How does the evidence support your theory?\n• What's their motive?",
            height=150
        )

        submitted = st.form_submit_button("🎯 Submit Solution", use_container_width=True)

    # Handle form submission
    if submitted:
        if not evidence_ids:
            st.error("❌ Please select at least one piece of evidence to support your theory!")
        elif not reasoning or len(reasoning) < 20:
            st.error("❌ Please provide a detailed explanation of your reasoning!")
        else:
            with st.spinner("🔍 Detective reviewing your solution..."):
                try:
                    case_obj = Case(
                        id=case['id'],
                        title=case['title'],
                        description=case['description'],
                        summary=case.get('summary', ''),
                        location=case.get('location', ''),
                        difficulty=case.get('difficulty', 'medium')
                    )
                    suspects = [Suspect(**s) for s in case['suspects']]
                    clues = [Clue(**c) for c in case['clues']]

                    # Analyze solution with AI
                    solution = analyze_solution(
                        case_obj,
                        suspects,
                        clues,
                        accused_id,
                        evidence_ids,
                        reasoning,
                        st.session_state.get('language', 'en')
                    )

                    # Show result with styling
                    if solution.solved:
                        st.balloons()
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
                                    padding: 2rem; border-radius: 15px; border: 4px solid #2E7D32;
                                    box-shadow: 5px 5px 0px #1B5E20; text-align: center;">
                            <h2 style="color: white; font-family: 'Bangers', cursive; font-size: 2.5rem; margin: 0;">
                                🎉 CASE SOLVED! 🎉
                            </h2>
                            <p style="color: white; font-size: 1.2rem; margin-top: 1rem;">
                                Congratulations, Detective! You cracked the case!
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Update database
                        update_case_status(case_id, solved=True)
                    else:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%);
                                    padding: 2rem; border-radius: 15px; border: 4px solid #F57C00;
                                    box-shadow: 5px 5px 0px #E65100; text-align: center;">
                            <h2 style="color: white; font-family: 'Bangers', cursive; font-size: 2.5rem; margin: 0;">
                                🤔 NOT QUITE RIGHT
                            </h2>
                            <p style="color: white; font-size: 1.2rem; margin-top: 1rem;">
                                Keep investigating! The truth is out there...
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Show AI feedback
                    st.markdown("### 📝 Detective's Verdict")
                    st.markdown(f"""
                    <div class="detective-card">
                        <p style="font-size: 1.1rem; line-height: 1.6;">{solution.narrative}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if solution.solved:
                        col_home, col_cases = st.columns(2)
                        with col_home:
                            if st.button("🏠 Return Home", use_container_width=True):
                                st.switch_page("streamlit_app.py")
                        with col_cases:
                            if st.button("📋 View All Cases", use_container_width=True):
                                st.switch_page("pages/2_📋_All_Cases.py")

                except Exception as e:
                    st.error(f"❌ Failed to evaluate solution: {str(e)}")


# Navigation
st.markdown("---")
col_back, col_home = st.columns(2)
with col_back:
    if st.button("← Back to All Cases", use_container_width=True):
        st.switch_page("pages/2_📋_All_Cases.py")
with col_home:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("streamlit_app.py")
