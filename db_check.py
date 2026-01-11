import mysql.connector

CONFIG = dict(host="127.0.0.1", user="root", password="12345")
DB_NAME = "FaceRecognitionSystem"


def main():
    print("== MySQL connectivity test ==")
    try:
        conn = mysql.connector.connect(**CONFIG)
        print("Connected to MySQL server")
        cur = conn.cursor()
        cur.execute("SELECT VERSION()")
        print("Server version:", cur.fetchone()[0])
        cur.execute("SHOW DATABASES")
        dbs = [row[0] for row in cur.fetchall()]
        print("Databases:", dbs)
        conn.close()
    except Exception as e:
        print("Server connection error:", e)
        return

    # Try case-insensitive match
    matched_db = None
    for name in dbs:
        if name.strip().lower() == DB_NAME.lower():
            matched_db = name.strip()
            break
    if not matched_db:
        print(f"Database '{DB_NAME}' not found. Create it and the 'student' table.")
        return

    try:
        conn = mysql.connector.connect(database=matched_db, **CONFIG)
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]
        print("Tables:", tables)
        if "student" not in tables:
            print("Table 'student' not found in", DB_NAME)
            return
        cur.execute("DESCRIBE student")
        cols = cur.fetchall()
        print("student columns:")
        for c in cols:
            print(" -", c[0], c[1])
        cur.execute("SELECT COUNT(*) FROM student")
        count = cur.fetchone()[0]
        print("student rows:", count)
        cur.execute("SELECT Student_id, Name, Roll_No, Department FROM student LIMIT 5")
        rows = cur.fetchall()
        print("Sample:")
        for r in rows:
            print(r)
        conn.close()
        print("DB check complete.")
    except Exception as e:
        print("Database error:", e)


if __name__ == "__main__":
    main()
