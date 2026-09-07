import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)
import joblib

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename

from src.parsing.resume_parser import extract_text
from src.analysis.resume_analyzer import analyze_resume
from src.scoring.resume_score import calculate_resume_score
from src.scoring.ats_score import calculate_ats_score
from src.recommendation.recommend_jobs import recommend_jobs
from src.suggestions.suggestions import generate_resume_suggestions
from src.reports.pdf_report import generate_pdf_report
from src.career.career_insights import generate_career_insights


# ==========================================================
# Flask App
# ==========================================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
MODEL_FOLDER = os.path.join(BASE_DIR, "..", "models")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "doc",
    "txt"
}


# ==========================================================
# Load ML Models
# ==========================================================

classifier = joblib.load(
    os.path.join(MODEL_FOLDER, "resume_classifier.pkl")
)

vectorizer = joblib.load(
    os.path.join(MODEL_FOLDER, "tfidf_vectorizer.pkl")
)

label_encoder = joblib.load(
    os.path.join(MODEL_FOLDER, "label_encoder.pkl")
)

# ==========================================================
# Helper Functions
# ==========================================================

def allowed_file(filename):

    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def predict_category(text):

    vector = vectorizer.transform([text])

    prediction = classifier.predict(vector)[0]

    probabilities = classifier.predict_proba(vector)[0]

    confidence = min(100.0, max(0.0, float(max(probabilities) * 100)))

    category = label_encoder.inverse_transform([prediction])[0]

    return category, confidence


def delete_file(filepath):

    try:

        if os.path.exists(filepath):
            os.remove(filepath)

    except Exception:
        pass
# ==========================================================
# Home Route
# ==========================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# Resume Prediction API
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "resume" not in request.files:

        return jsonify({

            "status": "error",

            "message": "No resume uploaded."

        }), 400

    file = request.files["resume"]

    if file.filename == "":

        return jsonify({

            "status": "error",

            "message": "Please select a resume."

        }), 400

    if not allowed_file(file.filename):

        return jsonify({

            "status": "error",

            "message": "Unsupported file type."

        }), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )

    file.save(filepath)

    try:

        # ==========================================
        # Resume Parsing
        # ==========================================

        resume_text = extract_text(filepath)

        if not resume_text.strip():

            delete_file(filepath)

            return jsonify({

                "status": "error",

                "message": "Unable to extract text from resume."

            }), 400

        # ==========================================
        # Resume Analysis
        # ==========================================

        analysis = analyze_resume(resume_text)

        # ==========================================
        # Category Prediction
        # ==========================================

        category, confidence = predict_category(resume_text)

        # ==========================================
        # Resume Score
        # ==========================================

        resume_score = calculate_resume_score(

            resume_text,

            analysis

        )

        # ==========================================
        # ATS Score
        # ==========================================

        ats_score = calculate_ats_score(

            resume_text,

            analysis

        )

        # ==========================================
        # Job Recommendation
        # ==========================================

        recommendations = recommend_jobs(

            category,

            analysis,

            resume_score,

            ats_score

        )
        career_insights = generate_career_insights(
            category,

            analysis,

            resume_score,

            ats_score,

            recommendations

       )



        # ==========================================
        # AI Suggestions
        # ==========================================

        suggestions = generate_resume_suggestions(

            resume_text,

            analysis,

            resume_score,

            ats_score

        )
        # ==========================================
        # Generate PDF Report
        # ==========================================

        report_filename = (
            os.path.splitext(filename)[0] + "_report.pdf"
        )

        report_path = os.path.join(

            app.config["REPORT_FOLDER"],

            report_filename

        )

        generate_pdf_report(

            output_path=report_path,

            category=category,

            confidence=confidence,

            analysis=analysis,

            resume_score=resume_score,

            ats_score=ats_score,

            recommendations=recommendations,

            suggestions=suggestions

        )  
        # ==========================================
        # Prepare Response
        # ==========================================

        response = {

            "status": "success",

            "category": category,

            "confidence": round(confidence, 2),

            "analysis": analysis,

            "resume_score": resume_score,

            "ats_score": ats_score,

            "recommended_jobs": recommendations,

            "career_insights": career_insights,

            "suggestions": suggestions,

            "report_file": report_filename

        }

        delete_file(filepath)

        return jsonify(response)

    except Exception as e:

        delete_file(filepath)

        return jsonify({

            "status": "error",

            "message": str(e)

        }), 500

# ==========================================================
# Download PDF Report
# ==========================================================

@app.route("/download-report/<filename>", methods=["GET"])
def download_report(filename):

    filename = secure_filename(filename)

    report_path = os.path.join(
        app.config["REPORT_FOLDER"],
        filename
    )

    print("=" * 60)
    print("Requested filename :", filename)
    print("Looking for file   :", report_path)
    print("Exists             :", os.path.exists(report_path))
    print("=" * 60)

    if not os.path.exists(report_path):

        return jsonify({
            "status": "error",
            "message": "Report not found."
        }), 404

    return send_file(
        report_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf"
    )


# ==========================================================
# Health Check
# ==========================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "status": "success",

        "message": "SmartHire AI Backend is running."

    })


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(

        host="0.0.0.0",

        port=port,

        debug=False

    )