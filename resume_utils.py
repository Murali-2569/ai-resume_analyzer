# import os
# import re
# from typing import List, Dict, Tuple
# import PyPDF2
# from io import StringIO

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Define role-to-skill mapping
# role_skill_map = {
#     "Machine Learning Engineer": ["machine learning", "tensorflow", "scikit-learn", "pandas", "classification", "prediction", "models", "deep learning", "algorithms"],
#     "Data Scientist": ["data analysis", "statistics", "python", "machine learning", "visualization", "pandas", "numpy", "regression", "classification"],
#     "Software Engineer": ["data structures", "algorithms", "python", "java", "c++", "git", "oop", "problem solving", "api"],
#     "Data Analyst": ["excel", "sql", "tableau", "powerbi", "data visualization", "analysis", "statistics", "reporting"],
#     "Full Stack Developer": ["html", "css", "javascript", "react", "node.js", "express", "mongodb", "api", "git", "deployment"],
#     "UI/UX Designer": ["figma", "adobe xd", "wireframes", "prototyping", "user research", "usability testing", "design systems", "interaction design"],
#     "Cloud Engineer": ["aws", "azure", "gcp", "devops", "docker", "kubernetes", "ci/cd", "linux", "cloud architecture"],
#     "DevOps Engineer": ["docker", "kubernetes", "jenkins", "ci/cd", "linux", "aws", "monitoring", "infrastructure as code"],
#     # Add more as needed
# }


# # Match score function

# def get_match_score(resume_text, jd_text):
#     resume_text_lower = resume_text.lower()
#     jd_keywords = [word.strip().lower() for word in jd_text.split() if len(word.strip()) > 2]

#     found_keywords = [kw for kw in jd_keywords if kw in resume_text_lower]
#     missing_keywords = list(set(jd_keywords) - set(found_keywords))

#     score = len(found_keywords) / len(jd_keywords) if jd_keywords else 0.0
#     return score * 100, missing_keywords

# # Extract text from uploaded file
# def extract_text_from_file(uploaded_file) -> str:
#     if uploaded_file.name.endswith('.pdf'):
#         try:
#             reader = PyPDF2.PdfReader(uploaded_file)
#             text = ""
#             for page in reader.pages:
#                 text += page.extract_text() or ""
#             return text.lower()
#         except Exception as e:
#             return f"Error reading PDF: {e}"
#     elif uploaded_file.name.endswith('.txt'):
#         stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#         return stringio.read().lower()
#     else:
#         return "Unsupported file format"

# # Get roles that suit the resume based on matched keywords
# def get_role_suggestions(resume_text: str, role_skill_map: Dict[str, List[str]]) -> List[Tuple[str, int]]:
#     role_matches = []
#     for role, skills in role_skill_map.items():
#         matched_skills = sum(1 for skill in skills if skill.lower() in resume_text)
#         if matched_skills > 0:
#             role_matches.append((role, matched_skills))
#     sorted_roles = sorted(role_matches, key=lambda x: x[1], reverse=True)
#     return sorted_roles

# # Suggest improvements for a specific role
# def improvement_suggestions(resume_text: str, role: str, role_skill_map: Dict[str, List[str]]) -> List[str]:
#     if role not in role_skill_map:
#         return []
#     missing = [skill for skill in role_skill_map[role] if skill.lower() not in resume_text]
#     return missing

# # Check if resume is suitable or not
# def is_resume_suitable(resume_text: str, role: str, role_skill_map: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
#     missing = improvement_suggestions(resume_text, role, role_skill_map)
#     is_suitable = len(missing) < len(role_skill_map.get(role, [])) * 0.5
#     return is_suitable, missing





import os
import re
from typing import List, Dict, Tuple
import PyPDF2
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Expanded role-to-skill mapping
role_skill_map = {
    "Machine Learning Engineer": ["machine learning", "tensorflow", "scikit-learn", "pandas", "classification", "prediction", "models", "deep learning", "algorithms"],
    "AI/ML Researcher": ["deep learning", "neural networks", "reinforcement learning", "NLP", "generative models", "research", "experiments", "pytorch", "transformers"],
    "Data Scientist": ["data analysis", "statistics", "python", "machine learning", "visualization", "pandas", "numpy", "regression", "classification"],
    "Data Analyst": ["excel", "sql", "tableau", "powerbi", "data visualization", "analysis", "statistics", "reporting"],
    "Software Engineer": ["data structures", "algorithms", "python", "java", "c++", "git", "oop", "problem solving", "api"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node.js", "express", "mongodb", "api", "git", "deployment"],
    "Frontend Developer": ["html", "css", "javascript", "react", "vue", "angular", "bootstrap", "sass"],
    "Backend Developer": ["node.js", "django", "flask", "express", "api", "sql", "mongodb", "python", "java", "server"],
    "UI/UX Designer": ["figma", "adobe xd", "wireframes", "prototyping", "user research", "usability testing", "design systems", "interaction design"],
    "Mobile App Developer": ["flutter", "react native", "android", "ios", "dart", "swift", "kotlin", "mobile UI"],
    "Cloud Engineer": ["aws", "azure", "gcp", "devops", "docker", "kubernetes", "ci/cd", "linux", "cloud architecture"],
    "DevOps Engineer": ["docker", "kubernetes", "jenkins", "ci/cd", "linux", "aws", "monitoring", "infrastructure as code"],
    "Cybersecurity Analyst": ["cybersecurity", "network security", "penetration testing", "firewalls", "encryption", "threat analysis", "vulnerability assessment", "siem"],
    "Business Analyst": ["business analysis", "requirements gathering", "stakeholder management", "excel", "data analysis", "documentation", "gap analysis", "jira"],
    "Blockchain Developer": ["blockchain", "solidity", "smart contracts", "ethereum", "web3", "cryptography", "dapps"],
}

# Match score function
def get_match_score(resume_text, jd_text):
    resume_text_lower = resume_text.lower()
    jd_keywords = [word.strip().lower() for word in jd_text.split() if len(word.strip()) > 2]

    found_keywords = [kw for kw in jd_keywords if kw in resume_text_lower]
    missing_keywords = list(set(jd_keywords) - set(found_keywords))

    score = len(found_keywords) / len(jd_keywords) if jd_keywords else 0.0
    return score * 100, missing_keywords


# Extract text from uploaded file
def extract_text_from_file(uploaded_file) -> str:
    if uploaded_file.name.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.lower()
        except Exception as e:
            return f"Error reading PDF: {e}"
    elif uploaded_file.name.endswith('.txt'):
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read().lower()
    else:
        return "Unsupported file format"


# Get roles that suit the resume based on matched keywords
def get_role_suggestions(resume_text: str, role_skill_map: Dict[str, List[str]]) -> List[Tuple[str, int]]:
    role_matches = []
    for role, skills in role_skill_map.items():
        matched_skills = sum(1 for skill in skills if skill.lower() in resume_text)
        if matched_skills > 0:
            role_matches.append((role, matched_skills))
    sorted_roles = sorted(role_matches, key=lambda x: x[1], reverse=True)
    return sorted_roles

# Suggest improvements for a specific role
def improvement_suggestions(resume_text: str, role: str, role_skill_map: Dict[str, List[str]]) -> List[str]:
    if role not in role_skill_map:
        return []
    missing = [skill for skill in role_skill_map[role] if skill.lower() not in resume_text]
    return missing

# Check if resume is suitable or not
def is_resume_suitable(resume_text: str, role: str, role_skill_map: Dict[str, List[str]]) -> Tuple[bool, List[str]]:
    missing = improvement_suggestions(resume_text, role, role_skill_map)
    is_suitable = len(missing) < len(role_skill_map.get(role, [])) * 0.5
    return is_suitable, missing
