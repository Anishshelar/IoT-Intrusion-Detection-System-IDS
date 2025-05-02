import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess(path):
    df = pd.read_csv(path)

    # Encode categorical features
    for col in ['protocol', 'service', 'flag']:
        df[col] = df[col].astype('category').cat.codes

    # Encode target
    label_encoder = LabelEncoder()
    df['label'] = label_encoder.fit_transform(df['label'])

    # Save label classes
    with open("models/label_encoder_classes.txt", "w") as f:
        f.write("\n".join(label_encoder.classes_))

    # Save feature order
    features = df.drop("label", axis=1).columns.tolist()
    with open("models/feature_names.txt", "w") as f:
        f.write("\n".join(features))

    X = df.drop("label", axis=1)
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    return X_train, X_test, y_train, y_test, label_encoder
