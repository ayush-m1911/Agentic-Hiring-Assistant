import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


class InterviewQuestionAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_questions(self, resume_text, job_description, missing_skills):
        prompt = f"""
You are a technical interviewer.

Generate 9-11 high-quality interview questions based on:

1. Candidate Resume:
{resume_text[:2000]}

2. Job Description:
{job_description[:1500]}

3. Missing Skills:
{', '.join(missing_skills)}

Guidelines:
- Mix conceptual and practical questions
- Focus on job requirements
- Include at least 2 questions targeting missing skills
- Avoid generic questions
- Keep questions concise

Return only a numbered list of questions.
"""

        response = self.llm.invoke(prompt)

        output = response.content.strip().split("\n")

        questions = [q.strip() for q in output if q.strip()]

        return questions