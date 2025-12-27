from tools.pdf_loader import extract_text_from_pdf
from agents.resume_screening_agent import ResumeScreeningAgent
from agents.job_matching_agent import JobMatchingAgent

class HiringOrchestrator:
    def process_inputs(self, resumes, job_description):
        screening_agent = ResumeScreeningAgent()
        matching_agent = JobMatchingAgent()

        results = []

        for resume in resumes:
            resume_text = extract_text_from_pdf(resume)

            screened = screening_agent.screen(resume_text)
            match_result = matching_agent.match(
                resume_text, job_description
            )

            results.append({
                "filename": resume.name,
                "match_score": match_result["match_score"],
                "missing_skills": match_result["missing_skills"]
            })

        return results
