"""New Case Generation Page"""

import streamlit as st
from lib.case_generator import generate_case
from lib.types import CaseGenerationParams
from dataclasses import asdict


st.set_page_config(page_title="New Case", page_icon="🆕", layout="wide")

st.title("🆕 Generate New Mystery")

st.markdown("""
Create a brand new detective mystery! Choose the difficulty and theme,
and our AI will create a fun case just for you!
""")

# Initialize session state if needed
if 'cases' not in st.session_state:
    st.session_state.cases = []

with st.form("new_case_form"):
    st.markdown("### 🎨 Customize Your Mystery")

    col1, col2 = st.columns(2)

    with col1:
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["very_easy", "easy", "medium"],
            value="easy",
            help="Choose how challenging you want the mystery to be"
        )

        theme = st.selectbox(
            "Theme",
            options=["random", "school", "home", "playground", "pet", "toy"],
            index=0,
            help="Pick a theme for your mystery"
        )

    with col2:
        location = st.text_input(
            "Location (optional)",
            placeholder="e.g., Sunny Elementary School",
            help="Where should the mystery take place?"
        )

        time_of_day = st.selectbox(
            "Time of Day",
            options=["random", "morning", "afternoon", "evening"],
            index=0
        )

    language = st.session_state.get('language', 'en')

    submitted = st.form_submit_button("🎲 Generate Mystery", use_container_width=True)

    if submitted:
        with st.spinner("🔮 Creating your mystery..."):
            try:
                # Create generation parameters
                params = CaseGenerationParams(
                    difficulty=difficulty,
                    theme=theme if theme != "random" else "",
                    location=location,
                    era=time_of_day if time_of_day != "random" else "",
                    language=language
                )

                # Generate the case
                generated_case = generate_case(params)

                # Convert to dict for storage
                case_dict = {
                    'id': generated_case.case.id,
                    'title': generated_case.case.title,
                    'description': generated_case.case.description,
                    'summary': generated_case.case.summary,
                    'difficulty': generated_case.case.difficulty,
                    'solved': False,
                    'location': generated_case.case.location,
                    'dateTime': generated_case.case.dateTime,
                    'clues': [asdict(c) for c in generated_case.clues],
                    'suspects': [asdict(s) for s in generated_case.suspects],
                    'solution': generated_case.solution
                }

                # Add to cases
                st.session_state.cases.append(case_dict)
                st.session_state.active_case_id = case_dict['id']

                st.success("✅ Mystery created successfully!")
                st.balloons()

                # Show case details
                st.markdown("---")
                st.markdown(f"## {case_dict['title']}")
                st.markdown(f"_{case_dict['description']}_")

                st.markdown(f"**Location:** {case_dict['location']}")
                st.markdown(f"**Difficulty:** {case_dict['difficulty'].title()}")
                st.markdown(f"**Clues:** {len(case_dict['clues'])}")
                st.markdown(f"**Suspects:** {len(case_dict['suspects'])}")

                if st.button("🔍 Start Investigation", use_container_width=True):
                    st.session_state.current_page = 'case_details'
                    st.session_state.selected_case_id = case_dict['id']
                    st.switch_page("pages/2_📋_All_Cases.py")

            except Exception as e:
                st.error(f"❌ Failed to generate case: {str(e)}")
                st.info("💡 Make sure your OPENAI_API_KEY is set correctly in your .env file")

st.markdown("---")
st.markdown("### 💡 Tips")
st.markdown("""
- **Very Easy**: Perfect for first-time detectives!
- **Easy**: Great for most 7-year-olds
- **Medium**: A bit more challenging but still fun!
""")
