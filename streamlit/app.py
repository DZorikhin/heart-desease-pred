import pickle
import requests

import streamlit as st


st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="🔬",
    initial_sidebar_state="expanded",
    )


def sidebar():
    st.sidebar.image("heart-disease.jpeg", width=300)
    st.sidebar.title("About")
    st.sidebar.write("This research intends to pinpoint the most relevant risk factors of heart disease as well as predict the overall risk.")
    sidebar_html = """
    [Here](https://github.com/DZorikhin/heart-desease-pred) is GitHub repository with:
    - Detailed project description
    - Data preparation and data cleaning
    - EDA, feature importance analysis
    - Model selection process 
    - Parameters tuning
    - Exporting notebook to script
    - Model deployment (Flask)
    - Dependency and Environment Management
    - Containerization with Docker
    - Deployment to the Cloud
    """
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)


def frontpage():
    st.title("Heart Disease Prediction")
    html_temp = """
    <div style="background-color:#319B98; padding:9px">
    <h3 style="color:white;text-align:center;">Predict a 10-year risk of future coronary heart disease</h3>
    </div>
    """  
    st.markdown(html_temp, unsafe_allow_html=True)
    st.subheader(f'Select features and predict with Logistic Regression model')


def main():
    sidebar()
    frontpage()

    # parameters
    gender = st.radio("Gender", ("Female", "Male"))
    age = st.slider("Age", value=45, step=1, min_value=30, max_value=70)
    current_smoker = st.radio("Current Smoker", ("Yes", "No"))
    if current_smoker == 'Yes':
        cigs_per_day = st.slider("The number of cigarettes that the person smoked on average in one day", value=20, step=1, min_value=1, max_value=50)
    else:
        cigs_per_day = 0.0
    total_cholesterol = st.slider("Total Cholesterol", value=230, step=1, min_value=100, max_value=500)
    bp_med = st.radio("Has the patient taken medication for blood pressure?", ("Yes", "No"))
    sys_bp = st.slider("Systolic Blood Pressure", value=130, step=1, min_value=80, max_value=300)
    prevalent_stroke = st.radio("Has the patient had a stroke?", ("Yes", "No"))
    bmi = st.slider("Body Mass Index", value=26, step=1, min_value=15, max_value=60)
    prevalent_hyp = st.radio("Was the patient hypertensive?", ("Yes", "No"))
    heart_rate = st.slider("Heart Rate", value=75, step=1, min_value=15, max_value=150)
    diabetes = st.radio("Has the patient had diabetes?", ("Yes", "No"))
    glucose = st.slider("Glucose Level", value=80, step=1, min_value=40, max_value=400)
    
    # already deployed model
    host = 'https://heart-disease-pred-z.herokuapp.com/'
    url = f'{host}/predict'

    parameters = {
        "age": float(age),
        "cigsPerDay": float(cigs_per_day),
        "totChol": float(total_cholesterol),
        "sysBP": float(sys_bp),
        "BMI": float(bmi),
        "heartRate": float(heart_rate),
        "glucose": float(glucose),
        "male": 1 if gender == 'Male' else 0,
        "currentSmoker": 1 if current_smoker == 'Yes' else 0,
        "BPMeds": 1 if bp_med == 'Yes' else 0,
        "prevalentStroke": 1 if prevalent_stroke == 'Yes' else 0,
        "prevalentHyp": 1 if prevalent_hyp == 'Yes' else 0,
        "diabetes": 1 if diabetes == 'Yes' else 0
    }
    if st.button('Predict Heart Disease'):
        response = requests.post(url, json=parameters).json()
        if response['risk'] == True:
            st.warning(f"There is a {response['disease_probability']*100:.0f}% probability that the person with provided health parameters has 10-year risk of future coronary heart disease")
        else:
            st.success("The person with provided health parameters has NO 10-year risk of future coronary heart disease")


if __name__=='__main__':
    main()