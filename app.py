import streamlit as st
from orchestrator import HiringOrchestrator

st.set_page_config(page_title="Agentic Hiring Assistant")

st.title("🧠 Agentic Hiring Assistant – Phase 4")

job_description = st.text_area("Paste Job Description")

resumes = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("Screen & Generate Interview Questions"):
    if not resumes or not job_description:
        st.warning("Please upload resumes and job description.")
    else:
        orchestrator = HiringOrchestrator()
        results = orchestrator.process_inputs(resumes, job_description)

        for res in results:
            st.markdown(f"## 📄 {res['filename']}")
            st.write(f"**Match Score:** {res['match_score']}%")
            st.write(f"**Decision:** {res['decision']}")
            st.write(f"**Reason:** {res['reason']}")

            if res["decision"] == "INTERVIEW":
                st.subheader("🎤 Suggested Interview Questions")
                for q in res["interview_questions"]:
                    st.write("•", q)
            else:
                st.info("Candidate not shortlisted for interview.")
