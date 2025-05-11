import math
import random
import time

import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "form"

def go_to_blank():
    st.session_state.page = "blank"
    st.rerun()

def create_dataframe(age, height, weight, injury, keywords):
    data = dict()

    data["age_at_injury"] = age
    data["bmi"] = weight / (height ** 2)
    words = ["Surgery", "Sprain", "Broken", "Bruise", "Strain"]
    for word in words:
        data[str.lower(word)] = word in keywords

    parts = [
        'main_body_part_abdomen', 'main_body_part_ankle',
       'main_body_part_arm', 'main_body_part_back', 'main_body_part_chest',
       'main_body_part_elbow', 'main_body_part_face', 'main_body_part_foot',
       'main_body_part_hand', 'main_body_part_head', 'main_body_part_heel',
       'main_body_part_hip', 'main_body_part_knee', 'main_body_part_leg',
       'main_body_part_neck', 'main_body_part_shoulder',
       'main_body_part_unknown'
    ]

    for part in parts:
        data[part] = False

    injury_place = str.lower(injury.split()[0])
    if injury_place == "other":
        data["main_body_part_unknown"] = True
    else:
        data["main_body_part_" + injury_place] = True

    col_order = ['surgery', 'sprain', 'broken', 'bruise', 'strain', 'bmi',
       'age_at_injury', 'main_body_part_abdomen', 'main_body_part_ankle',
       'main_body_part_arm', 'main_body_part_back', 'main_body_part_chest',
       'main_body_part_elbow', 'main_body_part_face', 'main_body_part_foot',
       'main_body_part_hand', 'main_body_part_head', 'main_body_part_heel',
       'main_body_part_hip', 'main_body_part_knee', 'main_body_part_leg',
       'main_body_part_neck', 'main_body_part_shoulder',
       'main_body_part_unknown']
    return pd.DataFrame(data, index=[1], columns=col_order)



# Page 1: Form
if st.session_state.page == "form":
    st.title("Biometric Injury Data Input")
    st.subheader("Please fill out the form below with your details.")

    with st.form(key="user_form"):
        age = st.number_input("Enter your age:", min_value=16, max_value=45, step=1)
        height = st.number_input("Enter your height (in inches):", min_value=50.0, max_value=100.0, format="%.2f")
        weight = st.number_input("Enter your weight (in lbs):", min_value=100.0, max_value=350.0, format="%.2f")
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
        )

        keywords = st.pills(
            "Select All Related to Injury",
            [
                "Surgery",
                "Strain",
                "Broken",
                "Bruise",
                "Sprain"
            ],
            selection_mode="multi"
        )

        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            df = create_dataframe(age, height, weight, injury, keywords)
            model = pickle.load(open("our_model", "rb"))
            st.session_state.prediction = math.exp(model.predict(df)[0])
            go_to_blank()

# Page 2: Blank
elif st.session_state.page == "blank":
    prediction = st.session_state.prediction

    st.title("Model Prediction")
    text_box = st.empty()
    text_box.header("Our Model is making its decisions")

    with st.spinner("Calculating Results...", show_time=True):
        time.sleep(3 + 3 * random.random())
        date_cols = [2, 19, 20, 26, 29, 30]
        injuries_df = pd.read_csv('data/injuries_cleaned.csv', parse_dates=date_cols)
        injuries_df['log10_days_injured'] = np.log10(injuries_df['DaysInjured'])

        fig = plt.figure(dpi=300)
        sns.histplot(data=injuries_df, x='log10_days_injured', bins=20, kde=True)
        t6 = np.log10(30 * 6)
        t1 = np.log10(30)
        tw = np.log10(7)
        tp = np.log10(prediction)
        plt.plot([t6, t6], [-1, -50], color='#FF0000')
        plt.text(t6, -100, '6 Month', ha='center')
        plt.plot([t1, t1], [-1, -50], color='#FF0000')
        plt.text(t1, -100, '1 Month ', ha='center')
        plt.plot([tw, tw], [-1, -50], color='#FF0000')
        plt.text(tw, -100, '1 Week', ha='center')

        plt.plot([tp, tp], [1, 1000], color='#FF00FF')
        plt.text(tp, 1050, 'Prediction', ha='center')

        plt.title('Comparison to Dataset')
        plt.xlabel('Log of Days Injured')
        plt.ylabel('Count')

    st.success("Done!")
    text_box.empty()


    st.subheader(
        """
        After analyzing over 6,500 rows of data, including NBA records dating back to 1968, our model has crunched the numbers and predicts a recovery time of approximately...
        """
    )
    st.title(str(round(prediction)) + " Days" )



    st.pyplot(fig)

