class DecisionAgent:
    def decide(self, match_score, missing_skills):
        if match_score >= 70:
            decision = "INTERVIEW"
            reason = "Strong alignment with job requirements."
        else:
            decision = "REJECTED"
            reason = "Insufficient match with job requirements."

        return {
            "decision": decision,
            "reason": reason,
            "risk_factors": missing_skills
        }
