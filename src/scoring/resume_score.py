import re


def calculate_resume_score(text, analysis):

    score = 0

    details = {}

    # ==========================================
    # Contact Information (20)
    # ==========================================

    contact = 0

    if analysis["email"] != "Not Found":
        contact += 10

    if analysis["phone"] != "Not Found":
        contact += 10

    score += contact

    details["Contact Information"] = contact

    # ==========================================
    # Skills (25)
    # ==========================================

    skill_count = len(analysis["skills"])

    if skill_count >= 10:
        skills_score = 25

    elif skill_count >= 7:
        skills_score = 20

    elif skill_count >= 5:
        skills_score = 15

    elif skill_count >= 3:
        skills_score = 10

    else:
        skills_score = 5

    score += skills_score

    details["Skills"] = skills_score

    # ==========================================
    # Education (20)
    # ==========================================

    education_score = 0

    if len(analysis["education"]) >= 4:
        education_score = 20

    elif len(analysis["education"]) >= 2:
        education_score = 15

    elif len(analysis["education"]) >= 1:
        education_score = 10

    score += education_score

    details["Education"] = education_score

    # ==========================================
    # Projects (20)
    # ==========================================

    project_keywords = [

        "project",

        "developed",

        "built",

        "designed",

        "implementation"

    ]

    project_score = 0

    lower = text.lower()

    for word in project_keywords:

        if word in lower:
            project_score = 20
            break

    score += project_score

    details["Projects"] = project_score

    # ==========================================
    # Certifications (10)
    # ==========================================

    cert_keywords = [

        "certificate",

        "certification",

        "coursera",

        "udemy",

        "infosys",

        "nptel"

    ]

    cert_score = 0

    for word in cert_keywords:

        if word in lower:
            cert_score = 10
            break

    score += cert_score

    details["Certifications"] = cert_score

    # ==========================================
    # Resume Length (5)
    # ==========================================

    words = len(text.split())

    if 300 <= words <= 900:
        length_score = 5

    else:
        length_score = 2

    score += length_score

    details["Resume Length"] = length_score

    score = min(100, max(0, score))

    return {

        "score": score,

        "details": details

    }