import streamlit as st
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import pandas as pd
import pickle

#load the trained mode
model=tf.keras.models.load_model('model.h5')

##load the encoder and scaler
with open('ohe.pkl','rb') as file:
    ohe=pickle.load(file)

with open('label_gender.pkl','rb') as file:
    label_gender=pickle.load(file)
    
with open('scaler.pkl','rb') as file:
    scaler=pickle.load(file)
    
##streamlit app
st.title("customer churn prediction")
geography=st.selectbox('Geography',ohe.categories_[0])
gender=st.selectbox('Gender',label_gender.classes_)
age=st.slider('Age',18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
estimated_salary=st.number_input('Estimated Salary')
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number of Prodcuts',1,4)
has_cr_card=st.selectbox('Has Credit Card',[0,1])
is_active_member=st.selectbox('Is Active Member',[0,1])

##prepare the input data
input_data=pd.DataFrame({
    'CreditScore':[credit_score],
    'Gender':[label_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'EstimatedSalary':[estimated_salary]
})

#one hot encode 'Geography'
geo_encoded=ohe.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=ohe.get_feature_names_out(['Geography']))

##combine one hot encoded columns with input data
input_data=pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)

#scale the input data
input_data_scaled=scaler.transform(input_data)

##predict churn
prediction=model.predict(input_data_scaled)
prediction_proba=prediction[0][0]

st.write(f'Churn probability:{prediction_proba:.2f}')

if prediction_proba>0.5 :
    st.write('the customer is likely to churn')
else:
    st.write('the customer is not likely to churn.')
