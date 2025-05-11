import streamlit as st

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "form"

def go_to_blank():
    st.session_state.page = "blank"
    st.rerun()

# Page 1: Form
if st.session_state.page == "form":
    st.title("User Input Form")
    st.markdown("Please fill out the form below with your details.")

    with st.form(key="user_form"):
        age = st.number_input("Enter your age:", min_value=0, step=1)
        height = st.number_input("Enter your height (in inches):", min_value=0.0, format="%.2f")
        weight = st.number_input("Enter your weight (in lbs):", min_value=0.0, format="%.2f")
        injury = st.selectbox(
            "Type of injury:",
            [
  "Abdomen Injury",
  "Ankle Injury",
  "Arm Injury",
  "Back Injury",
  "Chest Injury",
  "Elbow Injury",
  "Face Injury",
  "Foot Injury",
  "Hand Injury",
  "Head Injury",
  "Heel Injury",
  "Hip Injury",
  "Knee Injury",
  "Leg Injury",
  "Neck Injury",
  "Shoulder Injury",
  "Other"
]
        #Injury Description: Surgery, Strain, Broken,Bruise, Sprain
        #Calculate BMI
        )

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            go_to_blank()

# Page 2: Blank
elif st.session_state.page == "blank":
    st.title("New Page")
    st.markdown("This is a blank page for now.")