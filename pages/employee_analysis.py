import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px

st.set_page_config(page_title="Employee Analysis", layout="wide")

st.title("👤 Employee Analysis")

# ---------------------------
# Safe file loading
# ---------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "churn_model.pkl")

df = pd.read_csv(DATA_PATH)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ---------------------------
# Employee selection
# ---------------------------
emp_id = st.selectbox("Select Employee Index", df.index)

emp = df.loc[[emp_id]]  # keep DataFrame format

st.subheader("Employee Details")
st.dataframe(emp)

# ---------------------------
# Prepare input safely
# ---------------------------
X = emp.drop("Attrition", axis=1, errors="ignore")

# Align features with model (IMPORTANT FIX)
if hasattr(model, "feature_names_in_"):
    X = X.reindex(columns=model.feature_names_in_, fill_value=0)

# ---------------------------
# Prediction
# ---------------------------
prediction = model.predict(X)[0]
prob = model.predict_proba(X)[0][1]

# ---------------------------
# Display results
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.metric("Churn Prediction", "Yes" if prediction == 1 else "No")

with col2:
    st.metric("Churn Probability", f"{prob*100:.2f}%")

# ---------------------------
# Risk chart
# ---------------------------
risk_df = pd.DataFrame({
    "Risk": ["Low", "Medium", "High"],
    "Value": [0.3, 0.6, 1.0]
})

fig = px.bar(risk_df, x="Risk", y="Value", title="Risk Level Indicator")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Feature importance (safe check)
# ---------------------------
if hasattr(model, "feature_importances_"):
    importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    fig = px.bar(
        importance.head(10),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top Factors Affecting Churn"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Recommendation logic
# ---------------------------
st.subheader("💡 Recommendation")

if prob > 0.7:
    st.error("High Risk: Consider retention strategies (salary hike, workload balance).")
elif prob > 0.4:
    st.warning("Medium Risk: Monitor employee engagement.")
else:
    st.success("Low Risk: No immediate action needed.")