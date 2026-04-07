import streamlit as st
import Const  
import Helper  

# Form field configurations
FORM_CONFIG = {
    'personal_info': {
        'title': 'Dados do cliente',
        'fields': {
            'gender': {'label': 'Gender', 'options': ['Female', 'Male']},
            'senior_citizen': {'label': 'Senior Citizen', 'options': ['No', 'Yes']},
            'partner': {'label': 'Partner', 'options': ['No', 'Yes']},
            'dependents': {'label': 'Dependents', 'options': ['No', 'Yes']},
            'tenure': {'label': 'Tenure (meses)', 'type': 'number', 'min': 0, 'max': 1000, 'value': 12},
            'phone_service': {'label': 'Phone Service', 'options': ['No', 'Yes']},
            'multiple_lines': {'label': 'Multiple Lines', 'options': ['No', 'Yes', 'No phone service']},
        },
        'columns': 2
    },
    'service_info': {
        'title': 'Informações de Serviço',
        'fields': {
            'internet_service': {'label': 'Internet Service', 'options': ['DSL', 'Fiber optic', 'No']},
            'contract': {'label': 'Contract', 'options': ['Month-to-month', 'One year', 'Two year']},
            'paperless_billing': {'label': 'Paperless Billing', 'options': ['No', 'Yes']},
            'payment_method': {
                'label': 'Payment Method',
                'options': ['Bank transfer (automatic)', 'Credit card (automatic)', 'Electronic check', 'Mailed check']
            },
            'monthly_charges': {'label': 'Monthly Charges', 'type': 'number', 'min': 0.0, 'value': 70.0},
            'total_charges': {'label': 'Total Charges', 'type': 'number', 'min': 0.0, 'value': 850.0},
        },
        'columns': 2
    },
    'additional_services': {
        'title': 'Serviços adicionais',
        'fields': {
            'online_security': {'label': 'Online Security', 'options': ['No', 'Yes', 'No internet service']},
            'online_backup': {'label': 'Online Backup', 'options': ['No', 'Yes', 'No internet service']},
            'device_protection': {'label': 'Device Protection', 'options': ['No', 'Yes', 'No internet service']},
            'tech_support': {'label': 'Tech Support', 'options': ['No', 'Yes', 'No internet service']},
            'streaming_tv': {'label': 'Streaming TV', 'options': ['No', 'Yes', 'No internet service']},
            'streaming_movies': {'label': 'Streaming Movies', 'options': ['No', 'Yes', 'No internet service']},
        },
        'columns': 3
    }
}

def render_form_field(field_key: str, field_config: dict) -> any:
    """Render a single form field based on configuration."""
    label = field_config['label']
    
    if 'options' in field_config:
        return st.selectbox(label, field_config['options'], key=field_key)
    elif field_config.get('type') == 'number':
        return st.number_input(
            label,
            min_value=field_config.get('min', 0),
            max_value=field_config.get('max'),
            value=field_config.get('value', 0),
            step=0.1 if isinstance(field_config.get('value', 0), float) else 1,
            key=field_key
        )

def render_form_section(section_config: dict) -> dict:
    """Render a section of form fields and return their values."""
    st.subheader(section_config['title'])
    
    cols = st.columns(section_config['columns'])
    field_items = list(section_config['fields'].items())
    fields_per_col = (len(field_items) + section_config['columns'] - 1) // section_config['columns']
    
    values = {}
    for col_idx, col in enumerate(cols):
        with col:
            start_idx = col_idx * fields_per_col
            end_idx = min(start_idx + fields_per_col, len(field_items))
            
            for field_key, field_config in field_items[start_idx:end_idx]:
                values[field_key] = render_form_field(field_key, field_config)
    
    return values

def display_prediction_result(probability: float, threshold: float) -> None:
    """Display prediction results with color-coded output."""
    st.subheader("Resultado")
    
    is_high_risk = probability >= threshold
    status_text = "Cliente com risco de churn" if is_high_risk else "Cliente com baixo risco de churn"
    display_func = st.error if is_high_risk else st.success
    
    display_func(f"Probabilidade de churn: {probability:.2%}")
    st.write(f"**Classificação:** {status_text}")
    st.write(f"**Recomendação:** {Helper.recommend_action(probability)}")

# Initialize page
st.set_page_config(page_title='Churn Prediction', page_icon="📉", layout='centered')
st.title("📉 Churn Prediction")
st.write('Preencha os dados do cliente')

# Load model
try:
    model = Helper.load_model()
except Exception as ex:
    st.error("Erro ao carregar o modelo")
    st.stop()

# Build and render form
with st.form('churn_form'):
    form_data = {}
    
    # Render each form section
    for section_key in ['personal_info', 'service_info', 'additional_services']:
        section_values = render_form_section(FORM_CONFIG[section_key])
        form_data.update(section_values)
    
    # Threshold slider
    threshold = st.slider(
        "Threshold de decisão",
        min_value=0.10,
        max_value=0.90,
        value=Const.DEFAULT_THRESHOLD,
        step=0.05,
        help="Quanto menor o threshold, maior o recall e mais clientes serão marcados como risco de churn."
    )
    
    submitted = st.form_submit_button("Analisar cliente")

# Process form submission
if submitted:
    try:
        input_df = Helper.build_input_dataframe(form_data)
        probability = float(model.predict_proba(input_df)[:, 1][0])
        
        display_prediction_result(probability, threshold)
        
        with st.expander("Ver linha enviada ao modelo"):
            st.dataframe(input_df)
            
    except Exception as e:
        st.error(f"Erro ao processar predição: {e}")