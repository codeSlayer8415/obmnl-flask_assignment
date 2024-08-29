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
    balance=0
    for transaction in transactions:
        balance+=transaction['amount']
    return render_template("transactions.html",transactions=transactions,balance=balance)

#Search Transactions (Read operation)

@app.route('/search',methods=["GET","POST"])
def search_transactions():
    if request.method == "POST":
        min_amount=float(request.form['min_amount'])
        max_amount=float(request.form['max_amount'])
        filtered_transactions=[]
        for transaction in transactions:
            # check if transaction amount is in specified range
            if (transaction['amount'] >= min_amount) and (transaction['amount'] <= max_amount):
                filtered_transactions.append(transaction)
        # now all the filtered list is present, now we return this using all transaction template
        return render_template("transactions.html",transactions=filtered_transactions)
    # This is in case of get request , we just return a form template for max and min amounts
    return render_template("search.html")


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

#Operations that calculate total balance
@app.route('/balance')
def total_balance():
    balance=0
    for transaction in transactions:
        balance+=transaction['amount']
    #finally displaying balance in string format
    return f"Total balance after all the transactions is :{balance}"

# Run the Flask app
if __name__=="__main__":
    app.run(debug=True)
    