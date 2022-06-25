import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
import streamlit as st

st.set_page_config(page_title = "Customer Churn Dashboard",
                page_icon = ":bar_chart:",
                layout = "wide"
)

customers = pd.read_csv('Telco-Customer-Churn.csv')

customers.loc[customers.SeniorCitizen == 1, 'SeniorCitizen'] = 'Yes'
customers.loc[customers.SeniorCitizen == 0, 'SeniorCitizen'] = 'No'

customers['TotalCharges'] = pd.to_numeric(customers['TotalCharges'], errors='coerce')
customers['TotalCharges'] = customers['TotalCharges'].fillna(customers['TotalCharges'].median())

categorical = ['SeniorCitizen', 'Partner', 'Dependents','InternetService','MultipleLines',
               'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
               'TechSupport', 'StreamingTV', 'StreamingMovies',
               'Contract', 'PaperlessBilling', 'PaymentMethod']


data = customers.drop(['customerID','gender','PhoneService','TotalCharges'], axis=1)

data.loc[data.Churn == 'Yes', 'Churn'] = 1
data.loc[data.Churn == 'No', 'Churn'] = 0

X = data.drop('Churn', axis = 'columns')
y = data.Churn
y=y.astype('int')

lr = LogisticRegression(solver='lbfgs', max_iter=1000)

ohe = OneHotEncoder(sparse=False)
ohe.fit_transform(data)

transformer = make_column_transformer((ohe, categorical), remainder='passthrough')
transformer.fit_transform(X)

pipe = make_pipeline(transformer, lr)

#model = pickle.load(open('model.sav', 'rb'))

st.title('Customer Churn Prediction')


# FUNCTION
def user_report():
  SeniorCitizen = st.selectbox("Is the Customer a Senior Citizen?", customers["SeniorCitizen"].unique(),)
  Partner = st.selectbox("Does the Customer have a Partner?", customers["Partner"].unique(),)
  Dependents = st.selectbox("Does the Customer have Dependents?", customers["Dependents"].unique(),)
  MultipleLines = st.selectbox("Does the Customer have Multiple Lines?", customers["MultipleLines"].unique(),)
  InternetService = st.selectbox("Which Internet Service does the Customer use?", customers["InternetService"].unique(),)
  OnlineSecurity = st.selectbox("Is the Customer subscribed for Online Security?", customers["OnlineSecurity"].unique(),)
  OnlineBackup = st.selectbox("Is the Customer subscribed for  Online Backup?", customers["OnlineBackup"].unique(),)
  DeviceProtection = st.selectbox("Is the Customer subscribed for  Device Protection?", customers["DeviceProtection"].unique(),)
  TechSupport = st.selectbox("Is the Customer subscribed for  Tech Support?", customers["TechSupport"].unique(),)
  StreamingTV = st.selectbox("Is the Customer subscribed for  Streaming TV?", customers["StreamingTV"].unique(),)
  StreamingMovies = st.selectbox("Is the Customer subscribed for  Streaming Movies?", customers["StreamingMovies"].unique(),)
  Contract = st.selectbox("Contract Length", customers["Contract"].unique(),)
  PaperlessBilling = st.selectbox("Does the Customer use Paperless Billing?", customers["PaperlessBilling"].unique(),)
  PaymentMethod = st.selectbox("Which Payment Method does the Customer use?", customers["PaymentMethod"].unique(),)
  tenure = st.slider('How many months has the Customer been with the company?', 50,100, 1 )
  MonthlyCharges = st.number_input('How much is the Customer charged Monthly? $')

  user_report_data = {
      'SeniorCitizen':SeniorCitizen,
      'Partner':Partner,
      'Dependents':Dependents,
      'MultipleLines':MultipleLines,
      'InternetService':InternetService,
      'OnlineSecurity':OnlineSecurity,
      'OnlineBackup':OnlineBackup,
      'DeviceProtection':DeviceProtection,
      'TechSupport':TechSupport,
      'StreamingTV':StreamingTV,
      'StreamingMovies':StreamingMovies,
      'Contract':Contract,
      'PaperlessBilling':PaperlessBilling,
      'PaymentMethod':PaymentMethod,
      'tenure':tenure,
      'MonthlyCharges':MonthlyCharges
  }
  report_data = pd.DataFrame(user_report_data, index=[0])
  return report_data

user_data = user_report()
st.header('Customer Data')
st.write(user_data)


pipe.fit(X, y)


if st.button("Predict"):
    Churn = pipe.predict(user_data)
    if Churn[0] == 0:
        st.success('Employee will not churn')
    elif Churn[0] == 1:
        st.error( 'Employee will churn')


#Churn = pipe.predict(user_data)
#st.subheader('Probablilty of Churn')
#st.subheader(str(np.round(Churn[0], 2)))

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("---")


