# main.py

import os
import sys

from PyQt6.QtWidgets import QApplication
from database.db_manager import DBManager, safe_add_column
from utils.system_info import SystemInfo
from ui.main_window import MainWindow

def init_database():
    db = DBManager()
    cursor = db.cursor
    

    # Инициализация схемы, если нет таблицы rooms
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'"
    )
    if not cursor.fetchone():
        print("Выполняется инициализация схемы из schema.sql")
        with open("database/schema.sql", "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        db.conn.commit()

    # Миграции: новые колонки
    safe_add_column("fixed_expenses", "credit_limit REAL")
    safe_add_column("fixed_expenses", "is_credit_card BOOLEAN DEFAULT 0")
    safe_add_column("operations",       "transaction_id TEXT")
    safe_add_column("archived_operations", "transaction_id TEXT")
    safe_add_column("fixed_expenses", "is_closed INTEGER DEFAULT 0")

    db.close()

def load_stylesheet(style_filename: str) -> str:
    """Вернёт содержимое QSS-файла, лежащего рядом с main.py в папке ui/styles."""
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "ui", "styles", style_filename)
    if not os.path.exists(path):
        print(f"⚠️ Стиль не найден по пути: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    init_database()
    ADD_STYLE = True 
    APP_VERSION = "ver: T1.1"  
    app = QApplication(sys.argv)

    # загружаем стиль
    if ADD_STYLE:
        qss = load_stylesheet("style.qss")
        if qss:
            app.setStyleSheet(qss)
            print("✅ Стиль загружен")

    # системная информация
    sys_info = SystemInfo()
    print(f"Detected system: {sys_info}")

    is_mobile = False
    window = MainWindow(system_info=sys_info, mobile_mode=is_mobile, version=APP_VERSION)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

