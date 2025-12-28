class PostInterviewDecisionAgent:
    def decide(self, final_status):
        """
        final_status: 'SELECTED' or 'REJECTED'
        """
        if final_status == "SELECTED":
            return {
                "action": "SEND_OFFER"
            }
        else:
            return {
                "action": "SEND_POST_INTERVIEW_REJECTION"
            }
