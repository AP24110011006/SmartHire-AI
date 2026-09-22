"""
SmartHire AI - ATS Resume Scoring Engine
Calculates ATS compatibility score based on Contact Details,
Skills, Education, Standard Resume Sections, Length, and Formatting.
"""


class ATSScorer:
    """
    Calculates ATS compatibility score.
    """

    def __init__(self):
        self.max_score = 100

    # ======================================================
    # Contact Information (25 points)
    # ======================================================

    def contact_score(self, analysis, text):
        score = 0

        name = analysis.get("name")
        if name and name != "Not Found" and len(name.strip()) >= 2:
            score += 5

        email = analysis.get("email")
        if email and email != "Not Found" and "@" in email:
            score += 10

        phone = analysis.get("phone")
        if phone and phone != "Not Found":
            score += 10
        elif "linkedin.com" in text.lower() or "github.com" in text.lower():
            score += 5

        return min(25, score)

    # ======================================================
    # Skills (25 points)
    # ======================================================

    def skills_score(self, analysis):
        skills = analysis.get("skills", [])
        count = len(skills)

        if count >= 8:
            return 25
        if count >= 5:
            return 22
        if count >= 3:
            return 18
        if count >= 1:
            return 14

        return 5

    # ======================================================
    # Education (10 points)
    # ======================================================

    def education_score(self, analysis, text):
        education = analysis.get("education", [])

        if len(education) >= 2:
            return 10
        if len(education) == 1:
            return 8
        if any(k in text.lower() for k in ["education", "academic", "degree", "university", "college"]):
            return 6

        return 0

    # ======================================================
    # Resume Sections (20 points)
    # ======================================================

    def section_score(self, text):
        lower = text.lower()

        section_groups = [
            ["education", "academic", "qualifications", "academics"],
            ["skills", "technical skills", "core competencies", "technologies", "tools"],
            ["experience", "work history", "employment", "internship", "internships", "work experience"],
            ["projects", "portfolio", "key projects", "academic projects"],
            ["certification", "certifications", "licenses", "credentials", "achievements", "awards", "honors"],
            ["summary", "profile", "about me", "objective", "professional summary"]
        ]

        found_groups = 0
        for group in section_groups:
            if any(kw in lower for kw in group):
                found_groups += 1

        if found_groups >= 5:
            return 20
        if found_groups >= 4:
            return 18
        if found_groups >= 3:
            return 14
        if found_groups >= 2:
            return 10

        return 5

    # ======================================================
    # Resume Length (15 points)
    # ======================================================

    def length_score(self, text):
        words = len(text.split())

        if 250 <= words <= 900:
            return 15
        if 180 <= words < 250 or 900 < words <= 1200:
            return 12
        if 120 <= words < 180:
            return 8

        return 5

    # ======================================================
    # Formatting (10 points)
    # ======================================================

    def formatting_score(self, text):
        score = 0

        if len(text) > 350:
            score += 5

        if "\n" in text:
            score += 5

        return score

    # ======================================================
    # Calculate Total Score
    # ======================================================

    def calculate(self, text, analysis):
        breakdown = {
            "Contact Information": self.contact_score(analysis, text),
            "Skills": self.skills_score(analysis),
            "Education": self.education_score(analysis, text),
            "Resume Sections": self.section_score(text),
            "Resume Length": self.length_score(text),
            "Formatting": self.formatting_score(text),
        }

        total = sum(breakdown.values())
        total = min(total, self.max_score)
        total = max(0, total)

        return {
            "score": total,
            "breakdown": breakdown
        }


# ==========================================================
# Public Function
# ==========================================================

def calculate_ats_score(text, analysis):
    scorer = ATSScorer()
    return scorer.calculate(text, analysis)