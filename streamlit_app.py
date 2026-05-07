import os

import pandas as pd
import streamlit as st

st.title("My Streamlit App")
st.write("Deployment successful!")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "dataset.csv")

ATTRITION_OPTIONS = ["Yes", "No"]
GENDER_OPTIONS = ["Male", "Female"]
DEPARTMENT_OPTIONS = ["Sales", "Research & Development", "Human Resources"]
JOB_ROLE_OPTIONS = [
    "Sales Executive",
    "Research Scientist",
    "Laboratory Technician",
    "Manager"
]

st.set_page_config(page_title="Employee Manager", layout="wide")
st.title("Employee Manager")


tab1, tab2, tab3, tab4 = st.tabs(["Add Employee", "Edit Employee", "Delete Employee", "View Employees"])


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def save_data(df: pd.DataFrame) -> None:
    df.to_csv(DATA_PATH, index=False)


def get_default_int(default_value, fallback=0):
    try:
        return int(default_value)
    except (TypeError, ValueError):
        return fallback


def employee_fields(defaults=None):
    defaults = defaults or {}

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=get_default_int(defaults.get("Age"), 30),
    )
    gender = st.selectbox(
        "Gender",
        GENDER_OPTIONS,
        index=GENDER_OPTIONS.index(defaults.get("Gender", "Male")),
    )
    department = st.selectbox(
        "Department",
        DEPARTMENT_OPTIONS,
        index=DEPARTMENT_OPTIONS.index(defaults.get("Department", "Sales")),
    )
    job_role = st.selectbox(
        "Job Role",
        JOB_ROLE_OPTIONS,
        index=JOB_ROLE_OPTIONS.index(defaults.get("JobRole", "Sales Executive")),
    )
    monthly_income = st.number_input(
        "Monthly Income",
        min_value=0,
        value=get_default_int(defaults.get("MonthlyIncome"), 3000),
    )
    years_at_company = st.number_input(
        "Years at Company",
        min_value=0,
        value=get_default_int(defaults.get("YearsAtCompany"), 1),
    )
    attrition = st.selectbox(
        "Attrition",
        ATTRITION_OPTIONS,
        index=ATTRITION_OPTIONS.index(defaults.get("Attrition", "No")),
    )

    return {
        "Age": age,
        "Gender": gender,
        "Department": department,
        "JobRole": job_role,
        "MonthlyIncome": monthly_income,
        "YearsAtCompany": years_at_company,
        "Attrition": attrition,
        "BusinessTravel": defaults.get("BusinessTravel", "Travel_Rarely"),
        "DailyRate": get_default_int(defaults.get("DailyRate"), 0),
        "DistanceFromHome": get_default_int(defaults.get("DistanceFromHome"), 0),
        "Education": get_default_int(defaults.get("Education"), 3),
        "EducationField": defaults.get("EducationField", "Life Sciences"),
        "EmployeeCount": 1,
        "EnvironmentSatisfaction": get_default_int(defaults.get("EnvironmentSatisfaction"), 3),
        "HourlyRate": get_default_int(defaults.get("HourlyRate"), 0),
        "JobInvolvement": get_default_int(defaults.get("JobInvolvement"), 1),
        "JobLevel": get_default_int(defaults.get("JobLevel"), 1),
        "JobSatisfaction": get_default_int(defaults.get("JobSatisfaction"), 3),
        "MaritalStatus": defaults.get("MaritalStatus", "Single"),
        "MonthlyRate": get_default_int(defaults.get("MonthlyRate"), 0),
        "NumCompaniesWorked": get_default_int(defaults.get("NumCompaniesWorked"), 0),
        "Over18": "Y",
        "OverTime": defaults.get("OverTime", "No"),
        "PercentSalaryHike": get_default_int(defaults.get("PercentSalaryHike"), 0),
        "PerformanceRating": get_default_int(defaults.get("PerformanceRating"), 3),
        "RelationshipSatisfaction": get_default_int(defaults.get("RelationshipSatisfaction"), 3),
        "StandardHours": 80,
        "StockOptionLevel": get_default_int(defaults.get("StockOptionLevel"), 0),
        "TotalWorkingYears": get_default_int(defaults.get("TotalWorkingYears"), years_at_company),
        "TrainingTimesLastYear": get_default_int(defaults.get("TrainingTimesLastYear"), 0),
        "WorkLifeBalance": get_default_int(defaults.get("WorkLifeBalance"), 3),
        "YearsInCurrentRole": get_default_int(defaults.get("YearsInCurrentRole"), 0),
        "YearsSinceLastPromotion": get_default_int(defaults.get("YearsSinceLastPromotion"), 0),
        "YearsWithCurrManager": get_default_int(defaults.get("YearsWithCurrManager"), 0),
    }


def main():
    df = load_data()

    with tab1:
        st.subheader("Add a new employee")
        with st.form("add_form"):
            employee_data = employee_fields()
            submit = st.form_submit_button("Add")

        if submit:
            next_emp_num = int(df["EmployeeNumber"].max() + 1) if not df.empty else 1
            employee_data["EmployeeNumber"] = next_emp_num
            df = pd.concat([df, pd.DataFrame([employee_data])], ignore_index=True)
            save_data(df)
            st.success(f"Added employee {next_emp_num}.")
            st.dataframe(df.tail(5))

    with tab2:
        st.subheader("Edit employee details")
        if df.empty:
            st.warning("No employees to edit.")
            return

        selected_emp = st.selectbox(
            "Select employee",
            df["EmployeeNumber"].tolist(),
            format_func=lambda x: f"Employee {x}",
            key="edit_select"
        )
        employee_row = df.loc[df["EmployeeNumber"] == selected_emp].iloc[0]

        with st.form("edit_form"):
            updated_data = employee_fields(employee_row.to_dict())
            submit = st.form_submit_button("Save")

        if submit:
            for key, value in updated_data.items():
                df.loc[df["EmployeeNumber"] == selected_emp, key] = value
            save_data(df)
            st.success(f"Updated employee {selected_emp}.")
            st.dataframe(df.loc[df["EmployeeNumber"] == selected_emp])

    with tab3:
        st.subheader("Delete employee")
        if df.empty:
            st.warning("No employees to delete.")
            return

        selected_emp = st.selectbox(
            "Select employee",
            df["EmployeeNumber"].tolist(),
            format_func=lambda x: f"Employee {x}",
            key="delete_select"
        )
        st.write(df.loc[df["EmployeeNumber"] == selected_emp])

        if st.button("Delete"):
            df = df[df["EmployeeNumber"] != selected_emp].reset_index(drop=True)
            save_data(df)
            st.success(f"Deleted employee {selected_emp}.")
            st.dataframe(df.head(10))

    with tab4:
        st.subheader("Employees")
        display_cols = [
            "EmployeeNumber",
            "Age",
            "Gender",
            "Department",
            "JobRole",
            "MonthlyIncome",
            "YearsAtCompany",
            "Attrition",
        ]
        st.dataframe(df[display_cols] if all(col in df.columns for col in display_cols) else df)


if __name__ == "__main__":
    main()