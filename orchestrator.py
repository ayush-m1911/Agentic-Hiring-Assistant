import os
from dotenv import load_dotenv

from tools.pdf_loader import extract_text_from_pdf
from tools.email_extractor import extract_email

from agents.resume_screening_agent import ResumeScreeningAgent
from agents.job_matching_agent import JobMatchingAgent
from agents.decision_agent import DecisionAgent
from agents.interview_question_agent import InterviewQuestionAgent
from agents.interview_scheduler_agent import InterviewSchedulerAgent
from agents.email_agent import EmailAgent
from agents.post_interview_decision_agent import PostInterviewDecisionAgent

from db.database import (
    create_tables,
    upsert_candidate,
    update_interview_details,
    update_final_status
)

load_dotenv()


class HiringOrchestrator:

    def __init__(self):
        create_tables()

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

    def process_inputs(self, resumes, job_description):
        results = []

        for resume in resumes:
            resume_text = extract_text_from_pdf(resume)
            candidate_email = extract_email(resume_text)

            self.screening_agent.screen(resume_text)

            match_result = self.matching_agent.match(
                resume_text,
                job_description
            )

            decision_result = self.decision_agent.decide(
                match_result["match_score"],
                match_result["missing_skills"]
            )

            upsert_candidate(
                name=None,
                email=candidate_email if candidate_email else f"unknown_{resume.name}",
                resume_filename=resume.name,
                match_score=match_result["match_score"],
                missing_skills=",".join(match_result["missing_skills"]),
                status=decision_result["decision"]
            )

            interview_questions = []
            if decision_result["decision"] == "INTERVIEW":
                interview_questions = self.question_agent.generate_questions(
                    resume_text,
                    job_description,
                    match_result["missing_skills"]
                )

            results.append({
                "filename": resume.name,
                "candidate_email": candidate_email,
                "match_score": match_result["match_score"],
                "decision": decision_result["decision"],
                "reason": decision_result["reason"],
                "missing_skills": match_result["missing_skills"],
                "interview_questions": interview_questions
            })

        return results

    def schedule_interview_for_candidate(
        self,
        candidate_email,
        interview_start,
        interview_end
    ):
        meeting = self.scheduler_agent.schedule_interview(
            candidate_email=candidate_email,
            start_time=interview_start,
            end_time=interview_end
        )

        update_interview_details(
            email=candidate_email,
            interview_start=interview_start,
            interview_end=interview_end,
            meet_link=meeting["meet_link"]
        )

        self.email_agent.send_interview_email_with_meet(
            receiver_email=candidate_email,
            meet_link=meeting["meet_link"],
            start=meeting["start"],
            end=meeting["end"]
        )

        return meeting

    def post_interview_action(
        self,
        candidate_email,
        final_status,
        role,
        joining_date,
        ctc
    ):
        decision = self.post_interview_agent.decide(final_status)

        if decision["action"] == "SEND_OFFER":
            self.email_agent.send_offer_email(
                receiver_email=candidate_email,
                role=role,
                joining_date=joining_date,
                ctc=ctc
            )
            update_final_status(candidate_email, "SELECTED")
            return "OFFER_SENT"

        self.email_agent.send_post_interview_rejection_email(candidate_email)
        update_final_status(candidate_email, "REJECTED")
        return "POST_INTERVIEW_REJECTION_SENT"
