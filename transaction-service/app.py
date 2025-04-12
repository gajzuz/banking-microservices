from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock database
transactions = []

# URL of Account Service (internal Docker Compose service name!)
ACCOUNT_SERVICE_URL = "http://account_service:5001/accounts"


@app.route("/transactions", methods=["POST"])
def add_transaction():
    data = request.json
    account_id = data.get("account_id")
    amount = data.get("amount")
    tx_type = data.get("type")  # "deposit" or "withdrawal"

    # Get account info from Account Service
    response = requests.get(f"{ACCOUNT_SERVICE_URL}/{account_id}")
    if response.status_code != 200:
        return "Account not found", 404

    account = response.json()
    current_balance = account["balance"]

    if tx_type == "withdrawal" and amount > current_balance:
        return "Insufficient funds", 400

    # Update balance (mocked – not persisted in Account Service!)
    new_balance = (
        current_balance - amount
        if tx_type == "withdrawal"
        else current_balance + amount
    )

    transaction = {
        "id": len(transactions) + 1,
        "account_id": account_id,
        "type": tx_type,
        "amount": amount,
        "new_balance": new_balance,
    }
    transactions.append(transaction)
    return jsonify(transaction), 201


@app.route("/transactions", methods=["GET"])
def get_transactions():
    return jsonify(transactions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
