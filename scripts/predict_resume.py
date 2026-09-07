import sys
from pathlib import Path

# =====================================================
# Add project root to Python path
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import joblib

from src.data.preprocess import clean_text


# -----------------------------------------------------
# Load saved model, vectorizer, and label encoder
# -----------------------------------------------------
MODEL_PATH = PROJECT_ROOT / "models" / "resume_classifier.pkl"
VECTORIZER_PATH = PROJECT_ROOT / "models" / "tfidf_vectorizer.pkl"
LABEL_ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoder.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)


def predict_resume(text):
    """
    Predict resume category from resume text.
    """
    cleaned_text = clean_text(text)

    vector = vectorizer.transform([cleaned_text])

    prediction = model.predict(vector)[0]

    category = label_encoder.inverse_transform([prediction])[0]

    probabilities = model.predict_proba(vector)[0]

    confidence = min(100.0, max(0.0, float(max(probabilities) * 100)))

    return category, confidence


def main():
    print("=" * 60)
    print("SMART HIRE - RESUME CATEGORY PREDICTION")
    print("=" * 60)

    print("\nPaste the resume text below.")
    print("Press ENTER twice when finished.\n")

    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    resume_text = "\n".join(lines)

    if not resume_text.strip():
        print("\nNo resume text entered.")
        return

    category, confidence = predict_resume(resume_text)

    print("\n" + "=" * 60)
    print("PREDICTION RESULT")
    print("=" * 60)

    print(f"Predicted Category : {category}")
    print(f"Confidence Score   : {confidence:.2f}%")

    print("=" * 60)


if __name__ == "__main__":
    main()