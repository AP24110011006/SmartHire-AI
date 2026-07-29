"""
===========================================================

SmartHire AI

Professional PDF Report Generator

===========================================================
"""

import os

from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle

)


class PDFReportGenerator:

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # =======================================================
    # Candidate Table
    # =======================================================

    def candidate_table(self, analysis):

        data = [

            ["Field", "Value"],

            ["Name", analysis.get("name", "-")],

            ["Email", analysis.get("email", "-")],

            ["Phone", analysis.get("phone", "-")]

        ]

        table = Table(data, colWidths=[150, 300])

        table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#2563EB")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

            ("ALIGN", (0,0), (-1,-1), "CENTER")

        ]))

        return table

    # =======================================================
    # Score Table
    # =======================================================

    def score_table(self, resume_score, ats_score):

        data = [

            ["Metric", "Score"],

            ["Resume Score", f"{resume_score['score']}/100"],

            ["ATS Score", f"{ats_score['score']}/100"]

        ]

        table = Table(data, colWidths=[220, 120])

        table.setStyle(TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#10B981")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.beige),

            ("ALIGN", (0,0), (-1,-1), "CENTER")

        ]))

        return table

    # =======================================================
    # Generate PDF
    # =======================================================

    def generate(

        self,

        output_path,

        category,

        confidence,

        analysis,

        resume_score,

        ats_score,

        recommendations,

        suggestions

    ):

        doc = SimpleDocTemplate(output_path)

        story = []

        title = Paragraph(

            "<b><font size=20 color='#2563EB'>SmartHire AI Resume Analysis Report</font></b>",

            self.styles["Title"]

        )

        story.append(title)

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                "<b>Candidate Information</b>",

                self.styles["Heading2"]

            )

        )

        story.append(self.candidate_table(analysis))

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                f"<b>Predicted Category:</b> {category}",

                self.styles["BodyText"]

            )

        )

        story.append(

            Paragraph(

                f"<b>Prediction Confidence:</b> {confidence:.2f}%",

                self.styles["BodyText"]

            )

        )

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                "<b>Scores</b>",

                self.styles["Heading2"]

            )

        )

        story.append(

            self.score_table(

                resume_score,

                ats_score

            )

        )

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                "<b>Detected Skills</b>",

                self.styles["Heading2"]

            )

        )

        for skill in analysis.get("skills", []):

            story.append(

                Paragraph(

                    f"• {skill}",

                    self.styles["BodyText"]

                )

            )

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                "<b>Recommended Jobs</b>",

                self.styles["Heading2"]

            )

        )

        for job in recommendations:

            story.append(

                Paragraph(

                    f"• {job['title']} (Match Score: {job['match_score']})",

                    self.styles["BodyText"]

                )

            )

        story.append(Spacer(1,20))

        story.append(

            Paragraph(

                "<b>AI Suggestions</b>",

                self.styles["Heading2"]

            )

        )

        for suggestion in suggestions:

            story.append(

                Paragraph(

                    f"• {suggestion}",

                    self.styles["BodyText"]

                )

            )

        doc.build(story)

        return output_path


# ===========================================================
# Public Function
# ===========================================================

def generate_pdf_report(

    output_path,

    category,

    confidence,

    analysis,

    resume_score,

    ats_score,

    recommendations,

    suggestions

):

    generator = PDFReportGenerator()

    return generator.generate(

        output_path,

        category,

        confidence,

        analysis,

        resume_score,

        ats_score,

        recommendations,

        suggestions

    )