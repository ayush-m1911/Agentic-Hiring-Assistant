import os
from dotenv import load_dotenv

from tools.pdf_loader import extract_text_from_pdf

from agents.resume_screening_agent import ResumeScreeningAgent
from agents.job_matching_agent import JobMatchingAgent
from agents.decision_agent import DecisionAgent
from agents.interview_question_agent import InterviewQuestionAgent
from agents.interview_scheduler_agent import InterviewSchedulerAgent
from agents.email_agent import EmailAgent
from agents.post_interview_decision_agent import PostInterviewDecisionAgent

load_dotenv()  # Loads EMAIL_ADDRESS and EMAIL_APP_PASSWORD


class HiringOrchestrator:
    """
    Central controller for the Agentic Hiring Assistant.
    Handles:
    - Resume screening & shortlisting
    - Interview scheduling (Google Meet)
    - Automated emails
    - Post-interview offer / rejection
    """

    def __init__(self):
       
        self.screening_agent = ResumeScreeningAgent()
        self.matching_agent = JobMatchingAgent()
        self.decision_agent = DecisionAgent()
        self.question_agent = InterviewQuestionAgent()

       
        self.scheduler_agent = InterviewSchedulerAgent()

    
        self.email_agent = EmailAgent(
            sender_email=os.getenv("EMAIL_ADDRESS"),
            sender_password=os.getenv("EMAIL_APP_PASSWORD")
        )

      
        self.post_interview_agent = PostInterviewDecisionAgent()

    # ======================================================
    # PRE-INTERVIEW PIPELINE
    # ======================================================
    def process_inputs(
        self,
        resumes,
        job_description,
        send_emails=False,
        interview_start=None,
        interview_end=None
    ):
        """
        Executes resume screening + interview scheduling workflow
        """

        results = []

        for resume in resumes:
            # 1️⃣ Extract resume text
            resume_text = extract_text_from_pdf(resume)

            # 2️⃣ Resume screening
            self.screening_agent.screen(resume_text)

            # 3️⃣ Resume ↔ Job matching
            match_result = self.matching_agent.match(
                resume_text,
                job_description
            )

            # 4️⃣ Hiring decision (INTERVIEW / REJECTED)
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

            # ⚠️ Placeholder (later auto-extracted from resume)
            candidate_email = "candidate@example.com"

            meeting_details = None

            # 6️⃣ Email + Interview scheduling
            if send_emails:
                if decision_result["decision"] == "REJECTED":
                    self.email_agent.send_rejection_email(candidate_email)

                elif decision_result["decision"] == "INTERVIEW":
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
                        self.email_agent.send_interview_shortlist_email(
                            candidate_email
                        )

            # 7️⃣ Collect results
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

    # ======================================================
    # POST-INTERVIEW PIPELINE
    # ======================================================
    def post_interview_action(
        self,
        candidate_email,
        final_status,
        role="Backend Developer",
        joining_date="To be discussed",
        ctc="As per company standards"
    ):
        """
        Executes post-interview workflow:
        - Offer email OR
        - Post-interview rejection email
        """

        decision = self.post_interview_agent.decide(final_status)

        if decision["action"] == "SEND_OFFER":
            self.email_agent.send_offer_email(
                receiver_email=candidate_email,
                role=role,
                joining_date=joining_date,
                ctc=ctc
            )

            return {
                "status": "OFFER_SENT",
                "candidate_email": candidate_email
            }

        else:
            self.email_agent.send_post_interview_rejection_email(
                receiver_email=candidate_email
            )

            return {
                "status": "POST_INTERVIEW_REJECTION_SENT",
                "candidate_email": candidate_email
            }
