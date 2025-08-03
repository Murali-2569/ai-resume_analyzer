# # import streamlit as st
# # from io import StringIO
# # import fitz  # PyMuPDF
# # from resume_utils import extract_text_from_file, get_match_score, get_role_suggestions, improvement_suggestions, is_resume_suitable, role_skill_map
# # import re

# # st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
# # st.title("📄 AI Resume Analyzer")
# # st.write("Upload resumes and a job description to analyze match scores.")

# # # Upload job description
# # jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# # # Upload resumes
# # resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

# # if jd_file and resumes:
# #     # Extract job description text
# #     jd_text = jd_file.read().decode("utf-8")

# #     st.success("✅ Job description uploaded!")
# #     st.write("### 🧠 Job Description Preview:")
# #     st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

# #     for resume_file in resumes:
# #         # Extract resume text
# #         resume_text = extract_text_from_file(resume_file)

# #         # Match score
# #         score, missing_keywords = get_match_score(resume_text, jd_text)
# #         role_matches = get_role_suggestions(resume_text, role_skill_map)
# #         # Let user select the target role

# #         selected_role = st.selectbox(
# #           f"🎯 Select Target Role for {resume_file.name}",
# #               list(role_skill_map.keys()),
# #               key=f"role_select_{resume_file.name}"
# #             )


# #         # Then use that role for suitability and suggestions
# #         suitable, reasons = is_resume_suitable(resume_text, selected_role, role_skill_map)
# #         improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)

# #         # Display results
# #         st.subheader(f"📄 {resume_file.name}")
# #         st.markdown(f"**Match Score:** {score:.2f}%")
# #         st.markdown(f"**Missing Keywords:** `{', '.join(missing_keywords[:15])}`")

# #         st.markdown("### 🧠 Top Role Matches:")
# #         for role, _ in role_matches[:3]:  # Top 3 role suggestions
# #             suitable, reasons = is_resume_suitable(resume_text, role, role_skill_map)
# #             improvement = improvement_suggestions(resume_text, role, role_skill_map)

# #             st.markdown(f"#### 🎯 {role}")
# #             st.markdown(f"- ✅ Suitable: {'Yes' if suitable else 'No'}")
# #             st.markdown(f"- 💡 Suggestions: `{', '.join(improvement[:10])}`")

# #         st.markdown("---")

# # else:
# #     st.info("📌 Please upload both a job description and at least one resume.")












# # import streamlit as st
# # from io import StringIO
# # import fitz  # PyMuPDF
# # import pandas as pd
# # from resume_utils import (
# #     extract_text_from_file,
# #     get_match_score,
# #     get_role_suggestions,
# #     improvement_suggestions,
# #     is_resume_suitable,
# #     role_skill_map
# # )

# # st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
# # st.title("📄 AI Resume Analyzer")
# # st.write("Upload resumes and a job description to analyze match scores and role suitability.")

# # # Function to extract role from JD
# # def extract_role_from_jd(jd_text):
# #     jd_text_lower = jd_text.lower()
# #     for role in role_skill_map.keys():
# #         if role.lower() in jd_text_lower:
# #             return role
# #     return None

# # # Upload job description
# # jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# # # Upload resumes
# # resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

# # if jd_file and resumes:
# #     jd_text = jd_file.read().decode("utf-8")
# #     jd_role = extract_role_from_jd(jd_text) or "Machine Learning Engineer"  # Fallback

# #     st.success(f"✅ Job description uploaded! Detected Role: `{jd_role}`")
# #     st.write("### 🧠 Job Description Preview:")
# #     st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

# #     # Store all resume results for summary table
# #     results = []

# #     for resume_file in resumes:
# #         resume_text = extract_text_from_file(resume_file)

# #         # Analyze for JD role only (default)
# #         jd_score, jd_missing_keywords = get_match_score(resume_text, jd_text)
# #         jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
# #         jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

# #         # Add to summary results
# #         results.append({
# #             "Resume": resume_file.name,
# #             "Match Score (%)": round(jd_score, 2),
# #             "Suitable": "Yes" if jd_suitable else "No",
# #             "Top Missing Keywords": ", ".join(jd_missing_keywords[:5])
# #         })

# #         # Display per-resume results
# #         st.subheader(f"📄 {resume_file.name}")
# #         st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
# #         st.markdown(f"- **Match Score:** {jd_score:.2f}%")
# #         st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
# #         st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:15])}`")
# #         st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

# #         # Dropdown to optionally select another role
# #         with st.expander(f"🔍 Try Other Role Matching for {resume_file.name}"):
# #             selected_role = st.selectbox(
# #                 "Select another role to test suitability:",
# #                 list(role_skill_map.keys()),
# #                 key=f"role_select_{resume_file.name}"
# #             )

# #             if selected_role:
# #                 alt_suitable, _ = is_resume_suitable(resume_text, selected_role, role_skill_map)
# #                 alt_improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)

# #                 st.markdown(f"### 🧪 Results for Selected Role: `{selected_role}`")
# #                 st.markdown(f"- ✅ Suitable: {'Yes' if alt_suitable else 'No'}")
# #                 st.markdown(f"- 💡 Suggestions: `{', '.join(alt_improvement[:10])}`")

# #         st.markdown("---")

# #     # Summary Table
# #     if results:
# #         df = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)
# #         st.write("### 📊 Resume Comparison Summary:")
# #         st.dataframe(df)

# # else:
# #     st.info("📌 Please upload both a job description and at least one resume.")










# # import streamlit as st
# # from io import StringIO
# # import fitz  # PyMuPDF
# # import pandas as pd
# # from resume_utils import (
# #     extract_text_from_file,
# #     get_match_score,
# #     get_role_suggestions,
# #     improvement_suggestions,
# #     is_resume_suitable,
# #     role_skill_map
# # )

# # st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
# # st.title("📄 AI Resume Analyzer")
# # st.write("Upload resumes and a job description to analyze match scores, role suitability, and export results.")

# # # Function to extract role from JD
# # def extract_role_from_jd(jd_text):
# #     jd_text_lower = jd_text.lower()
# #     for role in role_skill_map.keys():
# #         if role.lower() in jd_text_lower:
# #             return role
# #     return None

# # # Upload job description
# # jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# # # Upload resumes
# # resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

# # all_results = []

# # if jd_file and resumes:
# #     jd_text = jd_file.read().decode("utf-8")
# #     jd_role = extract_role_from_jd(jd_text) or "Machine Learning Engineer"

# #     st.success(f"✅ Job description uploaded! Detected Role: `{jd_role}`")
# #     st.write("### 🧠 Job Description Preview:")
# #     st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

# #     resume_scores = []

# #     for resume_file in resumes:
# #         resume_text = extract_text_from_file(resume_file)
# #         jd_score, jd_missing_keywords = get_match_score(resume_text, jd_text)
# #         jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
# #         jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

# #         resume_scores.append((resume_file.name, jd_score))
# #         all_results.append({
# #             "Resume": resume_file.name,
# #             "Target Role": jd_role,
# #             "Score": jd_score,
# #             "Suitable": "Yes" if jd_suitable else "No",
# #             "Missing Keywords": ", ".join(jd_missing_keywords[:10]),
# #             "Suggestions": ", ".join(jd_improvement[:10])
# #         })

# #         st.subheader(f"📄 {resume_file.name}")
# #         st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
# #         st.markdown(f"- **Match Score:** {jd_score:.2f}%")
# #         st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
# #         st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:10])}`")
# #         st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

# #         with st.expander(f"🔍 Try Other Role Matching for {resume_file.name}"):
# #             selected_role = st.selectbox(
# #                 "Select another role to test suitability:",
# #                 list(role_skill_map.keys()),
# #                 key=f"role_select_{resume_file.name}"
# #             )

# #             if selected_role:
# #                 role_score, role_missing_keywords = get_match_score(resume_text, ' '.join(role_skill_map[selected_role]))
# #                 alt_suitable, _ = is_resume_suitable(resume_text, selected_role, role_skill_map)
# #                 alt_improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)
                
# #                 st.markdown(f"### 🧪 Results for Selected Role: `{selected_role}`")
# #                 st.markdown(f"- **Match Score:** {role_score:.2f}%")
# #                 st.markdown(f"- ✅ Suitable: {'Yes' if alt_suitable else 'No'}")
# #                 st.markdown(f"- **Missing Keywords:** `{', '.join(role_missing_keywords[:15])}`")
# #                 st.markdown(f"- 💡 Suggestions: `{', '.join(alt_improvement[:10])}`")

# #         st.markdown("---")

# #     # Show top 3 resumes
# #     st.markdown("## 🏆 Top 3 Resumes by Score")
# #     top_3 = sorted(resume_scores, key=lambda x: x[1], reverse=True)[:3]
# #     for i, (name, score) in enumerate(top_3, 1):
# #         st.markdown(f"{i}. **{name}** - `{score:.2f}%`")

# #     # Show score chart
# #     st.markdown("## 📊 Match Score Comparison")
# #     chart_df = pd.DataFrame(resume_scores, columns=["Resume", "Score"])
# #     st.bar_chart(chart_df.set_index("Resume"))

# #     # Export to CSV
# #     result_df = pd.DataFrame(all_results)
# #     csv = result_df.to_csv(index=False).encode('utf-8')
# #     st.download_button("📥 Download Results as CSV", data=csv, file_name="resume_analysis.csv", mime="text/csv")

# # else:
# #     st.info("📌 Please upload both a job description and at least one resume.")






# # import streamlit as st
# # from io import StringIO
# # import fitz  # PyMuPDF
# # import pandas as pd
# # from resume_utils import (
# #     extract_text_from_file,
# #     get_match_score,
# #     get_role_suggestions,
# #     improvement_suggestions,
# #     is_resume_suitable,
# #     role_skill_map
# # )
# # import re

# # st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
# # st.title("📄 AI Resume Analyzer")
# # st.write("Upload resumes and a job description to analyze match scores and role suitability.")

# # # Function to extract role from JD
# # def extract_role_from_jd(jd_text):
# #     jd_text_lower = jd_text.lower()
# #     for role in role_skill_map.keys():
# #         if role.lower() in jd_text_lower:
# #             return role
# #     return None

# # # Highlight skills in resume
# # def highlight_skills(resume_text, skills):
# #     highlighted_text = resume_text
# #     for skill in skills:
# #         pattern = re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
# #         highlighted_text = pattern.sub(f"<span style='color:green'><b>{skill}</b></span>", highlighted_text)
# #     return highlighted_text

# # def highlight_missing_skills(resume_text, skills):
# #     missing = []
# #     present = []
# #     for skill in skills:
# #         if re.search(rf'\b{re.escape(skill)}\b', resume_text, re.IGNORECASE):
# #             present.append(skill)
# #         else:
# #             missing.append(skill)
# #     return present, missing

# # # Upload job description
# # jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# # # Upload resumes
# # resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

# # if jd_file and resumes:
# #     jd_text = jd_file.read().decode("utf-8")
# #     jd_role = extract_role_from_jd(jd_text) or "Machine Learning Engineer"  # Fallback

# #     st.success(f"✅ Job description uploaded! Detected Role: `{jd_role}`")
# #     st.write("### 🧠 Job Description Preview:")
# #     st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

# #     resume_scores = []
# #     all_results = []

# #     for resume_file in resumes:
# #         resume_text = extract_text_from_file(resume_file)

# #         # Analyze for JD role only (default)
# #         jd_score, jd_missing_keywords = get_match_score(resume_text, jd_text)
# #         jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
# #         jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

# #         resume_scores.append((resume_file.name, jd_score))
# #         all_results.append({
# #             "Resume": resume_file.name,
# #             "Target Role": jd_role,
# #             "Score": jd_score,
# #             "Suitable": "Yes" if jd_suitable else "No",
# #             "Missing Keywords": ", ".join(jd_missing_keywords[:10]),
# #             "Suggestions": ", ".join(jd_improvement[:10])
# #         })

# #         st.subheader(f"📄 {resume_file.name}")
# #         st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
# #         st.markdown(f"- **Match Score:** {jd_score:.2f}%")
# #         st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
# #         st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:15])}`")
# #         st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

# #         with st.expander(f"🔍 Try Other Role Matching for {resume_file.name}"):
# #             selected_role = st.selectbox(
# #                 "Select another role to test suitability:",
# #                 list(role_skill_map.keys()),
# #                 key=f"role_select_{resume_file.name}"
# #             )

# #             if selected_role:
# #                 alt_suitable, _ = is_resume_suitable(resume_text, selected_role, role_skill_map)
# #                 alt_improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)
# #                 alt_score, alt_missing_keywords = get_match_score(resume_text, ' '.join(role_skill_map[selected_role]))

# #                 st.markdown(f"### 🧪 Results for Selected Role: `{selected_role}`")
# #                 st.markdown(f"- **Match Score:** {alt_score:.2f}%")
# #                 st.markdown(f"- ✅ Suitable: {'Yes' if alt_suitable else 'No'}")
# #                 st.markdown(f"- 💡 Suggestions: `{', '.join(alt_improvement[:10])}`")
# #                 st.markdown(f"- 🔑 Missing Keywords: `{', '.join(alt_missing_keywords[:15])}`")

# #         with st.expander(f"🧠 Highlight Skills in Resume for `{jd_role}`"):
# #             present, missing = highlight_missing_skills(resume_text, role_skill_map.get(jd_role, []))
# #             highlighted = highlight_skills(resume_text, present)
# #             st.markdown("#### ✅ Present Skills Highlighted in Green")
# #             st.markdown(highlighted, unsafe_allow_html=True)
# #             st.markdown(f"#### ❌ Missing Skills:")
# #             st.markdown(f"{', '.join(missing[:20])}")

# #         st.markdown("---")


# #         # Show top 3 resumes
# #     st.markdown("## 🏆 Top 3 Resumes by Score")
# #     top_3 = sorted(resume_scores, key=lambda x: x[1], reverse=True)[:3]
# #     for i, (name, score) in enumerate(top_3, 1):
# #         st.markdown(f"{i}. **{name}** - `{score:.2f}%`")

# #     # Show score chart
# #     st.markdown("## 📊 Match Score Comparison")
# #     chart_df = pd.DataFrame(resume_scores, columns=["Resume", "Score"])
# #     st.bar_chart(chart_df.set_index("Resume"))

# #     # Export to CSV
# #     result_df = pd.DataFrame(all_results)
# #     csv = result_df.to_csv(index=False).encode('utf-8')
# #     st.download_button("📥 Download Results as CSV", data=csv, file_name="resume_analysis.csv", mime="text/csv")


# # else:
# #     st.info("📌 Please upload both a job description and at least one resume.")







# # import streamlit as st
# # from io import StringIO
# # import fitz  # PyMuPDF
# # import pandas as pd
# # from resume_utils import (
# #     extract_text_from_file,
# #     get_match_score,
# #     get_role_suggestions,
# #     improvement_suggestions,
# #     is_resume_suitable,
# #     role_skill_map
# # )
# # import re

# # st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
# # st.title("📄 AI Resume Analyzer")
# # st.write("Upload resumes and a job description to analyze match scores and role suitability.")

# # # Function to extract role from JD
# # def extract_role_from_jd(jd_text):
# #     jd_text_lower = jd_text.lower()
# #     for role in role_skill_map.keys():
# #         if role.lower() in jd_text_lower:
# #             return role
# #     return None

# # # Highlight skills in resume
# # def highlight_skills(resume_text, skills):
# #     highlighted_text = resume_text
# #     for skill in skills:
# #         pattern = re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
# #         highlighted_text = pattern.sub(f"<span style='color:green'><b>{skill}</b></span>", highlighted_text)
# #     return highlighted_text

# # def highlight_missing_skills(resume_text, skills):
# #     missing = []
# #     present = []
# #     for skill in skills:
# #         if re.search(rf'\b{re.escape(skill)}\b', resume_text, re.IGNORECASE):
# #             present.append(skill)
# #         else:
# #             missing.append(skill)
# #     return present, missing

# # # Upload job description
# # jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# # # Upload resumes
# # resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

# # if jd_file and resumes:
# #     jd_text = jd_file.read().decode("utf-8")
# #     jd_role = extract_role_from_jd(jd_text) or "Machine Learning Engineer"  # Fallback

# #     st.success(f"✅ Job description uploaded! Detected Role: `{jd_role}`")
# #     st.write("### 🧠 Job Description Preview:")
# #     st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

# #     resume_scores = []
# #     all_results = []

# #     for resume_file in resumes:
# #         resume_text = extract_text_from_file(resume_file)

# #         # Analyze for JD role only (default)
# #         jd_score, jd_missing_keywords = get_match_score(resume_text, jd_text)
# #         jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
# #         jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

# #         resume_scores.append((resume_file.name, jd_score))
# #         all_results.append({
# #             "Resume": resume_file.name,
# #             "Target Role": jd_role,
# #             "Score": jd_score,
# #             "Suitable": "Yes" if jd_suitable else "No",
# #             "Missing Keywords": ", ".join(jd_missing_keywords[:10]),
# #             "Suggestions": ", ".join(jd_improvement[:10])
# #         })

# #         st.subheader(f"📄 {resume_file.name}")
# #         st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
# #         st.markdown(f"- **Match Score:** {jd_score:.2f}%")
# #         st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
# #         st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:15])}`")
# #         st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

# #         with st.expander(f"🔍 Try Other Role Matching for {resume_file.name}"):
# #             selected_role = st.selectbox(
# #                 "Select another role to test suitability:",
# #                 list(role_skill_map.keys()),
# #                 key=f"role_select_{resume_file.name}"
# #             )

# #             if selected_role:
# #                 alt_suitable, _ = is_resume_suitable(resume_text, selected_role, role_skill_map)
# #                 alt_improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)
# #                 alt_score, alt_missing_keywords = get_match_score(resume_text, ' '.join(role_skill_map[selected_role]))

# #                 st.markdown(f"### 🧪 Results for Selected Role: `{selected_role}`")
# #                 st.markdown(f"- **Match Score:** {alt_score:.2f}%")
# #                 st.markdown(f"- ✅ Suitable: {'Yes' if alt_suitable else 'No'}")
# #                 st.markdown(f"- 💡 Suggestions: `{', '.join(alt_improvement[:10])}`")
# #                 st.markdown(f"- 🔑 Missing Keywords: `{', '.join(alt_missing_keywords[:15])}`")

# #         with st.expander(f"🧠 Highlight Skills in Resume for `{jd_role}`"):
# #             present, missing = highlight_missing_skills(resume_text, role_skill_map.get(jd_role, []))
# #             highlighted = highlight_skills(resume_text, present)
# #             st.markdown("#### ✅ Present Skills Highlighted in Green")
# #             st.markdown(highlighted, unsafe_allow_html=True)
# #             st.markdown(f"#### ❌ Missing Skills:")
# #             st.markdown(f"{', '.join(missing[:20])}")

# #         # 🔍 NEW: Predict top 3 roles from resume (not JD)
# #         role_scores = []
# #         for role in role_skill_map:
# #             score, _ = get_match_score(resume_text, ' '.join(role_skill_map[role]))
# #             role_scores.append((role, score))

# #         role_scores_sorted = sorted(role_scores, key=lambda x: x[1], reverse=True)
# #         top_roles = role_scores_sorted[:3]

# #         st.markdown(f"### 🔮 Top 3 Predicted Roles from Resume:")
# #         for i, (role, score) in enumerate(top_roles, 1):
# #             st.markdown(f"{i}. **{role}** - `{score:.2f}%`")

# #         st.markdown("#### 📈 Role Suitability Prediction Chart")
# #         chart_df_roles = pd.DataFrame(role_scores_sorted, columns=["Role", "Score"])
# #         st.bar_chart(chart_df_roles.set_index("Role"))

# #         st.markdown("---")

# #     # Show top 3 resumes
# #     st.markdown("## 🏆 Top 3 Resumes by Score")
# #     top_3 = sorted(resume_scores, key=lambda x: x[1], reverse=True)[:3]
# #     for i, (name, score) in enumerate(top_3, 1):
# #         st.markdown(f"{i}. **{name}** - `{score:.2f}%`")

# #     # Show score chart
# #     st.markdown("## 📊 Match Score Comparison")
# #     chart_df = pd.DataFrame(resume_scores, columns=["Resume", "Score"])
# #     st.bar_chart(chart_df.set_index("Resume"))

# #     # Export to CSV
# #     result_df = pd.DataFrame(all_results)
# #     csv = result_df.to_csv(index=False).encode('utf-8')
# #     st.download_button("📥 Download Results as CSV", data=csv, file_name="resume_analysis.csv", mime="text/csv")

# # else:
# #     st.info("📌 Please upload both a job description and at least one resume.")





import streamlit as st
from io import StringIO
import fitz  # PyMuPDF
import pandas as pd
from resume_utils import (
    extract_text_from_file,
    get_match_score,
    get_role_suggestions,
    improvement_suggestions,
    is_resume_suitable,
    role_skill_map
)

import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄🧠 AI Resume Analyzer")
st.markdown("##### Crafted by Murali Krishna & Jarvis AI")
st.write("Upload resumes and a job description to analyze match scores and role suitability.")

# Function to extract role from JD
def extract_role_from_jd(jd_text):
    jd_text_lower = jd_text.lower()
    for role in role_skill_map.keys():
        if role.lower() in jd_text_lower:
            return role
    return None

# Highlight skills in resume
def highlight_skills(resume_text, skills):
    highlighted_text = resume_text
    for skill in skills:
        pattern = re.compile(rf'\b{re.escape(skill)}\b', re.IGNORECASE)
        highlighted_text = pattern.sub(f"<span style='color:green'><b>{skill}</b></span>", highlighted_text)
    return highlighted_text

def highlight_missing_skills(resume_text, skills):
    missing = []
    present = []
    for skill in skills:
        if re.search(rf'\b{re.escape(skill)}\b', resume_text, re.IGNORECASE):
            present.append(skill)
        else:
            missing.append(skill)
    return present, missing

# Upload job description
jd_file = st.file_uploader("📑 Upload Job Description (.txt)", type=["txt"])
# Upload resumes
resumes = st.file_uploader("📂 Upload Resumes (.pdf or .txt)", type=["pdf", "txt"], accept_multiple_files=True)

if jd_file and resumes:
    jd_text = jd_file.read().decode("utf-8")
    jd_role = extract_role_from_jd(jd_text) or "Machine Learning Engineer"  # Fallback

    st.success(f"✅ Job description uploaded! Detected Role: `{jd_role}`")
    st.write("### 🧠 Job Description Preview:")
    st.code(jd_text[:500] + ("..." if len(jd_text) > 500 else ""), language="text")

    # resume_scores = []
    # all_results = []
    # all_resumes_data = []

    # for resume_file in resumes:
    #     resume_text = extract_text_from_file(resume_file)

    #     # Analyze for JD role only (default)
    #     jd_score, jd_missing_keywords = get_match_score(resume_text, jd_text)
    #     jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
    #     jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

    #     resume_scores.append((resume_file.name, jd_score))
    #     all_results.append({
    #         "Resume": resume_file.name,
    #         "Target Role": jd_role,
    #         "Score": jd_score,
    #         "Suitable": "Yes" if jd_suitable else "No",
    #         "Missing Keywords": ", ".join(jd_missing_keywords[:10]),
    #         "Suggestions": ", ".join(jd_improvement[:10])
    #     })

    #     st.subheader(f"📄 {resume_file.name}")
    #     st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
    #     st.markdown(f"- **Match Score:** {jd_score:.2f}%")
    #     st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
    #     st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:15])}`")
    #     st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

top_n = st.selectbox("Select Top N Resumes to Show", options=[1, 3, 5, 10, 15, 20], index=2)
min_score = st.selectbox("Minimum Match Score (%)", options=[0, 30, 50, 70, 80, 90, 100], index=2)

resume_scores = []
resume_texts = {}

# Step 1: Extract resume scores
for resume_file in resumes:
    resume_text = extract_text_from_file(resume_file)
    jd_score, _ = get_match_score(resume_text, jd_text)
    resume_scores.append((resume_file.name, jd_score))
    resume_texts[resume_file.name] = (resume_file, resume_text)

# Step 2: Apply filters from dropdown
filtered_scores = [(name, score) for name, score in resume_scores if score >= min_score]
top_filtered = sorted(filtered_scores, key=lambda x: x[1], reverse=True)[:top_n]

# Step 3: Show warning if no resumes match
if not top_filtered:
    st.warning("⚠️ No resumes meet the selected match score threshold.")
else:
    all_results = []
    all_resumes_data = []

    for i, (resume_name, jd_score) in enumerate(top_filtered, 1):
        resume_file, resume_text = resume_texts[resume_name]

        jd_suitable, jd_reasons = is_resume_suitable(resume_text, jd_role, role_skill_map)
        jd_missing_keywords = get_match_score(resume_text, jd_text)[1]
        jd_improvement = improvement_suggestions(resume_text, jd_role, role_skill_map)

        st.subheader(f"📄 {resume_name}")
        st.markdown(f"**🎯 JD Role Match: `{jd_role}`**")
        st.markdown(f"- **Match Score:** {jd_score:.2f}%")
        st.markdown(f"- **Suitable:** {'✅ Yes' if jd_suitable else '❌ No'}")
        st.markdown(f"- **Missing Keywords:** `{', '.join(jd_missing_keywords[:15])}`")
        st.markdown(f"- **Improvement Suggestions:** `{', '.join(jd_improvement[:10])}`")

        # Highlighting (optional)
        present, missing = highlight_missing_skills(resume_text, role_skill_map.get(jd_role, []))
        role_scores = []
        for role in role_skill_map:
            score, _ = get_match_score(resume_text, ' '.join(role_skill_map[role]))
            role_scores.append((role, score))

        top_roles = sorted(role_scores, key=lambda x: x[1], reverse=True)[:3]
        all_resumes_data.append({
            "filename": resume_name,
            "jd_score": jd_score,
            "top_roles": top_roles,
            "missing_keywords": jd_missing_keywords,
            "improvements": jd_improvement,
            "present_skills": present,
            "missing_skills": missing
        })

    # You can now continue with skill pie charts, summaries, and download buttons


        with st.expander(f"🔍 Try Other Role Matching for {resume_file.name}"):
            selected_role = st.selectbox(
                "Select another role to test suitability:",
                list(role_skill_map.keys()),
                key=f"role_select_{resume_file.name}"
            )

            if selected_role:
                alt_suitable, _ = is_resume_suitable(resume_text, selected_role, role_skill_map)
                alt_improvement = improvement_suggestions(resume_text, selected_role, role_skill_map)
                alt_score, alt_missing_keywords = get_match_score(resume_text, ' '.join(role_skill_map[selected_role]))

                st.markdown(f"### 🧪 Results for Selected Role: `{selected_role}`")
                st.markdown(f"- **Match Score:** {alt_score:.2f}%")
                st.markdown(f"- ✅ Suitable: {'Yes' if alt_suitable else 'No'}")
                st.markdown(f"- 💡 Suggestions: `{', '.join(alt_improvement[:10])}`")
                st.markdown(f"- 🔑 Missing Keywords: `{', '.join(alt_missing_keywords[:15])}`")

        with st.expander(f"🧠 Highlight Skills in Resume for `{jd_role}`"):
            present, missing = highlight_missing_skills(resume_text, role_skill_map.get(jd_role, []))
            highlighted = highlight_skills(resume_text, present)
            st.markdown("#### ✅ Present Skills Highlighted in Green")
            st.markdown(highlighted, unsafe_allow_html=True)
            st.markdown(f"#### ❌ Missing Skills:")
            st.markdown(f"{', '.join(missing[:20])}")

        # 🔍 NEW: Predict top 3 roles from resume (not JD)
        role_scores = []
        for role in role_skill_map:
            score, _ = get_match_score(resume_text, ' '.join(role_skill_map[role]))
            role_scores.append((role, score))

        role_scores_sorted = sorted(role_scores, key=lambda x: x[1], reverse=True)
        top_roles = role_scores_sorted[:3]

        st.markdown(f"### 🔮 Top 3 Predicted Roles from Resume:")
        for i, (role, score) in enumerate(top_roles, 1):
            st.markdown(f"{i}. **{role}** - `{score:.2f}%`")

        st.markdown("#### 📈 Role Suitability Prediction Chart")
        chart_df_roles = pd.DataFrame(role_scores_sorted, columns=["Role", "Score"])
        st.bar_chart(chart_df_roles.set_index("Role"))

        # 📝 Save for summary
        all_resumes_data.append({
            "filename": resume_file.name,
            "jd_score": jd_score,
            "top_roles": top_roles,
            "missing_keywords": jd_missing_keywords,
            "improvements": jd_improvement,
            "present_skills": present,
            "missing_skills": missing
        })

        st.markdown("---")

    # Show top 3 resumes
    # st.markdown("## 🏆 Top 3 Resumes by Score")
    # top_3 = sorted(resume_scores, key=lambda x: x[1], reverse=True)[:3]
    # for i, (name, score) in enumerate(top_3, 1):
    #     st.markdown(f"{i}. **{name}** - `{score:.2f}%`")

    # Show top N resumes after filtering by score
    # st.markdown(f"## 🏆 Top {top_n} Resumes by Score (Filtered by ≥ {min_score}%)")
    # filtered = [(name, score) for name, score in resume_scores if score >= min_score]
    # top_filtered = sorted(filtered, key=lambda x: x[1], reverse=True)[:top_n]

    # if not top_filtered:
    #     st.warning("⚠️ No resumes meet the selected match score threshold.")
    # else:
    #     for i, (name, score) in enumerate(top_filtered, 1):
    #         st.markdown(f"{i}. **{name}** - `{score:.2f}%`")

    # Show score chart
    st.markdown("## 📊 Match Score Comparison's For All Resumes...")
    chart_df = pd.DataFrame(resume_scores, columns=["Resume", "Score"])
    st.bar_chart(chart_df.set_index("Resume"))

    # Export to CSV
    result_df = pd.DataFrame(all_results)
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", data=csv, file_name="resume_analysis.csv", mime="text/csv")

    # Export to TXT Summary
    def generate_summary_txt(resume_data):
        summary = f"Resume: {resume_data['filename']}\n"
        summary += f"Match Score with JD: {resume_data['jd_score']:.2f}%\n"
        summary += f"Top Predicted Roles: {', '.join([role for role, _ in resume_data['top_roles']])}\n"
        summary += f"Missing Keywords: {', '.join(resume_data['missing_keywords'][:15])}\n"
        summary += f"Improvement Suggestions: {', '.join(resume_data['improvements'][:10])}\n"
        summary += f"Missing Skills: {', '.join(resume_data['missing_skills'][:20])}\n"
        return summary

    if st.button("📄 Download Summary Report (TXT)"):
        summaries = [generate_summary_txt(data) for data in all_resumes_data]
        summary_text = "\n\n---\n\n".join(summaries)
        st.download_button("📥 Download All Summaries", summary_text, "summary_report.txt")

    else:
       st.info("📌 Please upload both a job description and at least one resume.")

st.markdown("---")
st.markdown("<div style='text-align: center; color: green;'>Made by <strong> ❤️ Murali Krishna</strong> and  <strong>Jarvis AI </strong></div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 Made by **Murali Krishna** and **Jarvis AI...**")
 