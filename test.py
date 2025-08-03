# import os
# from resume_matcher_utils import extract_text_from_pdf, extract_text_from_txt, calculate_match_score

# JD_FOLDER = "jobs"
# RESUME_FOLDER = "resumes"

# def read_text(file_path):
#     if file_path.endswith(".pdf"):
#         return extract_text_from_pdf(file_path)
#     elif file_path.endswith(".txt"):
#         return extract_text_from_txt(file_path)
#     else:
#         return None

# print("=== MATCH RESULTS ===\n")

# for jd_file in os.listdir(JD_FOLDER):
#     jd_path = os.path.join(JD_FOLDER, jd_file)
#     jd_text = read_text(jd_path)
#     if jd_text is None:
#         print(f"{jd_file} ➝ Skipped (Unsupported file type)")
#         continue

#     for resume_file in os.listdir(RESUME_FOLDER):
#         resume_path = os.path.join(RESUME_FOLDER, resume_file)
#         resume_text = read_text(resume_path)
#         if resume_text is None:
#             print(f"{resume_file} ➝ Skipped (Unsupported file type)")
#             continue

#         score = calculate_match_score(jd_text, resume_text)
#         print(f"{resume_file} ➝ Match Score: {score*100:.2f}%")


from resume_utils import extract_text_from_pdf, extract_text_from_txt, calculate_match_score, get_missing_keywords
import os
import csv

# 🔧 Role-to-skill mapping
role_skill_map = {
    "Data Scientist": ["python", "pandas", "scikit-learn", "sql", "statistics", "machine learning", "data analysis"],
    "Machine Learning Engineer": ["python", "tensorflow", "scikit-learn", "keras", "deep learning", "deployment", "mlops"],
    "Data Analyst": ["excel", "sql", "power bi", "tableau", "data visualization", "python", "data cleaning"],
    "AI Engineer": ["python", "transformers", "pytorch", "nlp", "deep learning", "opencv", "llms", "chatgpt"],
    "Software Engineer": ["java", "python", "c++", "problem solving", "algorithms", "data structures"],
}

# 📌 Helper functions
def suggest_roles(resume_text, role_skill_map):
    resume_text_lower = resume_text.lower()
    matched_roles = {}

    for role, skills in role_skill_map.items():
        match_count = sum(skill.lower() in resume_text_lower for skill in skills)
        if match_count:
            matched_roles[role] = match_count

    return sorted(matched_roles.items(), key=lambda x: x[1], reverse=True)

def improvement_suggestions(resume_text, target_role, role_skill_map):
    resume_text_lower = resume_text.lower()
    required_skills = role_skill_map.get(target_role, [])
    missing = [skill for skill in required_skills if skill.lower() not in resume_text_lower]
    return missing

# 🗂️ Folders
job_folder = "jobs"
resume_folder = "resumes"

# 📄 Load JD
job_files = [f for f in os.listdir(job_folder) if f.endswith('.txt')]
if not job_files:
    print("❌ No job description found in the 'jobs' folder.")
    exit()

with open(os.path.join(job_folder, job_files[0]), 'r', encoding='utf-8') as f:
    jd_text = f.read()

print("=== MATCH RESULTS ===\n")
print(f"📄 Job Description Preview:\n{jd_text[:300]}...\n")

# ✅ Resume processing
results = []

for resume_file in os.listdir(resume_folder):
    if not (resume_file.endswith('.txt') or resume_file.endswith('.pdf')):
        print(f"{resume_file} ➝ Skipped (Unsupported file type)")
        continue

    resume_path = os.path.join(resume_folder, resume_file)
    resume_text = extract_text_from_txt(resume_path) if resume_file.endswith(".txt") else extract_text_from_pdf(resume_path)

    score, missing = calculate_match_score(resume_text, jd_text)
    results.append((resume_file, score))
    print(f"{resume_file} ➝ Match Score: {score:.2f}%")

    # 🔍 Missing keywords
    print(f"🛠️ Missing Keywords in {resume_file}: {', '.join(missing) if missing else 'None'}")

    # 🧠 Suggest roles
    suggested_roles = suggest_roles(resume_text, role_skill_map)
    if suggested_roles:
        print(f"🧠 Roles suited for {resume_file}:")
        for role, count in suggested_roles[:3]:
            print(f"  - {role} (matched {count} relevant skills)")

        # 💡 Suggestions to improve resume for top role
        top_role = suggested_roles[0][0]
        suggestions = improvement_suggestions(resume_text, top_role, role_skill_map)
        if suggestions:
            print(f"💡 To improve for '{top_role}', consider adding: {', '.join(suggestions)}")
        else:
            print(f"💡 Your resume already has most skills for '{top_role}'")
    else:
        print(f"🧠 No matching roles found for {resume_file}")

    # ✅ Suitability Check
    threshold = 50.0
    if score >= threshold:
        suitability = "✅ Suitable"
        reason = "Includes most required keywords"
    else:
        suitability = "❌ Not Suitable"
        reason = f"Missing key skills: {', '.join(missing[:5])}" if missing else "Lacks alignment with job requirements"
    print(f"{suitability} — {reason}\n")

# 🎯 Best Match
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    print(f"🎯 Best Match: {results[0][0]} with {results[0][1]:.2f}%")

# 📦 Export to CSV
with open("match_results.csv", "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Resume", "Match Score"])
    writer.writerows(results)
    print("\n✅ Results exported to match_results.csv")

    