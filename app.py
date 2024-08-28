# Import libraries
from flask import Flask, request, url_for, redirect, render_template
# Instantiate Flask functionality
app=Flask("This is a transaction application that have multple static webpages on server to redirect")
# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation
@app.route('/')
def get_transactions():
    return render_template("transactions.html",transactions=transactions)
# Create operation
@app.route("/add",methods = ["GET","POST"])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    elif request.method == "POST":
        date=request.form['date']
        amount=float(request.form['amount'])
        transaction={
         'id':len(transactions)+1,
         'date':date,
         'amount':amount
        }
        transactions.append(transaction)
        return redirect(url_for('get_transactions'))

# Update operation
@app.route("/edit/<int:transaction_id>",methods=["GET","POST"])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template("edit.html",transaction=transaction)
        # Implies transaction id is not found in the list of id
        return {"message": "Transaction id not found"}, 404
    elif request.method == "POST":
        date=request.form['date']
        amount=float(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
                
        # Redirecting to transactions list page
        return redirect(url_for('get_transactions'))   
        



# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
            if transaction['id'] == transaction_id:
                #we need to delete this transaction from list
                transactions.remove(transaction)
                break
    # Implies transaction id is not found in the list of id
    # Redirecting to transactions list page
    return redirect(url_for('get_transactions'))
# Run the Flask app
if __name__=="__main__":
    app.run(debug=True)
    