import joblib
import pandas as pd
import shap

# Load model and metadata
model = joblib.load("models/rf_ids_model.pkl")

with open("models/label_encoder_classes.txt", "r") as f:
    label_classes = f.read().splitlines()

with open("models/feature_names.txt", "r") as f:
    feature_names = f.read().splitlines()

# For prediction
def predict_attack(sample_dict):
    df = pd.DataFrame([sample_dict], columns=feature_names)
    return label_classes[model.predict(df)[0]]

# For SHAP explanation
explainer = shap.TreeExplainer(model)

def explain_prediction(sample_dict):
    df = pd.DataFrame([sample_dict], columns=feature_names)
    shap_values = explainer.shap_values(df)
    return shap_values, df
