import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailAgent:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, receiver_email, subject, body):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))
        # server la connect kr ani mail send kr #
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password) #app password use kr for security purposes#
            server.send_message(msg)

    def send_rejection_email(self, receiver_email):
        subject = "Application Update"
        body = (
            "Dear Candidate,\n\n"
            "Thank you for your interest in our organization.\n"
            "After careful review, we will not be moving forward with your application at this stage.\n\n"
            "We appreciate your time and wish you success in your future endeavors.\n\n"
            "Kind regards,\n"
            "Hiring Team"
        )
        self.send_email(receiver_email, subject, body)

    def send_interview_shortlist_email(self, receiver_email):
        subject = "Interview Shortlisting – Next Steps"
        body = (
            "Dear Candidate,\n\n"
            "Thank you for applying to our organization.\n"
            "After reviewing your profile, we are pleased to inform you that you have been shortlisted "
            "for the next stage of the interview process.\n\n"
            "Further interview details will be shared shortly.\n\n"
            "Best regards,\n"
            "Hiring Team"
        )
        self.send_email(receiver_email, subject, body)

    def send_interview_email_with_meet(self, receiver_email, meet_link, start, end):
         subject = "Interview Scheduled – Google Meet"

         body = (
        "Dear Candidate,\n\n"
        "Your interview has been scheduled.\n\n"
        f"📅 Start: {start}\n"
        f"⏰ End: {end}\n"
        f"🔗 Google Meet Link: {meet_link}\n\n"
        "Please be available on time.\n\n"
        "Best regards,\n"
        "Hiring Team"
    )

         self.send_email(receiver_email, subject, body)

    def send_offer_email(self, receiver_email, role, joining_date, ctc):
        subject = f"Offer Letter – {role}"

        body = (
        f"Dear Candidate,\n\n"
        f"We are pleased to inform you that you have been selected for the role of {role}.\n\n"
        f"Offer Details:\n"
        f"- Role: {role}\n"
        f"- Joining Date: {joining_date}\n"
        f"- Compensation: {ctc}\n\n"
        f"The formal offer letter will be shared shortly.\n\n"
        f"Best regards,\n"
        f"Hiring Team"
    )

        self.send_email(receiver_email, subject, body)


    def send_post_interview_rejection_email(self, receiver_email):
        subject = "Interview Outcome"

        body = (
        "Dear Candidate,\n\n"
        "Thank you for taking the time to interview with us.\n"
        "After careful consideration, we regret to inform you that "
        "we will not be proceeding further with your application.\n\n"
        "We appreciate your effort and wish you success in your future endeavors.\n\n"
        "Kind regards,\n"
        "Hiring Team"
    )

        self.send_email(receiver_email, subject, body)
