import psycopg2
import sys

DB_CONFIG = {
    "host": "db",
    "database": "transactions",
    "user": "postgres",
    "password": "1",
    "port": "5432"
}

def seed_data():
    print("Начало заполнения базы данных")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO "Transactions_status" (name) 
            VALUES ('Бизнес'), ('Личное'), ('Налог')
            ON CONFLICT DO NOTHING;
        """)

        cursor.execute("""
            INSERT INTO "Transactions_type" (name) 
            VALUES ('Пополнение'), ('Списание')
            ON CONFLICT DO NOTHING
            RETURNING id, name;
        """)
        types = {name: id for id, name in cursor.fetchall()}

        categories = [
            ("Финансы", types['Пополнение'], ["Криптовалюта", "Банкинг"]),
            ("Маркетинг", types['Списание'], ["Farpost", "Avito"]),
            ("Инфраструктура", types['Списание'], ["VPS", "Proxy"])
        ]

        for cat_name, type_id, subcats in categories:
            cursor.execute("""
                INSERT INTO "Transactions_category" (name, type_id) 
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                RETURNING id;
            """, (cat_name, type_id))
            
            if cursor.rowcount > 0:
                cat_id = cursor.fetchone()[0]
                for subcat in subcats:
                    cursor.execute("""
                        INSERT INTO "Transactions_subcategory" (name, category_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (subcat, cat_id))

        conn.commit()
        print("Данные успешно загружены")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    seed_data()