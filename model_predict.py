import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import QuantileTransformer
import joblib
import os

risk_label = {2: "High Risk", 1: "Medium Risk", 0: "Low Risk"} 
def data_processing(data):
    quantile = joblib.load('model/quantile_transformer.pkl')
    handle_features = ['Access to Exercise Opportunities', 'Children in Poverty', 'Food Insecurity', 'Household with No Internet Service', 'Number of Dentists', 'Overall SVI', 'Severe Housing Cost Burden']
    select_data = data[handle_features]
    
    select_data = quantile.transform(select_data)
    
    data_new=pd.DataFrame(select_data)
    data_new.columns = handle_features
    data_new['Urban_Rural'] = data['Urban_Rural']
    # data_new['Risk Category'] = data['Risk Category']
    return data_new
    
def model_predict(data, model_name="RandomForest"):
    data = data_processing(data)
    cur_path = os.getcwd()
    model = joblib.load(cur_path + "/model/" + model_name.lower() + ".pkl")
    model_result = model.predict(data)[0]
    print(model_result)
    return risk_label[model_result]
    
    
