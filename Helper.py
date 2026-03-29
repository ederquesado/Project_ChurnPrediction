import joblib
import pandas as pd
import Const

def load_model():
    return joblib.load(Const.MODEL_PATH)

def empty_input_df() -> pd.DataFrame:
    return pd.DataFrame([[0] * len(Const.MODEL_COLUMNS)], columns=Const.MODEL_COLUMNS)

def set_binary(df: pd.DataFrame, column_name: str, condition: bool) -> None:
    if condition and column_name in df.columns:
        df.at[0,column_name] =1

def apply_three_state_service(
        df: pd.DataFrame,
        feature_prefix: str,
        selected_value: str
) -> None:
    no_internet_col = f'{feature_prefix}_No internet service'
    yes_col = f'{feature_prefix}_yes'

    if selected_value == 'No internet service':
        if no_internet_col in df.columns:
            df.at[0, no_internet_col] = 1
    elif selected_value == 'Yes':
        if yes_col in df.columns:
            df.at[0,yes_col] = 1

def build_input_dataframe(
    tenure: int,
    monthly_charges: float,
    total_charges: float,
    gender: str,
    senior_citizen: str,
    partner: str,
    dependents: str,
    phone_service: str,
    multiple_lines: str,
    internet_service: str,
    contract: str,
    paperless_billing: str,
    payment_method: str,
    online_security: str,
    online_backup: str,
    device_protection: str,
    tech_support: str,
    streaming_tv: str,
    streaming_movies: str,

) -> pd.DataFrame:

    df = empty_input_df()

    df.at[0, "tenure"] = tenure
    df.at[0, "MonthlyCharges"] = monthly_charges
    df.at[0, "TotalCharges"] = total_charges

    set_binary(df, "gender_Male", gender == "Male")
    set_binary(df, "SeniorCitizen_1", senior_citizen == "Yes")
    set_binary(df, "Partner_Yes", partner == "Yes")
    set_binary(df, "Dependents_Yes", dependents == "Yes")
    set_binary(df, "PhoneService_Yes", phone_service == "Yes")
    set_binary(df, "PaperlessBilling_Yes", paperless_billing == "Yes")

    set_binary(df, "MultipleLines_No phone service", multiple_lines == "No phone service")
    set_binary(df, "MultipleLines_Yes", multiple_lines == "Yes")


    set_binary(df, "InternetService_Fiber optic", internet_service == "Fiber optic")
    set_binary(df, "InternetService_No", internet_service == "No")
    
    set_binary(df, "PaymentMethod_Credit card (automatic)", payment_method == "Credit card (automatic)")
    set_binary(df, "PaymentMethod_Electronic check", payment_method == "Electronic check")
    set_binary(df, "PaymentMethod_Mailed check", payment_method == "Mailed check")

    set_binary(df, "Contract_One year", contract == "One year")
    set_binary(df, "Contract_Two year", contract == "Two year")

    apply_three_state_service(df, "OnlineSecurity", online_security)
    apply_three_state_service(df, "OnlineBackup", online_backup)
    apply_three_state_service(df, "DeviceProtection", device_protection)
    apply_three_state_service(df, "TechSupport", tech_support)
    apply_three_state_service(df, "StreamingTV", streaming_tv)
    apply_three_state_service(df, "StreamingMovies", streaming_movies)

    return df

def recommend_action(probability: float) -> str:

    if probability >= 0.75:
        return "Alto risco: oferecer desconto e acionar contato humano do time comercial."

    if probability >= 0.40:
        return "Risco moderado: enviar campanha de retenção e acompanhar engajamento."

    return "Baixo risco: manter acompanhamento padrão."