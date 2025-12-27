class InterviewQuestionAgent:
    def generate_questions(self, resume_text, job_description, missing_skills):
        questions = []

        # Resume-based depth questions
        if "django" in resume_text.lower():
            questions.append(
                "Can you explain how Django ORM works and how you optimize database queries?"
            )

        if "project" in resume_text.lower():
            questions.append(
                "Pick one project from your resume and explain the technical challenges you faced."
            )

        # Skill-gap based questions
        for skill in missing_skills:
            questions.append(
                f"You seem to have limited exposure to {skill}. How would you approach learning and applying it in a real project?"
            )

        # Job-role alignment question
        questions.append(
            "How does your previous experience align with the responsibilities mentioned in this job role?"
        )

        return questions
