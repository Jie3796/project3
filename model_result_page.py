import numpy as np
import pandas as pd
import streamlit as st
from model_predict import model_predict

def show_model_result():
    # print model result
    st.subheader("Model result")
    st.write("We explored several machine learning approaches, including KNN, SVM, Random Forest and AdaBoost. Below are the prediction results of different models:")
    data = {
        'Model': ['KNN', 'SVM', 'Random Forest', 'AdaBoost'],
        'Best Param': ['p: 1 \n n_neighbors: 19 \n weights: distance \n Metric: manhattan',
                       'kernel: rbf, C: 100, gamma: scale',
                       'n_estimators: 100, max_features: sqrt',
                       'n_estimators: 100, learning_rate: 100'],
        'Accuracy(%)': ['50.56', '52.94', '54.53', '54.05']
    }
    model_result_df = pd.DataFrame(data)
    st.table(model_result_df)
   

def show_model_predict():
    st.subheader("Diabetes Risk Prediction")
    st.write("Please select a model, then slide the corresponding feature values to predict diabetes risk.")
    
    features = ["Access to Exercise Opportunities", "Children in Poverty", "Food Insecurity",
            "Household with No Internet Service", "Number of Dentists", "Overall SVI",
            "Severe Housing Cost Burden", "Urban_Rural"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    model_name = st.selectbox('Select Prediction Model: ', ['KNN', 'SVM', 'RandomForest', 'AdaBoost'], 2)
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Slider of Access to Exercise Opportunities & Children in Poverty
    col1, spacer, col2 = st.columns([1, 0.1, 1]) # Create three columns, where the middle one acts as a spacer
    exercise_oppo = col1.slider('Access to Exercise Opportunities: ', min_value=0, max_value=100, value=50)
    children_poverty = col2.slider("Children in Poverty: ", min_value=0, max_value=100, value=18)

    # Slider of Food Insecurity & ousehold with No Internet Service
    col3, spacer, col4 = st.columns([1, 0.1, 1])
    food_insecurity = col3.slider("Food Insecurity: ", min_value=0, max_value=100, value=13)
    household_service = col4.slider("Household with No Internet Service: ", min_value=0, max_value=100, value=20)

    col5, spacer, col6 = st.columns([1, 0.1, 1])
    number_dentists = col5.slider("Number of Dentists: ", min_value=0, max_value=5000, value=80)
    overall_svi = col6.slider(r"Overall SVI ( $10^{-2}$ ): ", min_value=0, max_value=100, value=50)
    overall_svi /= 100

    col7, spacer, col8 = st.columns([1, 0.1, 1])
    severe_housing_burden = col7.slider("Severe Housing Cost Burden: ", min_value=0, max_value=100, value=10)
    urban_rural = col8.selectbox('Urban or Rural: ', ['Urban', 'Rural'], 0)
    is_urban = 1 if urban_rural == 'Urban' else 0

    st.markdown("<br>", unsafe_allow_html=True)
    # predition button
    press_button = st.button('Predict')
  
    # Add the "Predict" button
    if press_button:
        data = pd.DataFrame([[exercise_oppo, children_poverty, food_insecurity, household_service,
                             number_dentists, overall_svi, severe_housing_burden, is_urban]], columns=features)
        result = model_predict(data, model_name)
        st.write(fr"**Predict Result: {result}**")
     
