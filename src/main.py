import os
import shutil
from reader import read_email
from classifier import classify

# Расширения, которые точно являются письмами
EMAIL_EXTENSIONS = {'.txt', '.eml', '.msg'}

# Расширения, которые точно НЕ являются письмами
BINARY_EXTENSIONS = {'.jpeg', '.jpg', '.png', '.gif', '.bmp', '.bin', '.exe', '.dll', '.pdf', '.docx', '.xlsx', '.zip', '.rar', '.7z', '.json', '.xml', '.html', '.css', '.js'}

def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()

def process_inbox(inbox_path="data/inbox", outbox_path="data/outbox", unknown_path="data/unknown"):
    """
    Обрабатывает все файлы из папки inbox:
    - Письма (текстовые форматы) → читает, классифицирует, перемещает в outbox/категория
    - Бинарные файлы → перемещает в unknown/
    - Нечитаемые файлы → перемещает в unknown/
    """
    
    # Создаём все нужные папки
    os.makedirs(outbox_path, exist_ok=True)
    os.makedirs(unknown_path, exist_ok=True)
    
    if not os.path.exists(inbox_path):
        print(f"❌ Папка {inbox_path} не найдена")
        return
    
    files = os.listdir(inbox_path)
    print(f"📁 Найдено файлов: {len(files)}")
    print("-" * 50)
    
    stats = {
        "processed": 0,      # успешно обработанных писем
        "unsupported": 0,    # бинарные форматы
        "errors": 0,         # ошибки чтения
        "by_category": {}    # статистика по категориям
    }
    
    for filename in files:
        filepath = os.path.join(inbox_path, filename)
        ext = get_file_extension(filename)
        
        # 1. Явно бинарные файлы — сразу в unknown
        if ext in BINARY_EXTENSIONS:
            print(f"🖼️ {filename} -> НЕ ПИСЬМО (бинарный формат {ext})")
            shutil.move(filepath, os.path.join(unknown_path, filename))
            stats["unsupported"] += 1
            continue
        
        # 2. Пробуем прочитать как письмо
        email_data = read_email(filepath)
        
        if "error" in email_data:
            # Нечитаемый файл — в unknown
            print(f"⚠️ {filename} -> НЕ ПИСЬМО (ошибка: {email_data['error'][:50]})")
            shutil.move(filepath, os.path.join(unknown_path, filename))
            stats["errors"] += 1
            continue
        
        # 3. Успешно прочитали — классифицируем
        category = classify(email_data)
        print(f"📧 {filename} -> {category}")
        
        # Собираем статистику по категориям
        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
        
        # Перемещаем в папку категории
        category_path = os.path.join(outbox_path, category)
        os.makedirs(category_path, exist_ok=True)
        shutil.move(filepath, os.path.join(category_path, filename))
        stats["processed"] += 1
    
    # Выводим итоговую статистику
    print("-" * 50)
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print(f"✅ Обработано писем: {stats['processed']}")
    print(f"🖼️ Неподдерживаемые форматы: {stats['unsupported']}")
    print(f"⚠️ Ошибки чтения: {stats['errors']}")
    
    if stats["by_category"]:
        print("\n📂 По категориям:")
        for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
            print(f"   {cat}: {count}")
    
    return stats

if __name__ == "__main__":
    process_inbox()