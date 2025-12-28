import re

def extract_email(text):
    """
    Extracts first valid email address from resume text
    """
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    matches = re.findall(email_pattern, text)

    if matches:
        return matches[0]  # Return first email found
    return None
