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

# Feature encoding mappings
BINARY_FEATURES = {
    'gender': ('gender_Male', 'Male'),
    'senior_citizen': ('SeniorCitizen_1', 'Yes'),
    'partner': ('Partner_Yes', 'Yes'),
    'dependents': ('Dependents_Yes', 'Yes'),
    'phone_service': ('PhoneService_Yes', 'Yes'),
    'paperless_billing': ('PaperlessBilling_Yes', 'Yes'),
}

MULTI_STATE_FEATURES = {
    'multiple_lines': ('MultipleLines', ['No phone service', 'Yes']),
    'internet_service': ('InternetService', ['Fiber optic', 'No']),
    'contract': ('Contract', ['One year', 'Two year']),
    'payment_method': ('PaymentMethod', ['Credit card (automatic)', 'Electronic check', 'Mailed check']),
    'online_security': ('OnlineSecurity', ['Yes', 'No internet service']),
    'online_backup': ('OnlineBackup', ['Yes', 'No internet service']),
    'device_protection': ('DeviceProtection', ['Yes', 'No internet service']),
    'tech_support': ('TechSupport', ['Yes', 'No internet service']),
    'streaming_tv': ('StreamingTV', ['Yes', 'No internet service']),
    'streaming_movies': ('StreamingMovies', ['Yes', 'No internet service']),
}

NUMERIC_FEATURES = ['tenure', 'MonthlyCharges', 'TotalCharges']
NUMERIC_TO_DF_MAPPING = {
    'tenure': 'tenure',
    'monthly_charges': 'MonthlyCharges',
    'total_charges': 'TotalCharges',
}