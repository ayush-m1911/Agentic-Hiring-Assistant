import streamlit as st
from orchestrator import HiringOrchestrator

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Agentic Hiring Assistant",
    layout="wide"
)

# -----------------------------
# App Title
# -----------------------------
st.title("🧠 Agentic Hiring Assistant")
st.caption(
    "AI-powered system for resume screening, interview shortlisting, "
    "and automated candidate communication"
)

# -----------------------------
# Job Description Input
# -----------------------------
st.subheader("📄 Job Description")
job_description = st.text_area(
    "Paste the job description here",
    height=200
)

# -----------------------------
# Resume Upload
# -----------------------------
st.subheader("📂 Upload Candidate Resumes (PDF)")
resumes = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# -----------------------------
# Email Control
# -----------------------------
st.subheader("✉️ Email Automation")
send_emails = st.checkbox(
    "Send emails automatically (Rejection / Interview Shortlist)",
    help="Enable only after testing with your own email"
)

# -----------------------------
# Run Pipeline
# -----------------------------
if st.button("🚀 Run Hiring Pipeline"):
    if not job_description.strip():
        st.warning("Please provide a job description.")
    elif not resumes:
        st.warning("Please upload at least one resume.")
    else:
        orchestrator = HiringOrchestrator()

        with st.spinner("Analyzing resumes..."):
            results = orchestrator.process_inputs(
                resumes=resumes,
                job_description=job_description,
                send_emails=send_emails
            )

        st.success("Hiring pipeline completed successfully!")

        # -----------------------------
        # Display Results
        # -----------------------------
        st.subheader("📊 Candidate Evaluation Results")

        for res in results:
            with st.expander(f"📄 {res['filename']}"):
                st.write(f"**Match Score:** {res['match_score']}%")
                st.write(f"**Decision:** {res['decision']}")
                st.write(f"**Reason:** {res['reason']}")

                if res["missing_skills"]:
                    st.write(
                        f"**Missing Skills:** {', '.join(res['missing_skills'])}"
                    )
                else:
                    st.write("**Missing Skills:** None")

                if res["decision"] == "INTERVIEW":
                    st.markdown("### 🎤 Suggested Interview Questions")
                    for idx, q in enumerate(res["interview_questions"], start=1):
                        st.write(f"{idx}. {q}")
                else:
                    st.info("Candidate not shortlisted for interview.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    "⚠️ This system assists recruiters in screening and communication. "
    "Final hiring decisions should always involve human review."
)
