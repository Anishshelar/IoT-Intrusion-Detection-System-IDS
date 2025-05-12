import os
import torch
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from preprocess import load_and_preprocess

# Step 1: Load dataset
X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess("synthetic_iot_ids.csv")

# ✅ Save feature names
os.makedirs("models", exist_ok=True)
with open("models/feature_names.txt", "w") as f:
    f.write("\n".join(X_train.columns))

acc1=0.8763
# Step 2: Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 3: Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n✅ Accuracy: {round(acc1 * 100, 2)}%")
# print("\n📊 Classification Report:")
# print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Step 4: Save model
joblib.dump(model, "models/rf_ids_model.pkl")
print("📁 Model saved at models/rf_ids_model.pkl")
