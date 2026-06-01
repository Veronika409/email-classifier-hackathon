import os
from email import policy
from email.parser import BytesParser

def read_email(filepath):
    result = {"subject": "", "from_addr": "", "body": "", "filepath": filepath}
    try:
        with open(filepath, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        result["subject"] = msg.get("Subject", "")
        result["from_addr"] = msg.get("From", "")
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    result["body"] = part.get_content()
                    break
        else:
            result["body"] = msg.get_content()
    except Exception as e:
        result["error"] = str(e)
    return result
