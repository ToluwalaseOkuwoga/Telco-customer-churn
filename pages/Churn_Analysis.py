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
st.title("Customer Churn")
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




df_selection = df.copy()
# converting string values (Yes, No) of Churn columns to 0 and 1

df_selection2 = df_selection.copy()
df_selection2.loc[df_selection2.Churn == 'No', 'Churn'] = 0
df_selection2.loc[df_selection2.Churn == 'Yes', 'Churn'] = 1
df_selection2['Churn'] = df_selection2['Churn'].astype(int)

plot_by_gender = df_selection2.groupby('gender').mean().reset_index()
plot_by_gender = plot_by_gender.sort_values('Churn',ascending=False)

plot_by_SeniorCitizen = df_selection2.groupby('SeniorCitizen').mean().reset_index()
plot_by_SeniorCitizen = plot_by_SeniorCitizen.sort_values('Churn',ascending=False)

plot_by_Partner = df_selection2.groupby('Partner').mean().reset_index()
plot_by_Partner = plot_by_Partner.sort_values('Churn',ascending=False)

plot_by_Dependents = df_selection2.groupby('Dependents').mean().reset_index()
plot_by_Dependents = plot_by_Dependents.sort_values('Churn',ascending=False)

plot_by_tenure_bins = df_selection2.groupby('tenure_bins').mean().reset_index()
plot_by_tenure_bins = plot_by_tenure_bins.sort_values('Churn',ascending=False)

plot_by_Contract = df_selection2.groupby('Contract').mean().reset_index()
plot_by_Contract = plot_by_Contract.sort_values('Churn',ascending=False)

plot_by_PaperlessBilling = df_selection2.groupby('PaperlessBilling').mean().reset_index()
plot_by_PaperlessBilling = plot_by_PaperlessBilling.sort_values('Churn',ascending=False)

plot_by_PaymentMethod = df_selection2.groupby('PaymentMethod').mean().reset_index()
plot_by_PaymentMethod = plot_by_PaymentMethod.sort_values('Churn',ascending=False)

plot_by_PhoneService = df_selection2.groupby('PhoneService').mean().reset_index()
plot_by_PhoneService = plot_by_PhoneService.sort_values('Churn',ascending=False)

plot_by_MultipleLines = df_selection2.groupby('MultipleLines').mean().reset_index()
plot_by_MultipleLines = plot_by_MultipleLines.sort_values('Churn',ascending=False)

plot_by_InternetService = df_selection2.groupby('InternetService').mean().reset_index()
plot_by_InternetService = plot_by_InternetService.sort_values('Churn',ascending=False)

plot_by_OnlineSecurity = df_selection2.groupby('OnlineSecurity').mean().reset_index()
plot_by_OnlineSecurity = plot_by_OnlineSecurity.sort_values('Churn',ascending=False)

plot_by_OnlineBackup = df_selection2.groupby('OnlineBackup').mean().reset_index()
plot_by_OnlineBackup = plot_by_OnlineBackup.sort_values('Churn',ascending=False)

plot_by_DeviceProtection = df_selection2.groupby('DeviceProtection').mean().reset_index()
plot_by_DeviceProtection = plot_by_DeviceProtection.sort_values('Churn',ascending=False)

plot_by_TechSupport = df_selection2.groupby('TechSupport').mean().reset_index()
plot_by_TechSupport = plot_by_TechSupport.sort_values('Churn',ascending=False)

plot_by_StreamingTV = df_selection2.groupby('StreamingTV').mean().reset_index()
plot_by_StreamingTV = plot_by_StreamingTV.sort_values('Churn',ascending=False)

plot_by_StreamingMovies = df_selection2.groupby('StreamingMovies').mean().reset_index()
plot_by_StreamingMovies = plot_by_StreamingMovies.sort_values('Churn',ascending=False)


st.markdown("---")


# TOTAL CHURN [PIE CHART]
fig_churn_rate = px.pie(df_selection, names='Churn',color_discrete_sequence = ['#1c4e80','#0091d5'],
title = "Total Churn",
width=400, height=300
)

fig_churn = px.bar(df_selection['Churn'].value_counts(),color_discrete_sequence = ['#ea6a47','#a5d8dd'],
title="Customers by Churn Status",orientation="h",
width=400, height=300)

#fig_churn.update_yaxes(visible=True, showticklabels=True)
#fig_churn.update_layout(yaxis={'visible': True, 'showticklabels': True})


# TENURE CHURN [BOX CHART]

fig_tenure_churn = px.box(df_selection, x="Churn", y="tenure",title = "Tenure Churn",
color = "Churn",color_discrete_sequence=["#1c4e80","#0091d5"],
width=400, height=300
#title="<b>Sales by hour</b>",
#template="plotly_white",
)


# MONTHLY CHARGES CHURN [BOX CHART]
fig_MonthlyCharges_churn = px.box(df_selection, x="Churn", y="MonthlyCharges",title = "Monthly Charges Churn",
color = "Churn",color_discrete_sequence=["#1c4e80","#0091d5"],
width=400, height=300
#template="plotly_white",
)

fig_demographic_churn = make_subplots(rows=2, cols=2, shared_yaxes=True,
                    subplot_titles=("Gender", "Senior Citizen", "Partner", "Dependents"))

fig_demographic_churn.add_trace(go.Bar(
    x = plot_by_gender['gender'],
    y = plot_by_gender['Churn'],
    width = [0.5,0.5],
    marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),1,1)

fig_demographic_churn.add_trace(go.Bar(
    x = plot_by_SeniorCitizen['SeniorCitizen'],
    y = plot_by_SeniorCitizen['Churn'],
    width = [0.5,0.5],
    marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),1,2)

fig_demographic_churn.add_trace(go.Bar(
    x = plot_by_Partner['Partner'],
    y = plot_by_Partner['Churn'],
    width = [0.5,0.5],
   marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),2,1)

fig_demographic_churn.add_trace(go.Bar(
    x = plot_by_Dependents['Dependents'],
    y = plot_by_Dependents['Churn'],
    width = [0.5,0.5],
    marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),2,2)

fig_demographic_churn.update_layout(showlegend=False,width=600, height=600)

fig_account_churn = make_subplots(rows=2, cols=2, shared_yaxes=True,
                    subplot_titles=("Tenure", "Contract", "Paperless Billing", "Payment Method"))

fig_account_churn.add_trace(go.Bar(
    x = plot_by_tenure_bins['tenure_bins'],
    y = plot_by_tenure_bins['Churn'],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd","#7e909a","#202020"])
    ),1,1)

fig_account_churn.add_trace(go.Bar(
    x = plot_by_Contract['Contract'],
    y = plot_by_Contract['Churn'],
    width = [0.6,0.6,0.6],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),1,2)

fig_account_churn.add_trace(go.Bar(
    x = plot_by_PaperlessBilling['PaperlessBilling'],
    y = plot_by_PaperlessBilling['Churn'],
    width = [0.5,0.5],
    marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),2,1)

fig_account_churn.add_trace(go.Bar(
    x = plot_by_PaymentMethod['PaymentMethod'],
    y = plot_by_PaymentMethod['Churn'],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd","#202020"])
    ),2,2)

fig_account_churn.update_layout(showlegend=False,width=600, height=600)

fig_services_churn = make_subplots(rows=3, cols=3, shared_yaxes=False,
                    subplot_titles=("Phone Service", "Multiple Lines"
                                    , "Internet Service", "Online Security"
                                    ,"Online Backup", "Device Protection"
                                    , "Tech Support", "Streaming TV"
                                    , "Streaming Movies"))

fig_services_churn.add_trace(go.Bar(
    x = plot_by_PhoneService['PhoneService'],
    y = plot_by_PhoneService['Churn'],
    width = [0.5,0.5],
    marker= dict(
    color = ["#1c4e80","#0091d5"])
    ),1,1)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_MultipleLines['MultipleLines'],
    y = plot_by_MultipleLines['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),1,2)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_InternetService['InternetService'],
    y = plot_by_InternetService['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),1,3)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_OnlineSecurity['OnlineSecurity'],
    y = plot_by_OnlineSecurity['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),2,1)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_OnlineBackup['OnlineBackup'],
    y = plot_by_OnlineBackup['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),2,2)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_DeviceProtection['DeviceProtection'],
    y = plot_by_DeviceProtection['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),2,3)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_TechSupport['TechSupport'],
    y = plot_by_TechSupport['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),3,1)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_StreamingTV['StreamingTV'],
    y = plot_by_StreamingTV['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),3,2)

fig_services_churn.add_trace(go.Bar(
    x = plot_by_StreamingMovies['StreamingMovies'],
    y = plot_by_StreamingMovies['Churn'],
    width = [0.7,0.7,0.7],
    marker= dict(
    color = ["#1c4e80","#0091d5","#a5d8dd"])
    ),3,3)

fig_services_churn.update_layout(showlegend=False,width=1200, height=600)



st.subheader("Churn by Tenure and Monthly Charge")

left_column,middle_column,right_column  = st.columns(3)
left_column.plotly_chart(fig_churn_rate, use_container_width=True)
middle_column.plotly_chart(fig_tenure_churn, use_container_width=True)
right_column.plotly_chart(fig_MonthlyCharges_churn, use_container_width=True)

st.markdown("---")
st.subheader("Churn by Demographic and Account")

left_column,right_column  = st.columns(2)
left_column.plotly_chart(fig_demographic_churn, use_container_width=True)
right_column.plotly_chart(fig_account_churn, use_container_width=True)

#st.markdown("---")

#left_column,right_column  = st.columns(2)
#left_column.plotly_chart(fig_demographic_churn, use_container_width=True)
#right_column.plotly_chart(fig_account_churn, use_container_width=True)

st.markdown("---")
st.subheader("Churn by Services")

st.plotly_chart(fig_services_churn, use_container_width=True)


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