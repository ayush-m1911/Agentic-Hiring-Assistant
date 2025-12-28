import os
from dotenv import load_dotenv

from tools.pdf_loader import extract_text_from_pdf
from agents.resume_screening_agent import ResumeScreeningAgent
from agents.job_matching_agent import JobMatchingAgent
from agents.decision_agent import DecisionAgent
from agents.interview_question_agent import InterviewQuestionAgent
from agents.email_agent import EmailAgent
from agents.interview_scheduler_agent import InterviewSchedulerAgent

load_dotenv()  # Load EMAIL_ADDRESS and EMAIL_APP_PASSWORD


class HiringOrchestrator:
    """
    Central brain of the Agentic Hiring Assistant.
    Coordinates all agents and controls the hiring workflow.
    """

    def __init__(self):
        # ---------- Core Agents ----------
        self.screening_agent = ResumeScreeningAgent()
        self.matching_agent = JobMatchingAgent()
        self.decision_agent = DecisionAgent()
        self.question_agent = InterviewQuestionAgent()

        # ---------- Communication Agent ----------
        self.email_agent = EmailAgent(
            sender_email=os.getenv("EMAIL_ADDRESS"),
            sender_password=os.getenv("EMAIL_APP_PASSWORD")
        )

        # ---------- Scheduling Agent ----------
        self.scheduler_agent = InterviewSchedulerAgent()

    def process_inputs(
        self,
        resumes,
        job_description,
        send_emails=False,
        interview_start=None,
        interview_end=None
    ):
        """
        Executes the full hiring pipeline.

        Parameters:
        - resumes: uploaded PDF files
        - job_description: JD text
        - send_emails: bool (human-in-the-loop)
        - interview_start: ISO datetime string
        - interview_end: ISO datetime string
        """

        results = []

        for resume in resumes:
            # 1️⃣ Extract resume text
            resume_text = extract_text_from_pdf(resume)

            # 2️⃣ Resume screening
            screened_data = self.screening_agent.screen(resume_text)

            # 3️⃣ Resume ↔ Job matching
            match_result = self.matching_agent.match(
                resume_text,
                job_description
            )

            # 4️⃣ Hiring decision
            decision_result = self.decision_agent.decide(
                match_result["match_score"],
                match_result["missing_skills"]
            )

            # 5️⃣ Interview question generation
            interview_questions = []
            if decision_result["decision"] == "INTERVIEW":
                interview_questions = self.question_agent.generate_questions(
                    resume_text,
                    job_description,
                    match_result["missing_skills"]
                )

            # ⚠️ Placeholder (later extracted from resume)
            candidate_email = "candidate@example.com"

            meeting_details = None

            # 6️⃣ Interview scheduling + email sending
            if send_emails:
                if decision_result["decision"] == "REJECTED":
                    self.email_agent.send_rejection_email(candidate_email)

                elif decision_result["decision"] == "INTERVIEW":
                    # Schedule interview ONLY if date & time are provided
                    if interview_start and interview_end:
                        meeting_details = self.scheduler_agent.schedule_interview(
                            candidate_email=candidate_email,
                            start_time=interview_start,
                            end_time=interview_end
                        )

                        self.email_agent.send_interview_email_with_meet(
                            receiver_email=candidate_email,
                            meet_link=meeting_details["meet_link"],
                            start=meeting_details["start"],
                            end=meeting_details["end"]
                        )
                    else:
                        # Fallback: shortlist email without scheduling
                        self.email_agent.send_interview_shortlist_email(candidate_email)

            # 7️⃣ Collect final structured result
            results.append({
                "filename": resume.name,
                "match_score": match_result["match_score"],
                "decision": decision_result["decision"],
                "reason": decision_result["reason"],
                "missing_skills": match_result["missing_skills"],
                "interview_questions": interview_questions,
                "meeting_details": meeting_details
            })

        return results
