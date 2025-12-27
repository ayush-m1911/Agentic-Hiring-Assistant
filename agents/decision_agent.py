class DecisionAgent:
    def decide(self, match_score, missing_skills):
        if match_score >= 70:
            decision = "INTERVIEW"
            reason = "Candidate meets resume screening criteria and is suitable for technical interview."
        else:
            decision = "REJECTED"
            reason = "Resume does not meet the minimum screening threshold."

        return {
            "decision": decision,
            "reason": reason,
            "risk_factors": missing_skills
        }
