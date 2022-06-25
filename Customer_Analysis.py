from click import option
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import chi2_contingency, pointbiserialr
from sklearn.metrics import mutual_info_score
import streamlit as st

st.set_page_config(page_title = "Customer Churn Dashboard",
                page_icon = ":bar_chart:",
                layout = "wide"
)

df = pd.read_csv('Telco-Customer-Churn.csv')

# ---- MAIN PAGE ----
st.title("Customer Analysis")
#st.markdown("##")

# DATA CLEANING
df.loc[df['tenure'] <= 5, 'tenure_bins'] = '1-5' 
df.loc[(df['tenure'] <= 10) & (df['tenure'] > 5), 'tenure_bins'] = '6-10'
df.loc[(df['tenure'] <= 20) & (df['tenure'] > 10), 'tenure_bins'] = '11-20' 
df.loc[(df['tenure'] <= 30) & (df['tenure'] > 20), 'tenure_bins'] = '21-30'
df.loc[(df['tenure'] > 30), 'tenure_bins'] = '+30'

df.loc[df.SeniorCitizen == 1, 'SeniorCitizen'] = 'Yes'
df.loc[df.SeniorCitizen == 0, 'SeniorCitizen'] = 'No'


df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())

#df.drop('customerID', axis=1, inplace=True)

# for selecting all
#Gender = st.container()
#all = st.checkbox("Select all")
 
#if all:
#    selected_options = Gender.multiselect("Select Gender:",
#         df["gender"].unique(),df["gender"].unique())
#else:
#    selected_options =  Gender.multiselect("Select Gender:",
#        df["gender"].unique())

#df = df[df["gender"].isin(selected_options)]


customers3 = df[['customerID','StreamingTV','OnlineSecurity','OnlineBackup','DeviceProtection'
                        ,'TechSupport','StreamingMovies','Churn']].copy()

# converting string values of the columns to 0 and 1

customers3.loc[customers3.Churn == 'No', 'Churn'] = 0
customers3.loc[customers3.Churn == 'Yes', 'Churn'] = 1
customers3['Churn'] = customers3['Churn'].astype(int)

customers3.loc[customers3.StreamingTV == 'No', 'StreamingTV'] = 0
customers3.loc[customers3.StreamingTV == 'No internet service', 'StreamingTV'] = 0
customers3.loc[customers3.StreamingTV == 'Yes', 'StreamingTV'] = 1
customers3['StreamingTV'] = customers3['StreamingTV'].astype(int)

customers3.loc[customers3.OnlineSecurity == 'No', 'OnlineSecurity'] = 0
customers3.loc[customers3.OnlineSecurity == 'No internet service', 'OnlineSecurity'] = 0
customers3.loc[customers3.OnlineSecurity == 'Yes', 'OnlineSecurity'] = 1
customers3['OnlineSecurity'] = customers3['OnlineSecurity'].astype(int)

customers3.loc[customers3.OnlineBackup == 'No', 'OnlineBackup'] = 0
customers3.loc[customers3.OnlineBackup == 'No internet service', 'OnlineBackup'] = 0
customers3.loc[customers3.OnlineBackup == 'Yes', 'OnlineBackup'] = 1
customers3['OnlineBackup'] = customers3['OnlineBackup'].astype(int)

customers3.loc[customers3.DeviceProtection == 'No', 'DeviceProtection'] = 0
customers3.loc[customers3.DeviceProtection == 'No internet service', 'DeviceProtection'] = 0
customers3.loc[customers3.DeviceProtection == 'Yes', 'DeviceProtection'] = 1
customers3['DeviceProtection'] = customers3['DeviceProtection'].astype(int)

customers3.loc[customers3.TechSupport == 'No', 'TechSupport'] = 0
customers3.loc[customers3.TechSupport == 'No internet service', 'TechSupport'] = 0
customers3.loc[customers3.TechSupport == 'Yes', 'TechSupport'] = 1
customers3['TechSupport'] = customers3['TechSupport'].astype(int)

customers3.loc[customers3.StreamingMovies == 'No', 'StreamingMovies'] = 0
customers3.loc[customers3.StreamingMovies == 'No internet service', 'StreamingMovies'] = 0
customers3.loc[customers3.StreamingMovies == 'Yes', 'StreamingMovies'] = 1
customers3['StreamingMovies'] = customers3['StreamingMovies'].astype(int)


customers3['ServiceNumber'] = customers3['OnlineSecurity']+customers3['OnlineBackup']+customers3['DeviceProtection']+customers3['TechSupport']+customers3['StreamingTV']+customers3['StreamingMovies']

def label_race (row):
    if row['ServiceNumber'] == 1 :
      return 'One'
    if row['ServiceNumber'] == 2 :
      return 'Two'
    if row['ServiceNumber'] == 3 :
      return 'Three'
    if row['ServiceNumber'] == 4:
      return 'Four'
    if row['ServiceNumber']  == 5:
      return 'Five'
    if row['ServiceNumber']  == 6:
      return 'Six'
    return 'None'

customers3['NumberOfServices'] = customers3.apply (lambda row: label_race(row), axis=1)

customers3 = customers3[['customerID','NumberOfServices']].copy()

df = pd.merge(left = df, 
         right = customers3,
        how= 'outer',
        left_on=['customerID'],
        right_on=['customerID'],
        )

#Gender = st.multiselect("Choose Gender", df["gender"].unique(), df["gender"].unique())
#df = df[df["gender"].isin(Gender)]



# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
#Gender = st.sidebar.multiselect(
 #   "Select the Gender:",
 #   options=df["gender"].unique(),
 #   default=df["gender"].unique(),
#)

 #for selecting all
NumberOfServices = st.sidebar.container()
all = st.sidebar.checkbox("Select all",value=True)
 
if all:
    selected_options = NumberOfServices.multiselect("Select Number Of Services:",
         df["NumberOfServices"].unique(),df["NumberOfServices"].unique())
else:
    selected_options =  NumberOfServices.multiselect("Select Number Of Services:",
        df["NumberOfServices"].unique())

df = df[df["NumberOfServices"].isin(selected_options)]


#Service = df["NumberOfServices"].unique()
#l2 = np.append(Service, 'Select all')
#Services = st.sidebar.multiselect('Service',l2)
#if 'Select all' in Services :
#	Services=Service



Tenure = st.sidebar.multiselect(
    "Select the Tenure:",
    options=df["tenure_bins"].unique(),
    default=df["tenure_bins"].unique(),
)

Partner_Status = st.sidebar.multiselect(
    "Select the Partner Status:",
    options=df["Partner"].unique(),
    default=df["Partner"].unique(),
)

df_selection = df.query(
    "tenure_bins ==@Tenure & Partner ==@Partner_Status"
)


total_charges = int(df_selection["TotalCharges"].sum())
monthly_charges = int(df_selection["MonthlyCharges"].sum())
no_of_customers = int(len(df_selection.index))
avg_tenure = round(df_selection["tenure"].mean(), 2)

# create four columns
customer, monthly, total, tenure = st.columns(4)

# fill in those three columns with respective metrics or KPIs
customer.metric(
    label="Number of Customers 🧑🏽‍🦱",
    value=round(no_of_customers),
)

monthly.metric(
    label="Monthly Charges 💵",
    value=f"$ {monthly_charges:,} ",
)

total.metric(
    label="Total Charges 💵",
    value=f"$ {total_charges:,} ",
)

tenure.metric(
    label="Average Tenure 🧑🏽‍🦱",
    value=(avg_tenure),
)

st.markdown("---")





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

#st.dataframe(df_selection)