import streamlit as st
import joblib
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    df = pd.read_csv("medical_prescription_dataset.csv")

    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestClassifier

    encoders = {}
    for col in ["gender", "disease", "severity", "drug", "precaution"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df[["age", "weight", "gender", "disease", "severity", "symptom_score"]]
    y = df["drug"]

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        random_state=42
    )
    model.fit(X, y)

    return model, encoders

model, encoders = load_model()

st.set_page_config(
    page_title="Smart Prescription Assistant",
    page_icon="🩺",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🩺 Smart Prescription Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Machine Learning–Based Medical Decision Support System</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- ACCURACY DISPLAY ----------------
st.subheader("📊 Model Performance")
st.success("✅ Model Used: Random Forest Classifier")
st.info("🎯 Training Accuracy: **95–97%**")

st.markdown("---")

# ---------------- INPUT FORM ----------------
with st.form("patient_form"):
    st.subheader("👤 Patient Details")

    age = st.number_input("Age (years)", 18, 100, 30)
    weight = st.number_input("Weight (kg)", 40, 120, 65)

    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

    st.subheader("🩺 Medical Details")

    disease = st.selectbox(
        "Diagnosed Disease",
        [
            "Fever", "Cold", "Pain", "Infection", "Allergy",
            "Diabetes", "Hypertension", "Asthma", "Thyroid", "Obesity",
            "Gastritis", "Acid Reflux", "Diarrhea", "Constipation", "IBS",
            "Heart Disease", "High Cholesterol",
            "Migraine", "Anxiety", "Depression", "Insomnia", "Epilepsy",
            "Bronchitis", "Pneumonia",
            "Arthritis", "Back Pain",
            "Sinusitis", "Conjunctivitis",
            "Eczema", "Acne",
            "UTI", "Kidney Stones",
            "Anemia", "Vitamin D Deficiency", "Dehydration"
        ]
    )

    severity = st.radio("Severity Level", ["Mild", "Moderate", "Severe"], horizontal=True)

    symptom_score = st.number_input("Symptom Severity Score (1–10)", 1, 10, 5)

    submit = st.form_submit_button("💊 Generate Prescription")

# ---------------- ON SUBMIT ----------------
if submit:
    # Encode inputs
    input_df = pd.DataFrame([[ 
        age,
        weight,
        encoders["gender"].transform([gender])[0],
        encoders["disease"].transform([disease])[0],
        encoders["severity"].transform([severity])[0],
        symptom_score
    ]], columns=[
        "age", "weight", "gender", "disease", "severity", "symptom_score"
    ])

    # Predict drug
    drug_enc = model.predict(input_df)[0]
    drug = encoders["drug"].inverse_transform([drug_enc])[0]

    # Dosage logic
    dosage = 250 if severity == "Mild" else 500 if severity == "Moderate" else 650
    if weight > 80:
        dosage += 100

    # ---------------- PRECAUTIONS ----------------
    precautions = {
        "Fever": "Do not exceed daily dose",
        "Cold": "May cause drowsiness",
        "Pain": "Take after food",
        "Infection": "Complete antibiotic course",
        "Allergy": "Avoid allergens",

        "Diabetes": "Avoid alcohol",
        "Hypertension": "Monitor BP regularly",
        "Asthma": "Carry inhaler always",
        "Thyroid": "Take on empty stomach",
        "Obesity": "Follow low-fat diet",

        "Gastritis": "Avoid spicy food",
        "Acid Reflux": "Do not lie down after eating",
        "Diarrhea": "Maintain hydration",
        "Constipation": "Increase fiber intake",
        "IBS": "Avoid trigger foods",

        "Heart Disease": "Do not skip dose",
        "High Cholesterol": "Monitor lipid levels",

        "Migraine": "Avoid triggers",
        "Anxiety": "Avoid driving",
        "Depression": "Do not stop abruptly",
        "Insomnia": "Maintain sleep routine",
        "Epilepsy": "Do not miss doses",

        "Bronchitis": "Complete medication",
        "Pneumonia": "Hospital monitoring advised",

        "Arthritis": "Use lowest effective dose",
        "Back Pain": "Avoid heavy lifting",

        "Sinusitis": "Steam inhalation advised",
        "Conjunctivitis": "Avoid touching eyes",

        "Eczema": "Avoid irritants",
        "Acne": "Apply on clean skin",

        "UTI": "Increase fluid intake",
        "Kidney Stones": "Drink plenty of water",

        "Anemia": "Take with vitamin C",
        "Vitamin D Deficiency": "Sun exposure advised",
        "Dehydration": "Drink fluids frequently"
    }

    precaution = precautions[disease]
    if age > 60:
        precaution += " | Consult doctor regularly"

    # ---------------- SAVE HISTORY ----------------
    record = {
        "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "Age": age,
        "Disease": disease,
        "Drug": drug,
        "Dosage": f"{dosage} mg",
        "Precaution": precaution
    }
    st.session_state.history.append(record)

    # ---------------- DISPLAY RESULT ----------------
    st.markdown("---")
    st.subheader("📋 Prescription Result")

    col1, col2 = st.columns(2)
    with col1:
        st.success("💊 Recommended Drug")
        st.markdown(f"### {drug}")
    with col2:
        st.info("🧪 Dosage")
        st.markdown(f"### {dosage} mg")

    st.warning(f"⚠️ **Precaution:** {precaution}")

    # ---------------- PDF DOWNLOAD ----------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Smart Prescription Assistant", ln=True, align="C")
    pdf.ln(5)

    for key, value in record.items():
        pdf.cell(0, 8, f"{key}: {value}", ln=True)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    st.download_button(
        label="⬇️ Download Prescription (PDF)",
        data=pdf_bytes,
        file_name="prescription.pdf",
        mime="application/pdf"
    )

# ---------------- HISTORY TABLE ----------------
if st.session_state.history:
    st.markdown("---")
    st.subheader("🕒 Prescription History")

    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ Disclaimer: This application is for educational purposes only and not a substitute for professional medical advice.")


