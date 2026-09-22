"""
SmartHire AI - Comprehensive Resume Scoring Engine
Evaluates Contact Information, Skills, Education, Projects,
Certifications, and Resume Length.
"""


def calculate_resume_score(text, analysis):
    """
    Calculate an accurate, balanced resume score out of 100.
    """
    score = 0
    details = {}
    lower = text.lower()
    words = len(text.split())

    # ==========================================
    # 1. Contact Information (20 points)
    # ==========================================
    contact = 0

    if analysis.get("email") and analysis["email"] != "Not Found":
        contact += 10

    if analysis.get("phone") and analysis["phone"] != "Not Found":
        contact += 10

    # If phone/email is not explicitly extracted, credit LinkedIn/GitHub/Portfolio
    if contact < 20:
        if "linkedin.com" in lower or "github.com" in lower or "portfolio" in lower:
            contact = min(20, contact + 5)

    score += contact
    details["Contact Information"] = contact

    # ==========================================
    # 2. Skills (25 points)
    # ==========================================
    skills = analysis.get("skills", [])
    skill_count = len(skills)

    if skill_count >= 10:
        skills_score = 25
    elif skill_count >= 7:
        skills_score = 22
    elif skill_count >= 5:
        skills_score = 18
    elif skill_count >= 3:
        skills_score = 14
    elif skill_count >= 1:
        skills_score = 10
    else:
        skills_score = 5

    score += skills_score
    details["Skills"] = skills_score

    # ==========================================
    # 3. Education (20 points)
    # ==========================================
    edu = analysis.get("education", [])
    edu_count = len(edu)

    if edu_count >= 2:
        education_score = 20
    elif edu_count >= 1:
        education_score = 16
    elif any(k in lower for k in ["education", "academic", "qualifications", "degree"]):
        education_score = 12
    else:
        education_score = 5

    score += education_score
    details["Education"] = education_score

    # ==========================================
    # 4. Projects & Professional Work (20 points)
    # ==========================================
    project_keywords = [
        "project", "projects", "developed", "built", "designed",
        "implemented", "implementation", "engineered", "created",
        "architected", "deployed", "portfolio", "application",
        "applications", "system", "initiative", "work history", "case study"
    ]

    project_score = 0
    if any(word in lower for word in project_keywords):
        project_score = 20
    elif words >= 250:
        project_score = 10
    else:
        project_score = 5

    score += project_score
    details["Projects"] = project_score

    # ==========================================
    # 5. Certifications & Achievements (10 points)
    # ==========================================
    cert_keywords = [
        "certificate", "certification", "certifications", "certified",
        "coursera", "udemy", "infosys", "nptel", "aws", "azure",
        "google cloud", "gcp", "cisco", "oracle", "hackerrank",
        "leetcode", "license", "licensed", "credential", "workshop",
        "bootcamp", "training", "achievement", "achievements", "award",
        "awards", "honors", "fellowship"
    ]

    cert_score = 0
    if any(word in lower for word in cert_keywords):
        cert_score = 10
    elif words >= 300:
        cert_score = 5
    else:
        cert_score = 2

    score += cert_score
    details["Certifications"] = cert_score

    # ==========================================
    # 6. Resume Length (5 points)
    # ==========================================
    if 250 <= words <= 1000:
        length_score = 5
    elif 150 <= words < 250 or words > 1000:
        length_score = 3
    else:
        length_score = 2

    score += length_score
    details["Resume Length"] = length_score

    score = min(100, max(0, score))

    return {
        "score": score,
        "details": details
    }