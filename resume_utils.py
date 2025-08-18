import re
import PyPDF2

# ===== Roles and Skills =====
role_skill_map = {

    # AI / ML / Data Science
    "Data Scientist": ["Python", "Pandas", "NumPy", "Scikit-learn", "Machine Learning", "Deep Learning", "Statistics", "Data Visualization", "SQL", "Matplotlib", "Seaborn"],
    "Machine Learning Engineer": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "ML Algorithms", "Model Deployment", "Data Preprocessing", "Keras", "CNN", "RNN"],
    "AI Researcher": ["Python", "Deep Learning", "Neural Networks", "NLP", "Computer Vision", "Research Papers", "TensorFlow", "PyTorch", "Algorithm Design"],
    "Data Analyst": ["Excel", "SQL", "Power BI", "Tableau", "Python", "Data Cleaning", "Visualization", "Statistics", "Dashboarding"],

    # Full Stack / Software
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express.js", "SQL", "MongoDB", "REST API", "Bootstrap", "Responsive Design"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Bootstrap", "Responsive Design", "UI/UX", "AJAX"],
    "Backend Developer": ["Python", "Django", "Flask", "Node.js", "REST API", "Database", "SQL", "MongoDB", "Authentication", "APIs"],
    "Cloud Engineer": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform", "CI/CD", "Cloud Security", "Serverless Architecture"],

    # ECE / Electronics & Communication
    "Embedded Systems Engineer": ["C", "C++", "Microcontrollers", "Arduino", "Raspberry Pi", "Signal Processing", "PCB Design", "IoT", "Sensors"],
    "VLSI Engineer": ["Verilog", "VHDL", "FPGA", "Digital Design", "ASIC", "Timing Analysis", "Cadence", "Synopsys", "Logic Synthesis"],
    "Communication Engineer": ["Signals", "Telecommunication", "Modulation", "Networking", "MATLAB", "Wireless Systems", "RF Design", "Antenna Design"],
    "Electronics Engineer": ["Circuits", "Analog Electronics", "Digital Electronics", "PCB Design", "Microcontrollers", "MATLAB", "Oscilloscopes"],

    # EEE / Electrical & Electronics
    "Electrical Engineer": ["Circuit Analysis", "Power Systems", "Electrical Machines", "MATLAB", "Control Systems", "Transformers", "Switchgear", "Protection Systems"],
    "Power Systems Engineer": ["Load Flow Analysis", "Power Transmission", "SCADA", "ETAP", "MATLAB", "Protection Systems", "Substation Design"],
    "Control Systems Engineer": ["PID", "MATLAB", "Simulink", "Automation", "PLC", "Sensors", "Feedback Systems", "Robotics Control"],

    # Forensic / Cybersecurity
    "Forensic Analyst": ["Digital Forensics", "Evidence Collection", "Cybersecurity", "Network Analysis", "Malware Analysis", "Python", "EnCase", "FTK", "Incident Response"],
    "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "Firewalls", "Ethical Hacking", "SIEM", "Python", "Wireshark", "Vulnerability Assessment"],
    "Information Security Engineer": ["Cryptography", "Security Policies", "Risk Assessment", "Network Security", "Python", "IDS/IPS", "Firewall Configuration"],

    # Mechanical / Civil
    "Mechanical Engineer": ["AutoCAD", "SolidWorks", "Thermodynamics", "Material Science", "MATLAB", "Design Engineering", "CFD", "Mechanics"],
    "Civil Engineer": ["AutoCAD", "Structural Analysis", "Revit", "Construction Management", "Surveying", "Material Testing", "Project Planning"],

    # Miscellaneous / Other
    "Business Analyst": ["Requirements Gathering", "Data Analysis", "Excel", "Power BI", "SQL", "Communication", "Documentation", "Stakeholder Management"],
    "QA Engineer": ["Manual Testing", "Selenium", "Automation Testing", "Test Cases", "Bug Tracking", "JIRA", "Regression Testing"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "AWS", "Azure", "Linux", "Terraform", "Jenkins", "Monitoring"],
    "Network Engineer": ["Routing", "Switching", "LAN/WAN", "TCP/IP", "Cisco", "Firewalls", "Network Troubleshooting"],

    # Additional emerging tech roles
    "Robotics Engineer": ["ROS", "Python", "C++", "Sensors", "Actuators", "Control Systems", "Arduino", "Simulation"],
    "IoT Engineer": ["IoT", "Arduino", "Raspberry Pi", "Sensors", "MQTT", "Embedded Systems", "C", "Python"],
    "Blockchain Developer": ["Solidity", "Ethereum", "Smart Contracts", "Web3.js", "Cryptography", "Decentralized Apps", "Python"],
    "Cloud Data Engineer": ["SQL", "Python", "ETL", "BigQuery", "AWS", "Data Pipelines", "Data Warehousing", "Spark"]
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
