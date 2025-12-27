from tools.similarity_tool import calculate_similarity

class JobMatchingAgent:
    def match(self, resume_text, job_description):
        score = calculate_similarity(resume_text, job_description)

        missing_skills = []
        jd_keywords = ["django", "rest", "sql", "api", "docker"]

        for skill in jd_keywords:
            if skill.lower() not in resume_text.lower():
                missing_skills.append(skill)

        return {
            "match_score": score,
            "missing_skills": missing_skills
        }
