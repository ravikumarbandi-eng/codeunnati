import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import sqlite3
import google.generativeai as genai

# ================= ADMIN CREDENTIALS =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Prescription Assistant",
    page_icon="🩺",
    layout="wide"
)

# ================= GEMINI CONFIG =================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ================= PDF SAFE TEXT =================
def clean_text_for_pdf(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# ================= DATABASE =================
def get_db_connection():
    return sqlite3.connect("prescriptions.db", check_same_thread=False)

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            disease TEXT,
            drug TEXT,
            dosage TEXT,
            precaution TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_record(record, gender):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prescriptions
        (time, name, age, gender, disease, drug, dosage, precaution)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["Time"],
        record["Patient Name"],
        record["Age"],
        gender,
        record["Disease"],
        record["Drug"],
        record["Dosage"],
        record["Precaution"]
    ))
    conn.commit()
    conn.close()

create_table()

# ================= LOAD MODEL =================
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

# ✅ REQUIRED INITIALIZATION (THIS WAS THE MISSING PART)
model, encoders = load_model()

# ================= SESSION =================
if "history" not in st.session_state:
    st.session_state.history = []
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ================= HEADER =================
st.markdown("<h1 style='text-align:center;'>🩺 Smart Prescription Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>AI-powered Medical Decision Support System</p>", unsafe_allow_html=True)
st.markdown("---")

# ================= ROLE SELECTION =================
role = st.radio("Select Role", ["User", "Bot", "Admin"], horizontal=True)
st.markdown("---")

# ================= PRECAUTIONS =================
precautions_data = {
   "Fever":{"dose":"2 times a day","duration":"3 days","visit":"If fever lasts more than 3 days"},
    "Cold":{"dose":"1–2 times a day","duration":"3–5 days","visit":"If symptoms worsen"},
    "Pain":{"dose":"2 times a day after food","duration":"5 days","visit":"If pain persists"},
    "Infection":{"dose":"3 times a day","duration":"5–7 days","visit":"After course completion"},
    "Allergy":{"dose":"Once daily","duration":"As prescribed","visit":"If reaction increases"},
    "Diabetes":{"dose":"Once daily","duration":"Long-term","visit":"Monthly sugar check"},
    "Hypertension":{"dose":"Once daily","duration":"Long-term","visit":"BP check every 2 weeks"},
    "Asthma":{"dose":"As required","duration":"As needed","visit":"If breathing worsens"},
    "Thyroid":{"dose":"Once daily","duration":"Long-term","visit":"Thyroid test every 3 months"},
    "Obesity":{"dose":"Once daily","duration":"As prescribed","visit":"Diet review monthly"},
    "Gastritis":{"dose":"Once daily","duration":"7 days","visit":"If pain persists"},
    "Acid Reflux":{"dose":"Once daily","duration":"7 days","visit":"If chest pain continues"},
    "Diarrhea":{"dose":"After each episode","duration":"2–3 days","visit":"If dehydration occurs"},
    "Constipation":{"dose":"Once daily","duration":"5 days","visit":"If no improvement"},
    "IBS":{"dose":"2 times a day","duration":"As prescribed","visit":"If pain continues"},
    "Heart Disease":{"dose":"Once daily","duration":"Long-term","visit":"Immediately if chest pain"},
    "High Cholesterol":{"dose":"Once daily","duration":"Long-term","visit":"Lipid test every 3 months"},
    "Migraine":{"dose":"At headache onset","duration":"As needed","visit":"If attacks increase"},
    "Anxiety":{"dose":"Once daily","duration":"As prescribed","visit":"Mental health follow-up"},
    "Depression":{"dose":"Once daily","duration":"Long-term","visit":"Regular psychiatric visit"},
    "Insomnia":{"dose":"Once daily at night","duration":"7–14 days","visit":"If sleep not improved"},
    "Epilepsy":{"dose":"As prescribed","duration":"Long-term","visit":"Neurology review"},
    "Bronchitis":{"dose":"2 times a day","duration":"5–7 days","visit":"If breathing worsens"},
    "Pneumonia":{"dose":"As prescribed","duration":"7–14 days","visit":"Hospital admission advised"},
    "Arthritis":{"dose":"2 times a day","duration":"As prescribed","visit":"If swelling increases"},
    "Back Pain":{"dose":"2 times a day","duration":"5 days","visit":"If pain radiates"},
    "Sinusitis":{"dose":"2 times a day","duration":"5–7 days","visit":"If facial pain persists"},
    "Conjunctivitis":{"dose":"2–3 times a day","duration":"5 days","visit":"If vision blurs"},
    "Eczema":{"dose":"Apply twice daily","duration":"7 days","visit":"If itching worsens"},
    "Acne":{"dose":"Apply once daily","duration":"2–4 weeks","visit":"If no improvement"},
    "UTI":{"dose":"2 times a day","duration":"5 days","visit":"If burning continues"},
    "Kidney Stones":{"dose":"Once daily","duration":"As prescribed","visit":"If severe pain"},
    "Anemia":{"dose":"Once daily","duration":"3 months","visit":"Hb check after 1 month"},
    "Vitamin D Deficiency":{"dose":"Once weekly","duration":"6–8 weeks","visit":"Test after course"},
    "Dehydration":{"dose":"After episodes","duration":"Until recovery","visit":"If dizziness occurs"}

# ================= USER MODULE =================
if role == "User":

    with st.form("patient_form"):
        st.subheader("👤 Patient Details")
        name = st.text_input("Patient Name")
        age = st.number_input("Age", 18, 100, 30)
        weight = st.number_input("Weight (kg)", 40, 120, 65)
        gender = st.radio("Gender", ["Male", "Female"], horizontal=True)

        st.subheader("🩺 Medical Details")
        disease = st.selectbox("Disease", encoders["disease"].classes_)
        severity = st.radio("Severity", ["Mild", "Moderate", "Severe"], horizontal=True)
        symptom_score = st.number_input("Symptom Score (1–10)", 1, 10, 5)

        submit = st.form_submit_button("💊 Generate Prescription")

    if submit:
        if name.strip() == "":
            st.error("Please enter patient name")
            st.stop()

        input_df = pd.DataFrame([[age, weight,
            encoders["gender"].transform([gender])[0],
            encoders["disease"].transform([disease])[0],
            encoders["severity"].transform([severity])[0],
            symptom_score]],
            columns=["age","weight","gender","disease","severity","symptom_score"]
        )

        drug = encoders["drug"].inverse_transform([model.predict(input_df)[0]])[0]

        dosage = 250 if severity == "Mild" else 500 if severity == "Moderate" else 650
        if weight > 80:
            dosage += 100

        info = precautions_data.get(disease)
        precaution = (
            f"Dose: {info['dose']} | Duration: {info['duration']} | Visit: {info['visit']}"
            if info else
            "Follow doctor advice | Visit hospital if symptoms persist"
        )

        record = {
            "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Patient Name": name,
            "Age": age,
            "Disease": disease,
            "Drug": drug,
            "Dosage": f"{dosage} mg",
            "Precaution": precaution
        }

        insert_record(record, gender)
        st.session_state.history.append(record)

        st.subheader("📋 Prescription Result")
        st.write(f"Patient: {name}")
        st.write(f"Drug: {drug}")
        st.write(f"Dosage: {dosage} mg")
        st.warning(precaution)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for k, v in record.items():
            pdf.cell(0, 8, clean_text_for_pdf(f"{k}: {v}"), ln=True)

        st.download_button(
            "⬇️ Download Prescription (PDF)",
            pdf.output(dest="S").encode("latin-1"),
            "prescription.pdf",
            "application/pdf"
        )

    if st.session_state.history:
        st.subheader("🕒 Your Session History")
        st.table(pd.DataFrame(st.session_state.history))

# ================= BOT MODULE =================
if role == "Bot":

    st.subheader("🤖 Medical Doubt Assistant")
    st.info("Educational answers only. Consult a doctor for treatment.")

    question = st.text_area("Ask your medical question")

    if st.button("Ask Bot") and question.strip():

        prompt = f"""
        You are an educational medical assistant.
        Do not diagnose.
        Do not prescribe medication.
        Answer clearly and simply.

        Question:
        {question}
        """

        response = gemini_model.generate_content(prompt)
        st.subheader("🤖 Bot Response")
        st.write(response.text)

# ================= ADMIN MODULE =================
if role == "Admin":

    if not st.session_state.admin_logged_in:
        st.subheader("🔐 Admin Login")
        u = st.text_input("Admin ID")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Admin login successful")
            else:
                st.error("Invalid credentials")

    if st.session_state.admin_logged_in:
        conn = get_db_connection()
        df = pd.read_sql("SELECT * FROM prescriptions ORDER BY id DESC", conn)
        conn.close()

        st.subheader("📋 Admin – User Records")
        st.table(df)

        st.download_button(
            "⬇️ Export Database (CSV)",
            df.to_csv(index=False),
            "prescriptions_database.csv",
            "text/csv"
        )

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.experimental_rerun()

# ================= FOOTER =================
st.caption("⚠️ Educational project only. Not for real medical use.")
