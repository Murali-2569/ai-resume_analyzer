import re
import PyPDF2

# ===== Roles and Skills =====
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

# ===== Extract text from PDF/TXT =====
def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "".join([page.extract_text() or "" for page in reader.pages])
        return text
    elif name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")
    return ""

# ===== Basic keyword match =====
def get_match_score(resume_text, jd_text):
    r = resume_text.lower()
    words = [w for w in jd_text.lower().split() if len(w) > 2]
    if not words:
        return 0.0, []
    found = [w for w in words if w in r]
    missing = list(set(words) - set(found))
    return (len(found) / len(words)) * 100, missing

# ===== Role suggestions (top-3) from resume =====
def get_role_suggestions(resume_text):
    r = resume_text.lower()
    scored = []
    for role, skills in role_skill_map.items():
        score = sum(1 for s in skills if s in r)
        if score:
            pct = round((score / max(len(skills), 1)) * 100, 2)
            scored.append((role, pct))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:3]

# ===== Suggestions for improvement (missing role skills) =====
def improvement_suggestions(resume_text, role, role_skill_map_input=None):
    r = resume_text.lower()
    skills = (role_skill_map_input or role_skill_map).get(role, [])
    return [s for s in skills if s not in r]

# ===== Suitability check for a role (thresholded) =====
def is_resume_suitable(resume_text, role, role_skill_map_input=None, threshold=30):
    skills_text = " ".join((role_skill_map_input or role_skill_map).get(role, []))
    score, missing = get_match_score(resume_text, skills_text)
    return (score >= threshold, missing)
