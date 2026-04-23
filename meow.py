import sqlite3

db_path = r'C:\myproject\fastapi\fastapi_app\src\infrastructure\sqlite\database.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Проверяем, есть ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if not cursor.fetchone():
        print("❌ Таблица 'users' не существует в базе данных!")
        print("   Нужно создать таблицы через metadata.create_all()")
        conn.close()
        exit(1)
    
    # Получаем пользователей
    cursor.execute("SELECT id, login, password FROM users")
    users = cursor.fetchall()
    
    if not users:
        print("❌ Нет пользователей в базе данных!")
        print("   Нужно создать пользователя через API регистрации")
    else:
        print(f"Найдено {len(users)} пользователей:\n")
        for user_id, login, password in users:
            print(f"ID: {user_id}")
            print(f"Login: {login}")
            print(f"Password hash: {repr(password)}")
            print(f"Длина хеша: {len(password) if password else 0}")
            
            if password:
                print(f"Первые 20 символов: {password[:20]}")
                
                # Определяем тип хеша
                if password.startswith('$argon2'):
                    print("✅ Тип: ARGON2 - ПРАВИЛЬНО")
                elif password.startswith('$2a') or password.startswith('$2b') or password.startswith('$2y'):
                    print("✅ Тип: BCRYPT - ПРАВИЛЬНО")
                elif len(password) == 64 and all(c in '0123456789abcdef' for c in password.lower()):
                    print("❌ Тип: PLAIN SHA256 - НЕПРАВИЛЬНО (нужен argon2 или bcrypt)")
                elif len(password) < 30:
                    print("❌ Тип: ВОЗМОЖНО ПРОСТОЙ ТЕКСТ - НЕПРАВИЛЬНО")
                else:
                    print("❌ Тип: НЕИЗВЕСТНЫЙ - НЕПРАВИЛЬНО")
            print("-" * 50)
    
    conn.close()
    
except FileNotFoundError:
    print(f"❌ Файл базы данных не найден: {db_path}")
    print("   База данных еще не создана")
except Exception as e:
    print(f"❌ Ошибка: {e}")