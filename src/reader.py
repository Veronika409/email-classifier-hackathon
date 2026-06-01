import os
class Email:
    def __init__(self, filepath, subject="", sender="", body=""):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.subject = subject
        self.sender = sender
        self.body = body
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

def read_all(inbox_path):
    emails = []
    
    if not os.path.exists(inbox_path):
        return emails
    
    for filename in os.listdir(inbox_path):
        if filename.startswith('.'):
            continue
            
        filepath = os.path.join(inbox_path, filename)
        if not os.path.isfile(filepath):
            continue
            
        try:
            data = read_email(filepath)
            email = Email(
                filepath=filepath,
                subject=data.get("subject", ""),
                sender=data.get("from_addr", ""),
                body=data.get("body", ""))
            emails.append(email)
        except Exception:
            email = Email(
                filepath=filepath,
                subject="",
                sender="",
                body=""
            )
            emails.append(email)
    
    return emails