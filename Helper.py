import joblib
import pandas as pd
import Const

def load_model():
    return joblib.load(Const.MODEL_PATH)

def empty_input_df() -> pd.DataFrame:
    return pd.DataFrame([[0] * len(Const.MODEL_COLUMNS)], columns=Const.MODEL_COLUMNS)

def _set_feature_value(df: pd.DataFrame, column_name: str, value: int) -> None:
    """Set a feature value in the dataframe if column exists."""
    if column_name in df.columns:
        df.at[0, column_name] = value

def _encode_binary_feature(df: pd.DataFrame, feature_name: str, user_value: str) -> None:
    """Encode a binary feature (e.g., Yes/No)."""
    column_name, target_value = Const.BINARY_FEATURES[feature_name]
    _set_feature_value(df, column_name, int(user_value == target_value))

def _encode_multi_state_feature(df: pd.DataFrame, feature_name: str, user_value: str) -> None:
    """Encode a multi-state feature (e.g., multiple options with binary encoding)."""
    feature_prefix, active_values = Const.MULTI_STATE_FEATURES[feature_name]
    
    for active_value in active_values:
        column_name = f'{feature_prefix}_{active_value}'
        _set_feature_value(df, column_name, int(user_value == active_value))

def build_input_dataframe(input_data: dict) -> pd.DataFrame:
    """Build model input dataframe from user input dictionary.
    
    Args:
        input_data: Dictionary with feature names as keys and user-selected values.
        
    Returns:
        DataFrame with properly encoded features for model prediction.
    """
    df = empty_input_df()
    
    # Set numeric features
    for input_key, df_column in Const.NUMERIC_TO_DF_MAPPING.items():
        if input_key in input_data:
            df.at[0, df_column] = input_data[input_key]
    
    # Encode binary features
    for feature_name in Const.BINARY_FEATURES.keys():
        if feature_name in input_data:
            _encode_binary_feature(df, feature_name, input_data[feature_name])
    
    # Encode multi-state features
    for feature_name in Const.MULTI_STATE_FEATURES.keys():
        if feature_name in input_data:
            _encode_multi_state_feature(df, feature_name, input_data[feature_name])
    
    return df

def recommend_action(probability: float) -> str:

    if probability >= 0.75:
        return "Alto risco: oferecer desconto e acionar contato humano do time comercial."

    if probability >= 0.40:
        return "Risco moderado: enviar campanha de retenção e acompanhar engajamento."

    return "Baixo risco: manter acompanhamento padrão."