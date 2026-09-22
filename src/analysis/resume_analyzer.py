import re
from src.utils.skills import SKILLS


def extract_email(text):
    """
    Extract email address from resume text.
    """
    match = re.search(
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
        text
    )
    return match.group(0) if match else "Not Found"


def extract_phone(text):
    """
    Extract phone number from resume text.
    Supports Indian numbers (+91), US/international formats,
    hyphenated, dotted, and spaced formats.
    """
    patterns = [
        # Standard international with optional + and country code
        r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}',
        # 10-12 consecutive or lightly spaced digits
        r'(?:\+?91[-.\s]?)?[6-9]\d{4}[-.\s]?\d{5}',
        r'\b\d{5}[-.\s]?\d{5}\b'
    ]

    for pat in patterns:
        for match in re.finditer(pat, text):
            raw = match.group(0).strip()
            digits = re.sub(r'\D', '', raw)
            # Check length of digits: standard phone numbers are 10-13 digits
            if 10 <= len(digits) <= 13:
                # Discard years/date ranges like 2018-2022
                if re.match(r'^(19|20)\d{2}[-.\s]?(19|20)\d{2}$', raw):
                    continue
                return raw

    return "Not Found"


def extract_name(text):
    """
    Extract candidate name from the top of the resume.
    Avoids generic headings like 'Candidate Information', 'Resume', etc.
    """
    headers_to_ignore = {
        "curriculum vitae",
        "resume",
        "candidate information",
        "contact information",
        "personal details",
        "profile",
        "profile summary",
        "summary",
        "biodata",
        "bio-data",
        "cv",
        "name",
        "contact",
        "about me"
    }

    lines = text.splitlines()

    for line in lines[:20]:
        cleaned = line.strip()
        cleaned_lower = cleaned.lower().strip(":- ")

        if not cleaned:
            continue

        if cleaned_lower in headers_to_ignore:
            continue

        # Skip email, phone, links, addresses
        if any(cleaned_lower.startswith(prefix) for prefix in [
            "email", "phone", "contact", "address", "linkedin", "github", "http"
        ]):
            continue

        words = cleaned.split()
        # Candidate names typically have 2 to 4 words and are not excessively long
        if 2 <= len(words) <= 4 and len(cleaned) < 40:
            # Check that characters are primarily alphabetic
            if all(w.replace(".", "").replace("-", "").isalpha() for w in words):
                return cleaned

    return "Not Found"


def extract_skills(text):
    """
    Extract matched skills using word-boundary aware regex matching.
    Prevents false positive substring matches (e.g. 'c' in 'education').
    """
    found = set()
    lower_text = text.lower()

    for skill in SKILLS:
        skill_lower = skill.lower()

        # Handle special/short symbols carefully (C, C++, C#, R, Go, AI, ML)
        if len(skill_lower) <= 2 or skill_lower in ["c", "r", "go", "ai", "ml", "ui", "ux", ".net"]:
            escaped = re.escape(skill_lower)
            pattern = r'(?:\b|(?<=[^a-zA-Z0-9]))' + escaped + r'(?=\b|(?=[^a-zA-Z0-9]))'
            if re.search(pattern, lower_text):
                found.add(skill)
        elif "++" in skill_lower or "#" in skill_lower:
            escaped = re.escape(skill_lower)
            if re.search(escaped, lower_text):
                found.add(skill)
        else:
            escaped = re.escape(skill_lower)
            pattern = r'\b' + escaped + r'\b'
            if re.search(pattern, lower_text):
                found.add(skill)

    return sorted(list(found))


def extract_education(text):
    """
    Extract education credentials and qualifications from resume text.
    """
    education = []

    keywords = [
        "b.tech", "btech", "b.e", "bachelor", "bachelors",
        "master", "masters", "m.tech", "mtech", "m.e",
        "degree", "cgpa", "gpa", "percentage",
        "12th", "10th", "school", "college", "university", "institute",
        "diploma", "intermediate", "matriculation", "higher secondary",
        "b.sc", "bsc", "m.sc", "msc", "bca", "mca",
        "b.com", "bcom", "mba", "bba", "b.a", "ba",
        "phd", "ph.d", "doctorate", "cbse", "icse", "state board",
        "undergraduate", "postgraduate", "academics", "qualification"
    ]

    lines = text.splitlines()

    for line in lines:
        cleaned = line.strip()
        lower = cleaned.lower()

        if any(keyword in lower for keyword in keywords):
            # Avoid long paragraphs or sentences that merely mention a keyword
            if 3 < len(cleaned) < 140:
                education.append(cleaned)

    return education


def analyze_resume(text):
    """
    Analyze resume and extract candidate details, skills, and education.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text)
    }