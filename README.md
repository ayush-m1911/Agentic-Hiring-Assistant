# 🧠 Agentic Hiring Assistant (Agentic ATS)

An end-to-end **AI-assisted Applicant Tracking System (ATS)** that automates resume screening, interview scheduling with Google Meet, candidate communication, and lifecycle tracking — while keeping **final hiring decisions under human control**.

---

## 🚀 Project Overview

Recruitment is often time-consuming due to:
- Manual resume screening
- Repetitive candidate communication
- Interview scheduling overhead
- Lack of centralized candidate tracking

This project solves these problems by introducing an **agentic AI-based hiring assistant** that supports recruiters across the entire hiring lifecycle.

📌 **AI assists — humans decide.**

---

## ✨ Key Features

- 📄 Resume parsing from PDF
- 📧 Automatic email extraction from resumes
- 🧠 AI-based resume–job matching with score
- ⚖️ Rule-based shortlisting (Interview / Reject)
- 🎤 Personalized interview question generation
- 🗓️ Per-candidate interview scheduling
- 🔗 Automatic Google Meet link creation
- ✉️ Automated emails (shortlist, rejection, offer)
- 🗂️ Candidate database with status tracking
- 📌 Post-interview decision update from UI
- 👨‍💼 Human-in-the-loop ethical hiring

---

## 🧩 System Architecture

```text
Streamlit UI
     ↓
Hiring Orchestrator
     ↓
------------------------------------------------
| Resume Agent | Matching Agent | Decision Agent |
| Interview Agent | Email Agent | DB Layer      |
------------------------------------------------
     ↓
Google Calendar API | SMTP | SQLite
