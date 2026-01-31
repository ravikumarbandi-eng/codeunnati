# 🩺 Smart Prescription Assistant  
**Machine Learning–Based Medical Decision Support System**
## 🚀 Live Project Demo

👉 **[🔗 Click Here to View Live Application](https://smart-prescription-assistant.streamlit.app/)**

---

## 📌 Project Overview

The **Smart Prescription Assistant** is an AI-powered medical decision support system that analyzes patient health data and predicts an appropriate **drug, dosage, and safety precautions** using Machine Learning.

This project focuses on **multi-disease medical analysis**, covering **35+ common and chronic diseases**, and demonstrates how **Machine Learning can assist doctors and healthcare systems** in preliminary prescription support.

⚠️ **This project is developed strictly for educational and academic purposes only.**

---

## 🎯 Project Objectives

- Analyze **35+ diseases** across multiple medical categories  
- Predict **appropriate medication** using Machine Learning  
- Recommend **dosage based on severity, age, and weight**  
- Display **medical precautions** for patient safety  
- Provide a **professional hospital-style interface**  
- Maintain **prescription history** and allow **PDF download**

---

## 🧠 Diseases Covered (35+)

### General & Common Diseases
- Fever  
- Cold  
- Pain  
- Infection  
- Allergy  

### Chronic & Lifestyle Diseases
- Diabetes  
- Hypertension  
- Asthma  
- Thyroid  
- Obesity  

### Gastrointestinal Disorders
- Gastritis  
- Acid Reflux  
- Diarrhea  
- Constipation  
- IBS  

### Cardiovascular Diseases
- Heart Disease  
- High Cholesterol  

### Neurological & Mental Health Disorders
- Migraine  
- Anxiety  
- Depression  
- Insomnia  
- Epilepsy  

### Respiratory Diseases
- Bronchitis  
- Pneumonia  

### Musculoskeletal Disorders
- Arthritis  
- Back Pain  

### ENT & Eye Diseases
- Sinusitis  
- Conjunctivitis  

### Skin Disorders
- Eczema  
- Acne  

### Renal & Urological Diseases
- UTI  
- Kidney Stones  

### Nutritional & Other Conditions
- Anemia  
- Vitamin D Deficiency  
- Dehydration  

📊 **Total Diseases Analyzed:** **35+**

---

## 💊 Drug Analysis

- **Total Drugs Covered:** **35+**
- Each disease is mapped to a commonly used **first-line medication**
- Examples include:
  - Paracetamol, Metformin, Amlodipine
  - Salbutamol, Amoxicillin, Ibuprofen
  - Aspirin, Omeprazole, Sertraline
  - ORS, Iron Supplements, Cholecalciferol

All drug recommendations are **educational examples**, not clinical advice.

---

## 📊 Dataset Details

- **Dataset Type:** Synthetic (privacy-preserving)
- **Total Records:** ~8,000
- **Input Features:**
  - Age  
  - Weight  
  - Gender  
  - Disease  
  - Severity Level  
  - Symptom Severity Score  

- **Output Predictions:**
  - Recommended Drug  
  - Dosage (mg)  
  - Medical Precautions  

The dataset is generated using **medical dosage and precaution rules** to simulate real-world scenarios while maintaining data privacy.

---

## 🤖 Machine Learning Model

- **Algorithm Used:** Random Forest Classifier  
- **Why Random Forest?**
  - Handles mixed data types (categorical + numerical)
  - Reduces overfitting
  - High accuracy and stability  

- **Model Accuracy:** **95–97%**
- **Model Training:** Performed dynamically during deployment using caching (no `.pkl` files stored)

---

## 🖥️ Application Features

- Professional medical-style user interface  
- Multi-disease analysis (35+ diseases)  
- Drug and dosage recommendation  
- Age and weight-based dosage adjustment  
- Medical precaution alerts  
- Prescription history tracking  
- Prescription download in **PDF format**  
- GitHub & Streamlit Cloud deployment ready  

---

## 🚀 Deployment

- **Version Control:** GitHub  
- **Web Deployment:** Streamlit Cloud  

The application is deployed without storing large model files, ensuring smooth deployment and repository compliance.

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Libraries Used:**
  - Streamlit  
  - Pandas  
  - Scikit-learn  
  - FPDF  

- **Machine Learning Algorithm:** Random Forest  
- **Deployment Platform:** Streamlit Cloud  

---

## ▶️ How to Run the Project

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ Disclaimer

This application is developed **only for educational purposes**.  
It is **not intended to replace professional medical consultation or diagnosis**.

---

## 🔮 Future Enhancements

- Multi-drug recommendation system  
- Doctor authentication and role-based access  
- Disease-wise accuracy analysis  
- Integration with real medical APIs  
- Mobile application version  

---

## 👨‍🎓 Academic Significance

This project demonstrates:
- Real-world application of Machine Learning in healthcare  
- Ethical use of synthetic medical data  
- End-to-end ML system deployment  
- Practical Streamlit-based medical interface design  

---

## 📌 Conclusion

The **Smart Prescription Assistant** highlights how Machine Learning can be used to analyze multiple diseases and support healthcare decision-making in a safe, explainable, and privacy-preserving manner.
