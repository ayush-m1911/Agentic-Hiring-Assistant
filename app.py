import streamlit as st
from orchestrator import HiringOrchestrator

st.set_page_config(page_title="Agentic Hiring Assistant")

st.title("🧠 Agentic Hiring Assistant – Phase 3")

job_description = st.text_area("Paste Job Description")

resumes = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Evaluate Candidates"):
    if not resumes or not job_description:
        st.warning("Please upload resumes and job description.")
    else:
        orchestrator = HiringOrchestrator()
        results = orchestrator.process_inputs(resumes, job_description)

        st.subheader("📋 Hiring Decisions")

        for res in results:
            st.markdown(f"### {res['filename']}")
            st.write(f"**Match Score:** {res['match_score']}%")
            st.write(f"**Decision:** {res['decision']}")
            st.write(f"**Reason:** {res['reason']}")
            st.write(f"**Missing Skills:** {', '.join(res['missing_skills'])}")
