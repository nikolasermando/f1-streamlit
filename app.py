# -*- coding: utf-8 -*-
"""
Created on Sat May  7 00:43:18 2022

@author: Nikolas Ermando
"""

import streamlit as st
import pandas as pd
import pickle
import datetime
from PIL import Image

image = Image.open("Ferrari-F1-1998.png")

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

st.image(image)
st.markdown("<h1 style='text-align: center; '>F1 Machine Learning Prediction</h2>", unsafe_allow_html=True)
st.markdown("---")

circuit_info = pd.read_csv('circuit_info.csv')
driver_info = pd.read_csv('driver_info.csv').sort_values(by='fullname')
constructor_info = pd.read_csv('constructor_info.csv').sort_values(by='constructor')
new_circuit = pd.DataFrame({'circuit':'Miami International Autodrome','country':'USA'},index=[0])
circuit_info = pd.concat((circuit_info, new_circuit),ignore_index = True, axis=0).sort_values(by='circuit')

driver_name = st.selectbox('Your Driver Name', driver_info['fullname'])
constructor_name = st.selectbox('Constructor Name', constructor_info['constructor'])
circuit_name = st.selectbox('Circuit Name', circuit_info['circuit'])
grid_info = st.selectbox('Starting Grid',range(1,21))
date_name = st.date_input("Race Date",datetime.datetime(2022, 5, 6))
dob_name = driver_info[driver_info['fullname']==driver_name]['dob'].tolist()[0]
age_gap = (datetime.datetime(date_name.year, date_name.month, date_name.day) - datetime.datetime.strptime(dob_name, '%Y-%m-%d'))
age_gap = int(age_gap.total_seconds()) // 31536000

data = {'grid':grid_info,
        'age_gap':age_gap}
driver_dict = {}
constructor_dict={}
circuit_dict={}


for circuit in circuit_info['circuit'].sort_values():
    x = circuit.replace("-","_").replace(" ","_")
    y = int(circuit == circuit_name)
    circuit_dict["circuit_{0}".format(circuit)] = y

for driver in driver_info['fullname'].sort_values():
    x = driver.replace("-","_").replace(" ","_")
    y = int(driver == driver_name)
    driver_dict["fullname_{0}".format(driver)] = y
    
for constructor in constructor_info['constructor'].sort_values():
    x = constructor.replace("-","_").replace(" ","_")
    y = int(constructor == constructor_name)
    constructor_dict["constructor_{0}".format(constructor)] = y
    
data.update(circuit_dict)
data.update(driver_dict)
data.update(constructor_dict)
del data["constructor_Alfa Romeo"]
del data["circuit_Miami International Autodrome"]
del data["fullname_Alexander Albon"]

input_df = pd.DataFrame(data,index=[0])



def prediction_desc():
    prediction = loaded_model.predict(input_df)    
    if prediction == 1:
        st.markdown("<h2 style='text-align: center; '>Podium Point</h2>", unsafe_allow_html=True)
    elif prediction == 2:
        st.markdown("<h2 style='text-align: center; '>Top 10 Point</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; '>No Point</h2>", unsafe_allow_html=True)

button = st.button("Predict!!")

if button:
    prediction_desc()