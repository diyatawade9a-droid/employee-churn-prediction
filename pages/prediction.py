import numpy as np
import pickle
import streamlit as st

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# Example input (must be 4 features in SAME order as training)
# Age, MonthlyIncome, TotalWorkingYears, gender_encoded
input_data = np.array([[35, 50000, 10, 1]])

# Prediction
prediction = model.predict(input_data)[0]

# Convert result back to label
result = "Yes (Will Leave)" if prediction == 1 else "No (Will Stay)"

print("Prediction:", result)

# Prediction
age = st.number_input("Enter Age")
salary = st.number_input("Enter Salary")
experience = st.number_input("Enter Experience")

gender = st.selectbox("Gender", ["Male", "Female"])

gender_encoded = 1 if gender == "Male" else 0

if st.button("Predict", key="predict_btn"):
    prediction = model.predict([[age, salary, experience, gender_encoded]])[0]
    prob = model.predict_proba([[age, salary, experience, gender_encoded]])[0][1]

    st.subheader("Result")

    if prob > 0.7:
        st.error(f"🚨 High Risk of Churn ({prob*100:.2f}%)")
        st.write("**Reason:** Employee shows strong indicators of leaving. Consider retention strategies immediately.")
    elif prob > 0.4:
        st.warning(f"⚠ Medium Risk of Churn ({prob*100:.2f}%)")
        st.write("**Reason:** Employee may leave. Monitor engagement and satisfaction levels.")
    else:
        st.success(f"✅ Low Risk of Churn ({prob*100:.2f}%)")
        st.write("**Reason:** Employee appears satisfied and committed to the organization.")