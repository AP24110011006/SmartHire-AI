"""
===========================================================
SmartHire AI
Career Insights Engine
===========================================================
"""


class CareerInsights:

    def __init__(self):

        self.salary_ranges = {

            "ENGINEERING": (600000, 1200000),
            "INFORMATION-TECHNOLOGY": (500000, 1100000),
            "DATA SCIENCE": (700000, 1400000),
            "FINANCE": (400000, 900000),
            "HR": (300000, 700000)

        }

    # -------------------------------------------------------
    # Salary Band
    # -------------------------------------------------------

    def predict_salary_band(
        self,
        category,
        resume_score,
        ats_score,
        experience
    ):

        minimum, maximum = self.salary_ranges.get(
            category,
            (400000, 800000)
        )

        bonus = 0

        if resume_score >= 90:
            bonus += 200000

        elif resume_score >= 80:
            bonus += 100000

        if ats_score >= 90:
            bonus += 150000

        elif ats_score >= 80:
            bonus += 75000

        if experience >= 2:
            bonus += 200000

        minimum += bonus
        maximum += bonus

        return f"₹{minimum//100000} LPA - ₹{maximum//100000} LPA"

    # -------------------------------------------------------
    # Career Level
    # -------------------------------------------------------

    def predict_career_level(self, experience):

        if experience == 0:
            return "Intern / Fresher"

        elif experience <= 2:
            return "Entry Level"

        elif experience <= 5:
            return "Mid Level"

        else:
            return "Senior Level"

    # -------------------------------------------------------
    # Interview Readiness
    # -------------------------------------------------------

    def calculate_interview_readiness(
        self,
        resume_score,
        ats_score,
        project_count,
        skill_count
    ):

        readiness = (

            resume_score * 0.40 +

            ats_score * 0.30 +

            min(project_count * 5, 15) +

            min(skill_count * 2, 15)

        )

        return round(min(readiness, 100), 2)

    # -------------------------------------------------------
    # Skills To Learn
    # -------------------------------------------------------

    def recommend_skills(
        self,
        missing_skills
    ):

        if len(missing_skills) == 0:

            return [

                "System Design",

                "Leadership",

                "Communication"

            ]

        return missing_skills[:3]

    # -------------------------------------------------------
    # Master Function
    # -------------------------------------------------------

    def generate(
        self,
        category,
        analysis,
        resume_score,
        ats_score,
        recommendations
    ):

        experience = analysis.get(
            "experience_years",
            0
        )

        skills = analysis.get(
            "skills",
            []
        )

        projects = analysis.get(
            "projects",
            []
        )

        missing = []

        if recommendations:

            missing = recommendations[0].get(
                "missing_skills",
                []
            )

        return {

            "salary_band":

                self.predict_salary_band(

                    category,

                    resume_score["score"],

                    ats_score["score"],

                    experience

                ),

            "career_level":

                self.predict_career_level(

                    experience

                ),

            "interview_readiness":

                self.calculate_interview_readiness(

                    resume_score["score"],

                    ats_score["score"],

                    len(projects),

                    len(skills)

                ),

            "skills_to_learn":

                self.recommend_skills(

                    missing

                )

        }


career_engine = CareerInsights()

def generate_career_insights(
    category,
    analysis,
    resume_score,
    ats_score,
    recommendations
):

    return career_engine.generate(
        category,
        analysis,
        resume_score,
        ats_score,
        recommendations
    )