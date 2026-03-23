import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
load_dotenv()

class JobMatchingAgent:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
    def compute_similarity(self, resume_text, job_description):
        resume_embedding = self.model.encode([resume_text])
        jd_embedding = self.model.encode([job_description])

        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]

        return similarity
    def extract_skills(self, job_description):
     prompt = f"""
Extract key technical skills from this job description.

Return only a comma-separated list.

JD:
{job_description}
"""

     response = self.llm.invoke(prompt)
     skills = response.content.lower().split(",")

     return [s.strip() for s in skills]
    

    def match(self, resume_text, job_description):
        resume_lower = resume_text.lower()

        required_skills = self.extract_skills(job_description)

        matched_skills = [
            skill for skill in required_skills
            if skill in resume_lower
        ]

        skill_score = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0

        similarity = self.compute_similarity(resume_text, job_description)
        similarity_score = similarity * 100

        project_score = 100 if "project" in resume_lower else 50

        final_score = (
            0.5 * skill_score +
            0.3 * similarity_score +
            0.2 * project_score
        )

        return {
            "match_score": round(final_score, 2),
            "missing_skills": list(set(required_skills) - set(matched_skills))
        }