from click import option
import pandas as pd
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

df.drop('customerID', axis=1, inplace=True)

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


Gender = df["gender"].unique()
options = st.multiselect("Choose Gender", Gender, Gender)

df = df[df["gender"].isin(options)]


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
#Gender = st.sidebar.multiselect(
 #   "Select the Gender:",
 #   options=df["gender"].unique(),
 #   default=df["gender"].unique(),
#)

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