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
if 'just_generated_case' not in st.session_state:
    st.session_state.just_generated_case = None

with st.form("new_case_form"):
    st.markdown("### 🎨 Customize Your Mystery")

    # Custom scenario field
    custom_scenario = st.text_area(
        "Custom Mystery Scenario (optional)",
        placeholder="e.g., Someone stole the gummy worms from my lunchbox at school",
        help="Describe your own mystery scenario, or leave blank to use the theme options below",
        height=80
    )

    st.markdown("#### Or choose from preset options:")

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
            help="Pick a theme for your mystery (ignored if custom scenario is provided)"
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
                language=language,
                custom_scenario=custom_scenario.strip() if custom_scenario else ""
            )

            # Generate the case (with images by default)
            st.info("🎨 Generating case and AI artwork... This may take a minute.")
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
                'imageUrl': generated_case.case.imageUrl,  # Add case scene image
                'clues': [asdict(c) for c in generated_case.clues],
                'suspects': [asdict(s) for s in generated_case.suspects],
                'solution': generated_case.solution
            }

            # Add to cases
            st.session_state.cases.append(case_dict)
            st.session_state.active_case_id = case_dict['id']
            st.session_state.just_generated_case = case_dict

            st.success("✅ Mystery created successfully!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Failed to generate case: {str(e)}")
            st.info("💡 Make sure your OPENAI_API_KEY is set correctly in your .env file")
            st.session_state.just_generated_case = None

# Show the newly generated case details outside the form
if st.session_state.just_generated_case:
    case_dict = st.session_state.just_generated_case

    st.markdown("---")
    st.markdown(f"## {case_dict['title']}")

    # Display case scene image if available
    if case_dict.get('imageUrl') and case_dict['imageUrl'] != "/case-file.png":
        st.image(case_dict['imageUrl'], use_container_width=True, caption="Case Scene")

    st.markdown(f"_{case_dict['description']}_")

    st.markdown(f"**Location:** {case_dict['location']}")
    st.markdown(f"**Difficulty:** {case_dict['difficulty'].title()}")
    st.markdown(f"**Clues:** {len(case_dict['clues'])}")
    st.markdown(f"**Suspects:** {len(case_dict['suspects'])}")

    if st.button("🔍 Start Investigation", use_container_width=True):
        st.session_state.current_page = 'case_details'
        st.session_state.selected_case_id = case_dict['id']
        st.session_state.just_generated_case = None  # Clear the flag
        st.switch_page("pages/3_🔍_Case_Details.py")

st.markdown("---")
st.markdown("### 💡 Tips")
st.markdown("""
- **Very Easy**: Perfect for first-time detectives!
- **Easy**: Great for most 7-year-olds
- **Medium**: A bit more challenging but still fun!
""")
