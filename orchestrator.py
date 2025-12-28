import os
from tools.pdf_loader import extract_text_from_pdf
from agents.resume_screening_agent import ResumeScreeningAgent
from agents.job_matching_agent import JobMatchingAgent
from agents.decision_agent import DecisionAgent
from agents.interview_question_agent import InterviewQuestionAgent
from agents.email_agent import EmailAgent

from dotenv import load_dotenv

load_dotenv()  # loads EMAIL_ADDRESS and EMAIL_APP_PASSWORD


class HiringOrchestrator:
    """
    Central controller that coordinates all agents
    """

    def __init__(self):
        # Initialize agents
        self.screening_agent = ResumeScreeningAgent()
        self.matching_agent = JobMatchingAgent()
        self.decision_agent = DecisionAgent()
        self.question_agent = InterviewQuestionAgent()

        # Initialize email agent securely
        self.email_agent = EmailAgent(
            sender_email=os.getenv("EMAIL_ADDRESS"),
            sender_password=os.getenv("EMAIL_APP_PASSWORD")
        )

    def process_inputs(self, resumes, job_description, send_emails=False):
        """
        Main hiring pipeline
        """
        results = []

        for resume in resumes:
            # 1️⃣ Extract resume text
            resume_text = extract_text_from_pdf(resume)

            # 2️⃣ Screen resume (structure / metadata)
            screened_data = self.screening_agent.screen(resume_text)

            # 3️⃣ Match resume with job description
            match_result = self.matching_agent.match(
                resume_text,
                job_description
            )

            # 4️⃣ Make hiring decision (INTERVIEW / REJECTED)
            decision_result = self.decision_agent.decide(
                match_result["match_score"],
                match_result["missing_skills"]
            )

            # 5️⃣ Generate interview questions (only if shortlisted)
            interview_questions = []
            if decision_result["decision"] == "INTERVIEW":
                interview_questions = self.question_agent.generate_questions(
                    resume_text,
                    job_description,
                    match_result["missing_skills"]
                )

            # ⚠️ TEMPORARY PLACEHOLDER
            # Later this will be extracted from resume
            candidate_email = "ayushmetkar138@gmail.com"

            # 6️⃣ Send emails if enabled
            if send_emails:
                if decision_result["decision"] == "REJECTED":
                    self.email_agent.send_rejection_email(candidate_email)

                elif decision_result["decision"] == "INTERVIEW":
                    self.email_agent.send_interview_shortlist_email(candidate_email)

            # 7️⃣ Collect results
            results.append({
                "filename": resume.name,
                "match_score": match_result["match_score"],
                "decision": decision_result["decision"],
                "reason": decision_result["reason"],
                "missing_skills": match_result["missing_skills"],
                "interview_questions": interview_questions
            })

        return results
