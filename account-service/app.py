from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_NAME = "accounts.db"


# Create table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            );
        """
        )


init_db()


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.json
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (name, balance) VALUES (?, ?)",
            (data["name"], data["balance"]),
        )
        conn.commit()
        account_id = cursor.lastrowid
    return (
        jsonify({"id": account_id, "name": data["name"], "balance": data["balance"]}),
        201,
    )


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, balance FROM accounts WHERE id = ?", (account_id,)
        )
        row = cursor.fetchone()
    if row:
        return jsonify({"id": row[0], "name": row[1], "balance": row[2]})
    else:
        return "Account not found", 404


@app.route("/accounts", methods=["GET"])
def get_all_accounts():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM accounts")
        rows = cursor.fetchall()
    return jsonify([{"id": r[0], "name": r[1], "balance": r[2]} for r in rows])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
