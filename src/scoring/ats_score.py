"""
===========================================================

SmartHire AI

ATS Resume Scoring Engine

===========================================================
"""


import re


class ATSScorer:
    """
    Calculates ATS compatibility score.
    """

    def __init__(self):

        self.max_score = 100

    # ======================================================
    # Contact Information
    # ======================================================

    def contact_score(self, analysis):

        score = 0

        if analysis.get("name"):
            score += 5

        if analysis.get("email"):
            score += 10

        if analysis.get("phone"):
            score += 10

        return score

    # ======================================================
    # Skills
    # ======================================================

    def skills_score(self, analysis):

        skills = analysis.get("skills", [])

        if len(skills) >= 12:
            return 25

        if len(skills) >= 8:
            return 22

        if len(skills) >= 5:
            return 18

        if len(skills) >= 3:
            return 12

        if len(skills) >= 1:
            return 6

        return 0

    # ======================================================
    # Education
    # ======================================================

    def education_score(self, analysis):

        education = analysis.get("education", [])

        if len(education) >= 2:
            return 10

        if len(education) == 1:
            return 7

        return 0

    # ======================================================
    # Resume Sections
    # ======================================================

    def section_score(self, text):

        score = 0

        text = text.lower()

        keywords = [

            "education",

            "skills",

            "projects",

            "experience",

            "certification",

            "internship",

            "summary"

        ]

        for keyword in keywords:

            if keyword in text:
                score += 3

        return min(score, 20)

    # ======================================================
    # Resume Length
    # ======================================================

    def length_score(self, text):

        words = len(text.split())

        if 350 <= words <= 800:
            return 15

        if 250 <= words < 350:
            return 12

        if 150 <= words < 250:
            return 8

        if words > 800:
            return 10

        return 5

    # ======================================================
    # Formatting
    # ======================================================

    def formatting_score(self, text):

        score = 0

        if len(text) > 500:
            score += 5

        if "\n" in text:
            score += 5

        return score

    # ======================================================
    # Calculate Total Score
    # ======================================================

    def calculate(self, text, analysis):

        breakdown = {

            "Contact Information":
                self.contact_score(analysis),

            "Skills":
                self.skills_score(analysis),

            "Education":
                self.education_score(analysis),

            "Resume Sections":
                self.section_score(text),

            "Resume Length":
                self.length_score(text),

            "Formatting":
                self.formatting_score(text)

        }

        total = sum(breakdown.values())

        total = min(total, self.max_score)

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