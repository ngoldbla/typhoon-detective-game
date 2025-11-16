"""New Case Generation Page"""

import streamlit as st
from lib.case_generator import generate_case
from lib.types import CaseGenerationParams
from lib.database import save_case, get_image_data
from lib.image_generator import get_image_data_uri
from dataclasses import asdict


# Page configuration
st.set_page_config(
    page_title="New Mystery - Emerson's Detective Game",
    page_icon="🆕",
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
        color: #2C3E50;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        border: 3px solid #2C3E50;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        box-shadow: 3px 3px 0px #2C3E50;
    }

    img {
        border-radius: 15px;
        border: 4px solid var(--primary-color);
        box-shadow: 5px 5px 0px var(--secondary-color);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# Load custom CSS
load_custom_css()


# Header
st.markdown("""
<h1 style="font-family: 'Bangers', cursive; color: #FF6B35; text-align: center; font-size: 2.5rem;">
    🆕 Generate New Mystery
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class="detective-card">
    <p style="font-size: 1.1rem; text-align: center;">
        Create a brand new detective mystery! Choose the difficulty and theme,
        and our AI will create a fun case just for you with unique artwork!
    </p>
</div>
""", unsafe_allow_html=True)


# Initialize session state
if 'just_generated_case' not in st.session_state:
    st.session_state.just_generated_case = None


# Case generation form
with st.form("new_case_form"):
    st.markdown("### 🎨 Customize Your Mystery")

    # Custom scenario field
    custom_scenario = st.text_area(
        "📝 Custom Mystery Scenario (optional)",
        placeholder="Example: Someone stole the cookies from the cookie jar in our classroom during recess",
        help="Describe your own mystery scenario, or leave blank to use the theme options below",
        height=100
    )

    st.markdown("#### Or choose from preset options:")

    col1, col2 = st.columns(2)

    with col1:
        difficulty = st.select_slider(
            "⭐ Difficulty Level",
            options=["very_easy", "easy", "medium"],
            value="easy",
            help="Choose how challenging you want the mystery to be"
        )

        difficulty_descriptions = {
            "very_easy": "🌟 Perfect for first-time detectives!",
            "easy": "⭐ Great for most 7-year-olds",
            "medium": "✨ A bit more challenging but still fun!"
        }
        st.caption(difficulty_descriptions[difficulty])

        theme = st.selectbox(
            "🎭 Theme",
            options=["random", "school", "home", "playground", "pet", "toy"],
            index=0,
            help="Pick a theme for your mystery (ignored if custom scenario is provided)"
        )

    with col2:
        location = st.text_input(
            "📍 Location (optional)",
            placeholder="e.g., Sunny Elementary School, Maple Street Park",
            help="Where should the mystery take place?"
        )

        time_of_day = st.selectbox(
            "🕐 Time of Day",
            options=["random", "morning", "afternoon", "evening"],
            index=0
        )

    # Get language from session state
    language = st.session_state.get('language', 'en')

    st.markdown("---")
    submitted = st.form_submit_button("🎲 Generate Mystery", use_container_width=True, type="primary")


# Handle form submission
if submitted:
    with st.spinner("🔮 Creating your mystery with AI..."):
        try:
            # Show progress steps
            progress_placeholder = st.empty()
            progress_placeholder.info("📝 Step 1/3: Generating mystery story...")

            # Create generation parameters
            params = CaseGenerationParams(
                difficulty=difficulty,
                theme=theme if theme != "random" else "",
                location=location,
                era=time_of_day if time_of_day != "random" else "",
                language=language,
                custom_scenario=custom_scenario.strip() if custom_scenario else ""
            )

            # Generate the case with images
            progress_placeholder.info("🎨 Step 2/3: Creating AI artwork (this may take 1-2 minutes)...")
            generated_case = generate_case(params, generate_images=True)

            # Convert to dict for storage - structure matches what save_case expects
            case_dict = {
                'case': {
                    'id': generated_case.case.id,
                    'title': generated_case.case.title,
                    'description': generated_case.case.description,
                    'summary': generated_case.case.summary,
                    'difficulty': generated_case.case.difficulty,
                    'location': generated_case.case.location,
                    'solved': False,
                    'archived': False,
                    'dateTime': getattr(generated_case.case, 'dateTime', ''),
                    'imageUrl': generated_case.case.imageUrl,
                    'isLLMGenerated': True
                },
                'clues': [asdict(c) for c in generated_case.clues],
                'suspects': [asdict(s) for s in generated_case.suspects],
                'solution': generated_case.solution
            }

            # Save to database
            progress_placeholder.info("💾 Step 3/3: Saving to database...")
            save_case(case_dict)

            # Set as active case
            st.session_state.active_case_id = case_dict['case']['id']
            st.session_state.just_generated_case = case_dict

            progress_placeholder.empty()
            st.success("✅ Mystery created successfully!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Failed to generate case: {str(e)}")
            st.info("💡 Make sure your OPENAI_API_KEY is set correctly in your .env file")
            st.exception(e)  # Show full error for debugging
            st.session_state.just_generated_case = None


# Show the newly generated case details
if st.session_state.just_generated_case:
    case_dict = st.session_state.just_generated_case

    st.markdown("---")
    st.markdown(f"""
    <h2 style="font-family: 'Bangers', cursive; color: #FF6B35; text-align: center; font-size: 2rem;">
        📋 {case_dict['case']['title']}
    </h2>
    """, unsafe_allow_html=True)

    # Display case scene image
    image_data = get_image_data('case', case_dict['case']['id'])
    if image_data:
        data_uri = get_image_data_uri(image_data)
        st.markdown(f'<img src="{data_uri}" style="width: 100%; max-height: 400px; object-fit: cover;">',
                   unsafe_allow_html=True)
    elif case_dict['case'].get('imageUrl') and case_dict['case']['imageUrl'] not in ["/case-file.png", ""]:
        st.image(case_dict['case']['imageUrl'], use_container_width=True, caption="Case Scene")

    # Case details
    st.markdown(f"""
    <div class="detective-card">
        <p style="font-size: 1.1rem; line-height: 1.6;">{case_dict['case']['description']}</p>

        <div style="margin-top: 1rem;">
            <strong>📍 Location:</strong> {case_dict['case']['location']}<br>
            <strong>⭐ Difficulty:</strong> {case_dict['case']['difficulty'].title()}<br>
            <strong>🧩 Clues to Examine:</strong> {len(case_dict['clues'])}<br>
            <strong>👥 Suspects to Interview:</strong> {len(case_dict['suspects'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Preview suspects
    if case_dict.get('suspects'):
        st.markdown("### 👥 Suspects")
        cols = st.columns(min(3, len(case_dict['suspects'])))
        for idx, suspect in enumerate(case_dict['suspects'][:3]):
            with cols[idx]:
                st.markdown(f"""
                <div class="detective-card" style="padding: 1rem; text-align: center;">
                    <div style="font-size: 2rem;">{suspect.get('emoji', '👤')}</div>
                    <strong>{suspect['name']}</strong>
                </div>
                """, unsafe_allow_html=True)

        if len(case_dict['suspects']) > 3:
            st.caption(f"...and {len(case_dict['suspects']) - 3} more suspects!")

    # Preview clues
    if case_dict.get('clues'):
        st.markdown("### 🧩 Clues")
        cols = st.columns(min(3, len(case_dict['clues'])))
        for idx, clue in enumerate(case_dict['clues'][:3]):
            with cols[idx]:
                st.markdown(f"""
                <div class="detective-card" style="padding: 1rem; text-align: center;">
                    <div style="font-size: 2rem;">{clue.get('emoji', '🔍')}</div>
                    <strong>{clue['title']}</strong>
                </div>
                """, unsafe_allow_html=True)

        if len(case_dict['clues']) > 3:
            st.caption(f"...and {len(case_dict['clues']) - 3} more clues!")

    # Action buttons
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    col_investigate, col_home = st.columns(2)

    with col_investigate:
        if st.button("🔍 Start Investigation", use_container_width=True, type="primary"):
            st.session_state.selected_case_id = case_dict['case']['id']
            st.session_state.just_generated_case = None
            st.switch_page("pages/3_🔍_Case_Details.py")

    with col_home:
        if st.button("🏠 Return Home", use_container_width=True):
            st.session_state.just_generated_case = None
            st.switch_page("streamlit_app.py")

    st.markdown("</div>", unsafe_allow_html=True)


# Tips section
st.markdown("---")
st.markdown("""
<div class="detective-card">
    <h3 style="color: #F7931E; font-family: 'Comic Neue', cursive;">💡 Mystery Tips</h3>
    <ul style="font-family: 'Comic Neue', cursive; font-size: 1rem;">
        <li><strong>Very Easy:</strong> Simple mysteries with obvious clues - perfect for first-time detectives!</li>
        <li><strong>Easy:</strong> Fun challenges with clear connections - great for most 7-year-olds</li>
        <li><strong>Medium:</strong> More complex cases requiring careful thinking - for experienced detectives!</li>
    </ul>

    <h3 style="color: #F7931E; font-family: 'Comic Neue', cursive; margin-top: 1rem;">🎨 About AI Art</h3>
    <p style="font-family: 'Comic Neue', cursive;">
        Each mystery comes with unique AI-generated artwork including:
    </p>
    <ul style="font-family: 'Comic Neue', cursive; font-size: 1rem;">
        <li>🖼️ A dramatic scene illustration of the mystery location</li>
        <li>👥 Character portraits for each suspect</li>
        <li>🔍 Visual representations of important clues</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# Navigation
st.markdown("---")
col_back, col_view_cases = st.columns(2)

with col_back:
    if st.button("← Back to Home", use_container_width=True):
        st.session_state.just_generated_case = None
        st.switch_page("streamlit_app.py")

with col_view_cases:
    if st.button("📋 View All Cases", use_container_width=True):
        st.session_state.just_generated_case = None
        st.switch_page("pages/2_📋_All_Cases.py")
