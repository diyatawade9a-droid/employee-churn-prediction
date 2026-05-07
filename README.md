# Employee churn prediction App

A Streamlit-based application for managing employee data and predicting employee churn risk.

## Features

- **Employee Management**: Add, edit, delete, and view employee records
- **Dashboard**: Visualize employee attrition data with charts and KPIs
- **Employee Analysis**: Analyze individual employee churn risk with detailed insights
- **Churn Prediction**: Predict employee churn probability based on input features

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Navigate through the sidebar to:
- Add new employee information
- Edit existing employee details
- Delete employee records
- View the employee list

Use the prediction page to input employee details and get churn risk assessment with reasons.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

## Project Structure

```
employee/
├── app.py                 # Main Streamlit application
├── train_model.py         # Model training script
├── test.py                # Test script
├── data/
│   └── dataset.csv        # Employee dataset
├── model/
│   └── model.pkl          # Trained model
└── pages/
    ├── dashboard.py       # Dashboard page
    ├── employee_analysis.py # Employee analysis page
    └── prediction.py      # Churn prediction page
```

## Data

The application uses the IBM HR Analytics Employee Attrition dataset.

## Model

The churn prediction model is trained using Random Forest classifier.