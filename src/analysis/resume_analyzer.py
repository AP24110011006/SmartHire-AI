import re

from src.utils.skills import SKILLS


def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_phone(text):

    match = re.search(
        r'(\+91[\-\s]?)?[6-9]\d{9}',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_name(text):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 35:

            if "resume" not in line.lower():

                return line

    return "Not Found"


def extract_skills(text):

    found = []

    lower_text = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower_text:

            found.append(skill)

    return sorted(found)


def extract_education(text):

    education = []

    keywords = [

        "b.tech",
        "bachelor",
        "master",
        "m.tech",
        "degree",
        "cgpa",
        "12th",
        "10th",
        "school",
        "college",
        "university"

    ]

    lines = text.splitlines()

    for line in lines:

        lower = line.lower()

        if any(keyword in lower for keyword in keywords):

            education.append(line.strip())

    return education


def analyze_resume(text):

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text)

    }