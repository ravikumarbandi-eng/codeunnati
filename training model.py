import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("medical_prescription_dataset.csv")

# Encode categorical columns
label_encoders = {}
categorical_cols = ["gender", "disease", "severity", "drug", "precaution"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and target
X = df[["age", "weight", "gender", "disease", "severity", "symptom_score"]]
y = df["drug"]   # predicting drug (main target)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest Model (BEST)
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy * 100)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(model, "prescription_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("Model and encoders saved successfully!")
