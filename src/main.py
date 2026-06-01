import os
from reader import read_email
from classifier import classify

def process_inbox(inbox_path="data/inbox", outbox_path="data/outbox"):
    if not os.path.exists(inbox_path):
        print(f"Папка {inbox_path} не найдена")
        return
    files = [f for f in os.listdir(inbox_path) if f.endswith('.eml')]
    print(f"Найдено {len(files)} писем")
    for filename in files:
        filepath = os.path.join(inbox_path, filename)
        email_data = read_email(filepath)
        if "error" in email_data:
            print(f"Ошибка: {filename} - {email_data['error']}")
            continue
        category = classify(email_data)
        print(f"{filename} -> {category}")

if __name__ == "__main__":
    process_inbox()
