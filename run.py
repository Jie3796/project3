import streamlit as st
import pandas as pd
from data_explorer_page import county_data_explorer
from model_result_page import show_model_result, show_model_predict
import os
PAGES = ['Exploratory Data Analysis', 'Diabetes Prediction']

# read_data
def prepocess_data(data_path="data/data_cleaned.csv"):
    data = pd.read_csv(data_path)
    data = data.dropna(subset=['County_FIPS'])
    risk_probality = [8, 10] # 三个类别的分界点，少于8%为'Low Risk'，大于12%为'High Risk'，中间为'Medium Risk'，这个分界点是根据数据的分布来定的，可以根据需要调整
    risk_label = {"High Risk": 2, "Medium Risk": 1, "Low Risk": 0} 
    def categorize_risk(percentage):
        if percentage > risk_probality[1]:
            return risk_label["High Risk"]
        elif percentage > risk_probality[0]:
            return risk_label["Medium Risk"]
        else:
            return risk_label["Low Risk"]

    data['Risk Category'] = data['Diagnosed Diabetes Percentage'].apply(categorize_risk)
    return data

# Page 1
def data_explor_page(data):
    st.header("Exploratory Data Analysis")
    # st.write("欢迎来到页面 1!")
    county_data_explorer(data)

# Page 2
def model_analysis_page():
    st.header("Diabetes Prediction")
    
    show_model_result()
    show_model_predict()
    
    
def main():
    # 在侧边栏中选择页面
    page=st.sidebar.radio('Navigation', PAGES)
    cur_path = os.getcwd()
    print(cur_path)
    data = prepocess_data(cur_path + '/data/data_cleaned.csv')

    # 根据选择调用相应的函数
    if page == 'Exploratory Data Analysis':
        data_explor_page(data)
    elif page == 'Diabetes Prediction':
        model_analysis_page()


if __name__ == "__main__":
    main()
