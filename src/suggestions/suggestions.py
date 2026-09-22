"""
===========================================================

SmartHire AI

Resume Suggestion Engine

===========================================================
"""


class ResumeSuggestionEngine:

    def __init__(self):
        pass

    # ======================================================
    # Contact Suggestions
    # ======================================================

    def contact_suggestions(self, analysis):

        suggestions = []

        if not analysis.get("name") or analysis.get("name") == "Not Found":
            suggestions.append(
                "Add your full name at the top of the resume."
            )

        if not analysis.get("email") or analysis.get("email") == "Not Found":
            suggestions.append(
                "Include a professional email address."
            )

        if not analysis.get("phone") or analysis.get("phone") == "Not Found":
            suggestions.append(
                "Add your contact number."
            )

        return suggestions

    # ======================================================
    # Skills Suggestions
    # ======================================================

    def skills_suggestions(self, analysis):

        suggestions = []

        skills = analysis.get("skills", [])

        if len(skills) < 5:

            suggestions.append(
                "Include more technical skills related to your target job."
            )

        if len(skills) < 10:

            suggestions.append(
                "Adding frameworks, tools, and technologies can improve ATS performance."
            )

        return suggestions

    # ======================================================
    # Education Suggestions
    # ======================================================

    def education_suggestions(self, analysis):

        suggestions = []

        if len(analysis.get("education", [])) == 0:

            suggestions.append(
                "Mention your educational qualifications."
            )

        return suggestions

    # ======================================================
    # Resume Length
    # ======================================================

    def length_suggestions(self, text):

        suggestions = []

        words = len(text.split())

        if words < 250:

            suggestions.append(
                "Your resume is short. Add projects, internships, achievements, and certifications."
            )

        elif words > 900:

            suggestions.append(
                "Your resume is lengthy. Remove less relevant information to improve readability."
            )

        return suggestions

    # ======================================================
    # Resume Score Suggestions
    # ======================================================

    def resume_score_suggestions(self, resume_score):

        suggestions = []

        score = resume_score["score"]

        if score < 60:

            suggestions.append(
                "Resume quality is below average. Improve formatting and add stronger technical content."
            )

        elif score < 80:

            suggestions.append(
                "Your resume is good, but adding measurable achievements and certifications will improve it."
            )

        return suggestions

    # ======================================================
    # ATS Suggestions
    # ======================================================

    def ats_suggestions(self, ats_score):

        suggestions = []

        score = ats_score["score"]

        if score < 70:

            suggestions.append(
                "Improve ATS compatibility by using standard section headings like Skills, Education, Experience, and Projects."
            )

        elif score < 85:

            suggestions.append(
                "Add more relevant keywords from your target job description to increase ATS matching."
            )

        return suggestions

    # ======================================================
    # Overall Suggestions
    # ======================================================

    def generate(
        self,
        text,
        analysis,
        resume_score,
        ats_score
    ):

        suggestions = []

        suggestions.extend(
            self.contact_suggestions(analysis)
        )

        suggestions.extend(
            self.skills_suggestions(analysis)
        )

        suggestions.extend(
            self.education_suggestions(analysis)
        )

        suggestions.extend(
            self.length_suggestions(text)
        )

        suggestions.extend(
            self.resume_score_suggestions(resume_score)
        )

        suggestions.extend(
            self.ats_suggestions(ats_score)
        )

        if len(suggestions) == 0:

            suggestions.append(
                "Excellent! Your resume is well optimized. Only minor improvements are recommended."
            )

        return suggestions


# ==========================================================
# Public Function
# ==========================================================

def generate_resume_suggestions(
    text,
    analysis,
    resume_score,
    ats_score
):

    engine = ResumeSuggestionEngine()

    return engine.generate(
        text,
        analysis,
        resume_score,
        ats_score
    )