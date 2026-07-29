import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from src.data.load_data import load_resume_data
from src.data.preprocess import clean_text


def main():
    print("=" * 60)
    print("SMART HIRE - RESUME CLASSIFICATION MODEL")
    print("=" * 60)

    # Load dataset
    df = load_resume_data()

    # Clean text
    df["Clean_Resume"] = df["Resume_str"].apply(clean_text)

    X = df["Clean_Resume"]
    y = df["Category"]

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    X_vectorized = vectorizer.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    print(f"\nTraining Samples : {X_train.shape[0]}")
    print(f"Testing Samples  : {X_test.shape[0]}")

    # Train model
    model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    print("\nTraining Model...")
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print("\nAccuracy:")
    print(f"{accuracy*100:.2f}%")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))

    # Save models
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    joblib.dump(model, models_dir / "resume_classifier.pkl")
    joblib.dump(vectorizer, models_dir / "tfidf_vectorizer.pkl")
    joblib.dump(label_encoder, models_dir / "label_encoder.pkl")

    print("\nModels saved successfully!")

    print("\nSaved Files:")
    print("resume_classifier.pkl")
    print("tfidf_vectorizer.pkl")
    print("label_encoder.pkl")


if __name__ == "__main__":
    main()