import streamlit as st
from datetime import datetime, time
from orchestrator import HiringOrchestrator

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Agentic Hiring Assistant",
    layout="wide"
)

# ---------------------------------
# Title
# ---------------------------------
st.title("🧠 Agentic Hiring Assistant")
st.caption(
    "End-to-end AI-assisted hiring system with interview scheduling, "
    "Google Meet integration, and automated candidate communication"
)

# ---------------------------------
# Job Description
# ---------------------------------
st.subheader("📄 Job Description")
job_description = st.text_area(
    "Paste the job description here",
    height=200
)

# ---------------------------------
# Resume Upload
# ---------------------------------
st.subheader("📂 Upload Candidate Resumes (PDF)")
resumes = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------------------------
# Interview Scheduling Inputs
# ---------------------------------
st.subheader("🗓️ Interview Scheduling (For Shortlisted Candidates)")

col1, col2, col3 = st.columns(3)

with col1:
    interview_date = st.date_input("Interview Date")

with col2:
    start_time = st.time_input("Start Time", value=time(10, 0))

with col3:
    end_time = st.time_input("End Time", value=time(11, 0))

# Convert to ISO datetime strings
interview_start = None
interview_end = None

if interview_date and start_time and end_time:
    interview_start = datetime.combine(
        interview_date, start_time
    ).isoformat()

    interview_end = datetime.combine(
        interview_date, end_time
    ).isoformat()

# ---------------------------------
# Email Automation Control
# ---------------------------------
st.subheader("✉️ Email Automation")
send_emails = st.checkbox(
    "Send emails automatically (Rejection / Interview with Google Meet)",
    help="Enable only after testing with your own email"
)

# ---------------------------------
# Run Hiring Pipeline
# ---------------------------------
if st.button("🚀 Run Hiring Pipeline"):
    if not job_description.strip():
        st.warning("Please provide a job description.")
    elif not resumes:
        st.warning("Please upload at least one resume.")
    elif send_emails and (interview_start is None or interview_end is None):
        st.warning("Please select interview date and time before sending emails.")
    else:
        orchestrator = HiringOrchestrator()

        with st.spinner("Processing candidates..."):
            results = orchestrator.process_inputs(
                resumes=resumes,
                job_description=job_description,
                send_emails=send_emails,
                interview_start=interview_start,
                interview_end=interview_end
            )

        st.success("Hiring pipeline completed successfully!")

        # ---------------------------------
        # Display Results
        # ---------------------------------
        st.subheader("📊 Candidate Evaluation Results")

        for res in results:
            with st.expander(f"📄 {res['filename']}"):
                st.write(f"**Candidate Email:** {res.get('candidate_email', 'Not found')}")
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

                    if res["meeting_details"]:
                        st.markdown("### 🔗 Interview Scheduled")
                        st.write(
                            f"**Google Meet Link:** {res['meeting_details']['meet_link']}"
                        )
                        st.write(
                            f"**Start:** {res['meeting_details']['start']}"
                        )
                        st.write(
                            f"**End:** {res['meeting_details']['end']}"
                        )
                else:
                    st.info("Candidate not shortlisted for interview.")

# =====================================================
# POST-INTERVIEW FINAL DECISION SECTION
# =====================================================
st.markdown("---")
st.header("📌 Post-Interview Final Decision")

st.info(
    "Use this section after interviews are completed to send "
    "offer or post-interview rejection emails."
)

with st.form("post_interview_form"):
    candidate_email = st.text_input(
        "Candidate Email",
        placeholder="candidate@example.com"
    )

    final_status = st.radio(
        "Final Interview Outcome",
        ["SELECTED", "REJECTED"]
    )

    role = st.text_input(
        "Role",
        value="Backend Developer"
    )

    joining_date = st.text_input(
        "Joining Date",
        value="To be discussed"
    )

    ctc = st.text_input(
        "CTC / Compensation",
        value="As per company standards"
    )

    submit_final_decision = st.form_submit_button(
        "📨 Send Final Decision Email"
    )

if submit_final_decision:
    if not candidate_email:
        st.warning("Please enter candidate email.")
    else:
        orchestrator = HiringOrchestrator()

        with st.spinner("Sending final decision email..."):
            response = orchestrator.post_interview_action(
                candidate_email=candidate_email,
                final_status=final_status,
                role=role,
                joining_date=joining_date,
                ctc=ctc
            )

        st.success(
            f"✅ {response['status']} for {response['candidate_email']}"
        )

# ---------------------------------
# Footer
# ---------------------------------
st.markdown("---")
st.caption(
    "⚠️ This system assists recruiters across the hiring lifecycle. "
    "Final hiring decisions must always involve human judgment."
)
