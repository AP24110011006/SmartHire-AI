"""
===========================================================
SmartHire AI
Enhanced Job Recommendation Engine
===========================================================
"""


class JobRecommender:

    def __init__(self):

        self.job_database = {

            "ENGINEERING": [

                {
                    "title": "Software Engineer",
                    "skills": [
                        "python",
                        "java",
                        "c++",
                        "algorithms",
                        "data structures"
                    ]
                },

                {
                    "title": "Backend Developer",
                    "skills": [
                        "python",
                        "flask",
                        "django",
                        "api",
                        "sql"
                    ]
                },

                {
                    "title": "Machine Learning Engineer",
                    "skills": [
                        "python",
                        "machine learning",
                        "tensorflow",
                        "pandas",
                        "numpy"
                    ]
                },

                {
                    "title": "AI Engineer",
                    "skills": [
                        "artificial intelligence",
                        "deep learning",
                        "python",
                        "tensorflow",
                        "pytorch"
                    ]
                }

            ],

            "INFORMATION-TECHNOLOGY": [

                {
                    "title": "Cloud Engineer",
                    "skills": [
                        "aws",
                        "azure",
                        "docker",
                        "kubernetes"
                    ]
                },

                {
                    "title": "DevOps Engineer",
                    "skills": [
                        "docker",
                        "linux",
                        "jenkins",
                        "git"
                    ]
                },

                {
                    "title": "Cyber Security Analyst",
                    "skills": [
                        "network security",
                        "linux",
                        "penetration testing"
                    ]
                }

            ],

            "DATA SCIENCE": [

                {
                    "title": "Data Scientist",
                    "skills": [
                        "python",
                        "pandas",
                        "numpy",
                        "sql",
                        "statistics"
                    ]
                },

                {
                    "title": "Data Analyst",
                    "skills": [
                        "excel",
                        "power bi",
                        "sql",
                        "python"
                    ]
                }

            ],

            "FINANCE": [

                {
                    "title": "Financial Analyst",
                    "skills": [
                        "excel",
                        "finance",
                        "accounting"
                    ]
                },

                {
                    "title": "Investment Analyst",
                    "skills": [
                        "finance",
                        "valuation",
                        "market research"
                    ]
                }

            ],

            "HR": [

                {
                    "title": "HR Executive",
                    "skills": [
                        "communication",
                        "recruitment",
                        "management"
                    ]
                },

                {
                    "title": "Talent Acquisition Specialist",
                    "skills": [
                        "recruitment",
                        "interviewing"
                    ]
                }

            ]
        }

    # =======================================================
    # Helper Functions
    # =======================================================

    def get_growth(self, score):

        if score >= 90:
            return "Excellent"

        elif score >= 75:
            return "High"

        elif score >= 60:
            return "Moderate"

        return "Needs Improvement"

    def get_salary(self, score):

        if score >= 90:
            return "₹12–18 LPA"

        elif score >= 80:
            return "₹8–12 LPA"

        elif score >= 70:
            return "₹6–8 LPA"

        return "₹3–6 LPA"

    def get_recommendation(self, missing_skills):

        if missing_skills:

            return (
                "Improve your profile by learning "
                + ", ".join(missing_skills[:3])
                + "."
            )

        return (
            "Excellent profile. Focus on interview preparation."
        )

    # =======================================================
    # Main Recommendation Engine
    # =======================================================

    def recommend(
        self,
        category,
        analysis,
        resume_score,
        ats_score
    ):

        jobs = self.job_database.get(category, [])

        recommendations = []

        resume_skills = [

            skill.lower()

            for skill in analysis.get("skills", [])

        ]

        for job in jobs:

            job_skills = [

                skill.lower()

                for skill in job["skills"]

            ]

            matched_skills = [

                skill

                for skill in job_skills

                if skill in resume_skills

            ]

            missing_skills = [

                skill

                for skill in job_skills

                if skill not in resume_skills

            ]
            match_score = (
                len(matched_skills) * 15 +
                resume_score["score"] * 0.35 +
                ats_score["score"] * 0.25
            )

            match_score = min(round(match_score, 2), 100)

            recommendations.append({

                "title": job["title"],

                "match_score": match_score,

                "matched_skills": matched_skills,

                "missing_skills": missing_skills,

                "salary_band": self.get_salary(match_score),

                "career_growth": self.get_growth(match_score),

                "recommendation": self.get_recommendation(
                    missing_skills
                )

            })

        recommendations.sort(
            key=lambda job: job["match_score"],
            reverse=True
        )

        return recommendations[:5]


# ==========================================================
# Public Function
# ==========================================================

def recommend_jobs(
    category,
    analysis,
    resume_score,
    ats_score
):

    recommender = JobRecommender()

    return recommender.recommend(
        category,
        analysis,
        resume_score,
        ats_score
    )