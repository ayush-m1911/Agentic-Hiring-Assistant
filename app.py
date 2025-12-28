import streamlit as st
from datetime import datetime, time
import sqlite3
from orchestrator import HiringOrchestrator

st.set_page_config(page_title="Agentic Hiring Assistant", layout="wide")

st.title("🧠 Agentic Hiring Assistant")
st.caption("End-to-end AI-assisted hiring system")

# ---------------- Job Description ----------------
st.subheader("📄 Job Description")
job_description = st.text_area("Paste job description", height=200)

# ---------------- Resume Upload ----------------
st.subheader("📂 Upload Resumes")
resumes = st.file_uploader(
    "Upload PDF resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# ---------------- Run Screening ----------------
if st.button("🚀 Run Resume Screening"):
    if not job_description.strip() or not resumes:
        st.warning("Please provide job description and resumes.")
    else:
        orchestrator = HiringOrchestrator()
        results = orchestrator.process_inputs(resumes, job_description)
        st.session_state["results"] = results
        st.success("Resume screening completed.")

# ---------------- Screening Results ----------------
if "results" in st.session_state:
    st.subheader("📊 Candidate Results")

    for res in st.session_state["results"]:
        with st.expander(f"📄 {res['filename']}"):
            st.write(f"**Email:** {res['candidate_email']}")
            st.write(f"**Score:** {res['match_score']}%")
            st.write(f"**Decision:** {res['decision']}")

            if res["decision"] == "INTERVIEW":
                st.markdown("### 🎤 Interview Questions")
                for i, q in enumerate(res["interview_questions"], 1):
                    st.write(f"{i}. {q}")

                st.markdown("### 🗓️ Schedule Interview")

                c1, c2, c3 = st.columns(3)
                with c1:
                    date = st.date_input("Date", key=f"d_{res['filename']}")
                with c2:
                    start = st.time_input("Start", value=time(10, 0), key=f"s_{res['filename']}")
                with c3:
                    end = st.time_input("End", value=time(11, 0), key=f"e_{res['filename']}")

                if st.button("📨 Schedule Interview", key=f"btn_{res['filename']}"):
                    orchestrator = HiringOrchestrator()
                    meeting = orchestrator.schedule_interview_for_candidate(
                        res["candidate_email"],
                        datetime.combine(date, start).isoformat(),
                        datetime.combine(date, end).isoformat()
                    )
                    st.success("Interview scheduled!")
                    st.write(f"🔗 Meet Link: {meeting['meet_link']}")

# =====================================================
# POST-INTERVIEW STATUS UPDATE SECTION
# =====================================================
st.markdown("---")
st.header("📌 Post-Interview Status Update")

conn = sqlite3.connect("hiring.db")
cursor = conn.cursor()

cursor.execute("""
SELECT email, resume_filename, status
FROM candidates
WHERE status IN ('INTERVIEW_SCHEDULED', 'INTERVIEWED')
""")
candidates = cursor.fetchall()
conn.close()

if not candidates:
    st.info("No interviewed candidates available for status update.")
else:
    candidate_map = {
        f"{email} ({filename})": email
        for email, filename, _ in candidates
    }

    selected_candidate = st.selectbox(
        "Select Candidate",
        list(candidate_map.keys())
    )

    final_status = st.radio(
        "Final Decision",
        ["SELECTED", "REJECTED"]
    )

    role = st.text_input("Role", value="Backend Developer")
    joining_date = st.text_input("Joining Date", value="To be discussed")
    ctc = st.text_input("CTC", value="As per company standards")

    if st.button("📨 Send Final Decision Email"):
        orchestrator = HiringOrchestrator()
        response = orchestrator.post_interview_action(
            candidate_email=candidate_map[selected_candidate],
            final_status=final_status,
            role=role,
            joining_date=joining_date,
            ctc=ctc
        )

        st.success(f"✅ {response} sent successfully!")

st.markdown("---")
st.caption("Final hiring decisions remain human-controlled.")
