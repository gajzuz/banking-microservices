const accountAPI = "http://localhost:5001/accounts";
const transactionAPI = "http://localhost:5002/transactions";

function createAccount() {
  const name = document.getElementById("name").value;
  const balance = parseFloat(document.getElementById("balance").value);

  fetch(accountAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, balance })
  })
  .then(res => res.json())
  .then(data => alert("Account created: " + JSON.stringify(data)));
}

function loadAccounts() {
  fetch(accountAPI)
    .then(res => res.json())
    .then(accounts => {
      const list = document.getElementById("accountList");
      list.innerHTML = "";
      accounts.forEach(a => {
        const li = document.createElement("li");
        li.innerText = `ID: ${a.id}, Name: ${a.name}, Balance: €${a.balance}`;
        list.appendChild(li);
      });
    });
}

function createTransaction() {
  const account_id = parseInt(document.getElementById("tx_account_id").value);
  const type = document.getElementById("tx_type").value;
  const amount = parseFloat(document.getElementById("tx_amount").value);

  fetch(transactionAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ account_id, type, amount })
  })
  .then(res => res.json())
  .then(data => alert("Transaction created: " + JSON.stringify(data)));
}

function loadTransactions() {
  fetch(transactionAPI)
    .then(res => res.json())
    .then(txs => {
      const list = document.getElementById("transactionList");
      list.innerHTML = "";
      txs.forEach(t => {
        const li = document.createElement("li");
        li.innerText = `Account: ${t.account_id}, Type: ${t.type}, Amount: €${t.amount}, New Balance: €${t.new_balance}`;
        list.appendChild(li);
      });
    });
}
