MODEL_PATH = "churn_model.pkl"

MODEL_COLUMNS = [
    'tenure',
    'MonthlyCharges',
    'TotalCharges',
    'gender_Male',
    'SeniorCitizen_1',
    'MultipleLines_No phone service',
    'MultipleLines_Yes',
    'InternetService_Fiber optic',
    'InternetService_No',
    'PaymentMethod_Credit card (automatic)',
    'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check',
    'Contract_One year',
    'Contract_Two year',
    'Partner_Yes',
    'Dependents_Yes',
    'PhoneService_Yes',
    'OnlineSecurity_No internet service',
    'OnlineSecurity_Yes',
    'OnlineBackup_No internet service',
    'OnlineBackup_Yes',
    'DeviceProtection_No internet service',
    'DeviceProtection_Yes',
    'TechSupport_No internet service',
    'TechSupport_Yes',
    'StreamingTV_No internet service',
    'StreamingTV_Yes',
    'StreamingMovies_No internet service',
    'StreamingMovies_Yes',
    'PaperlessBilling_Yes'
]

DEFAULT_THRESHOLD = 0.40