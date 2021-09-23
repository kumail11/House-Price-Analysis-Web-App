import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import pickle

pickle_read = open('forest_model.pkl', 'rb')
my_model = pickle.load(pickle_read)

def province(city):
    if city == 'Karachi':
        return ['Sindh']
    elif city == 'Islamabad':
        return ['Islamabad Capital']
    elif city == 'Lahore' or 'Rawalpindi' or 'Faisalabad':
        return ['Punjab']

def predict_data(model, input_df):
    pred_array = np.array([input_df['property_type'][0], input_df['city'][0], input_df['province_name'][0],
    input_df['baths'][0], input_df['purpose'][0], input_df['bedrooms'][0], input_df['area_sqft'][0]])
    final_array = [pred_array[0], pred_array[1], pred_array[2], pred_array[3],
    pred_array[4], pred_array[5], pred_array[6]]
    predictions = model.predict([final_array])
    return predictions

def run_data():
    st.set_page_config(page_title = 'House Price Analysis App..')
    st.sidebar.header('House Price Analysis App')
    image = Image.open('house.png')
    navbar_value = st.sidebar.selectbox('Navigation', ('Estimate House Rates', 'See the Trends', 'About Me'))
    st.sidebar.info('This app is analysis of housing dataset that contains information extracted from Pakistan\'s biggest property portal, Zameen.com')
    if navbar_value == 'See the Trends':
        st.title("Trends in House prices")
    if navbar_value == 'About Me':
        st.title("About Me")
    if navbar_value == 'Estimate House Rates':
        st.title("Estimate the market price using AI!")
        property_type = st.selectbox('Property Type', ['Flat', 'House'])
        property_cat = 0 if property_type == 'Flat' else 1

        column_1, column_2 = st.beta_columns(2)

        with column_1:
            city = st.selectbox('City', ['Islamabad', 'Lahore', 'Faisalabad', 'Rawalpindi', 'Karachi'])
            city_cat = 0 if city == 'Faisalabad' else 1 if city == 'Islamabad' else 2 if city == 'Karachi' else 3 if city == 'Lahore' else 4
            baths = st.number_input('Baths', min_value = 0, max_value = 3, value = 1)
            area_sqft = st.number_input('Area Sqft', min_value = 60, max_value = 1500, value = 120)

        with column_2:
            prov_arr =  ['Sindh', 'Punjab', 'Islamabad Capital']
            province_name = st.selectbox('Province',options = province(city))
            prov_cat = 0 if province_name == 'Islamabad Capital' else 1 if province_name == 'Punjab' else 2
            bedrooms = st.selectbox('Bedrooms', [0, 1, 2, 3])
            purpose = st.selectbox('Purpose', ['Sale', 'Rent'])
            purpose_cat = 0 if purpose == 'Rent' else 1

        output = ""

        my_dict = {
            'property_type' : property_cat,
            'city' : city_cat,
            'province_name' : prov_cat,
            'baths' : baths,
            'purpose' : purpose_cat,
            'bedrooms' : bedrooms,
            'area_sqft' : area_sqft
        }
        input_df = pd.DataFrame([my_dict])

        column_3 = st.beta_columns(2)
        if st.button('Predict', ):
            output = predict_data(model = my_model, input_df = input_df)
            st.success('The estimated price is '+ str(int(output[0])) + ' PKR')

if __name__ == '__main__':
    run_data()

            

