import os
from flask import Flask, jsonify
import pymysql

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "preoday_api_tests")
DB_USER = os.getenv("DB_USER", "preoday")
DB_PASS = os.getenv("DB_PASS", "preoday")

app = Flask(__name__)

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        connect_timeout=2,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/health")
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 as ok")
                row = cur.fetchone()
        return jsonify(status="UP", db=row["ok"]), 200
    except Exception as e:
        return jsonify(status="DOWN", error=str(e)), 503

@app.get("/init-db")
def init_db():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS transactions ("
                    "id BIGINT PRIMARY KEY AUTO_INCREMENT,"
                    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                    "amount DECIMAL(12,2) DEFAULT 0.00"
                    ")"
                )
            conn.commit()
        return jsonify(message="DB initialized"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/txn")
def new_txn():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO transactions(amount) VALUES(1.23)")
            conn.commit()
        return jsonify(message="txn ok"), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/stats")
def stats():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) as total FROM transactions")
                total = cur.fetchone()["total"]
        return jsonify(total_transactions=total), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
