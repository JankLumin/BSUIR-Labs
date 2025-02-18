import psycopg2
import sys


def main():
    enable_protection = True
    if "--disable-protection" in sys.argv:
        enable_protection = False

    username = input("Введите имя пользователя: ")

    try:
        conn = psycopg2.connect(
            dbname="lab6", user="postgres", password="8025", host="localhost"
        )
        cur = conn.cursor()

        if enable_protection:
            query = "SELECT * FROM users WHERE username = %s"
            cur.execute(query, (username,))
        else:
            query = f"SELECT * FROM users WHERE username = '{username}'"
            cur.execute(query)

        rows = cur.fetchall()
        print("Результаты запроса:")
        for row in rows:
            print(row)

    except Exception as e:
        print("Ошибка:", e)
    finally:
        if "cur" in locals():
            cur.close()
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    main()

# ' OR '1'='1
