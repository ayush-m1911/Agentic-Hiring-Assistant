import streamlit as st
from orchestrator import HiringOrchestrator

st.set_page_config(page_title="Agentic Hiring Assistant")

st.title("🧠 Agentic Hiring Assistant ")

job_description = st.text_area("Paste Job Description")

resumes = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Analyze"):
    if not resumes or not job_description:
        st.warning("Please upload resumes and job description.")
    else:
        orchestrator = HiringOrchestrator()
        results = orchestrator.process_inputs(resumes, job_description)

        st.subheader("📊 Candidate Match Results")
        for res in results:
            st.markdown(f"### {res['filename']}")
            st.write(f"**Match Score:** {res['match_score']}%")
            st.write(f"**Missing Skills:** {', '.join(res['missing_skills'])}")
