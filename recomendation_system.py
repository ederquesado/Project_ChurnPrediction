import streamlit as st
import joblib
import pandas as pd
import Const  
import Helper  

st.set_page_config(page_title='Churn Predition', page_icon="📉", layout='centered')
st.title("📉 Churn Prediction")
st.write('Preencha os dados do cliente')


try:
    model = Helper.load_model()
except Exception as ex:
    st.error(f"Erro ao carregar o modelo")
    st.stop()


with st.form('churn_form'):
    st.subheader('Dados do cliente')

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner = st.selectbox("Partner", ["No", "Yes"])
        dependents = st.selectbox("Dependents", ["No", "Yes"])
        tenure = st.number_input("Tenure (meses)", min_value=0, max_value=1000, value=12, step=1)
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    with col2:

        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
        payment_method = st.selectbox(
            "Payment Method",
            [
                "Bank transfer (automatic)",
                "Credit card (automatic)",
                "Electronic check",
                "Mailed check",
            ],
        )
        monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=70.0, step=0.1)
        total_charges = st.number_input("Total Charges", min_value=0.0, value=850.0, step=0.1)



    st.subheader("Serviços adicionais")
    s1, s2, s3 = st.columns(3)

    with s1:
        online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])

    with s2:
        device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])

    with s3:
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])

    threshold = st.slider(
        "Threshold de decisão",
        min_value=0.10,
        max_value=0.90,
        value=Const.DEFAULT_THRESHOLD,
        step=0.05,
        help="Quanto menor o threshold, maior o recall e mais clientes serão marcados como risco de churn."
    )

    submitted = st.form_submit_button("Analisar cliente")

if submitted:

    try:
        input_df = Helper.build_input_dataframe(
            tenure=tenure,
            monthly_charges=monthly_charges,
            total_charges=total_charges,
            gender=gender,
            senior_citizen=senior_citizen,
            partner=partner,
            dependents=dependents,
            phone_service=phone_service,
            multiple_lines=multiple_lines,
            internet_service=internet_service,
            contract=contract,
            paperless_billing=paperless_billing,
            payment_method=payment_method,
            online_security=online_security,
            online_backup=online_backup,
            device_protection=device_protection,
            tech_support=tech_support,
            streaming_tv=streaming_tv,
            streaming_movies=streaming_movies,
        )
    except Exception as e:
        st.error(f"Erro ao executar a previsão: {e}")
        
    try: 
        probability = float(model.predict_proba(input_df)[:, 1][0])
        prediction = int(probability >= threshold)

        st.subheader("Resultado")

        if prediction == 1:
            st.error(f"Probabilidade de churn: {probability:.2%}")
            st.write("**Classificação:** Cliente com risco de churn")

        else:
            st.success(f"Probabilidade de churn: {probability:.2%}")
            st.write("**Classificação:** Cliente com baixo risco de churn")

        st.write(f"**Recomendação:** {Helper.recommend_action(probability)}")

        with st.expander("Ver linha enviada ao modelo"):
            st.dataframe(input_df)

    except Exception as e:
        st.error(f"Erro ao executar a previsão: {e}")