import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Employee Churn Dashboard")

# Load data
df = pd.read_csv("data/dataset.csv")

# KPIs
total_emp = len(df)
attrition_rate = (df["Attrition"] == "Yes").mean() * 100
high_risk = df[df["Attrition"] == "Yes"].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Employees", total_emp)
col2.metric("Attrition Rate", f"{attrition_rate:.2f}%")
col3.metric("Employees Left", high_risk)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    fig = px.pie(df, names="Attrition", title="Attrition Distribution",
                 color="Attrition",
                 color_discrete_map={"Yes": "#0F4C81", "No": "#8FBFE0"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df, x="Department", color="Attrition",
                 title="Attrition by Department", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# Age distribution
fig = px.histogram(df, x="Age", color="Attrition",
                   title="Age Distribution by Attrition")
st.plotly_chart(fig, use_container_width=True)

# Correlation heatmap
numeric_df = df.select_dtypes(include=['int64', 'float64'])
corr = numeric_df.corr()

fig = px.imshow(corr, text_auto=True, title="Feature Correlation Heatmap")
st.plotly_chart(fig, use_container_width=True)