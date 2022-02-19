from datetime import datetime as dt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app= Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Accounts(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    account_no = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    date_created = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )
    transaction_details = db.Column(
        db.String(150),
        index=False,
        unique=False,
        nullable=False
    )
    value_date = db.Column(
        db.String(50),
        index=False,
        unique=False,
        nullable=False
    )
    withdrawal_amt = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False,
        default=0.0
    )
    deposit_amt = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False,
        default=0.0
    )
    balance_amt = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False,
        default=0.0
    )

    def __init__(self, account_no, date_created, transaction_details, value_date, withdrawal_amt, deposit_amt, balance_amt):
        self.account_no = account_no
        self.date_created = date_created
        self.transaction_details = transaction_details
        self.value_date = value_date
        self.withdrawal_amt = withdrawal_amt
        self.deposit_amt = deposit_amt
        self.balance_amt = balance_amt



@app.route('/')
def index():
    return "Hello, World!"

@app.route('/transactions/add', methods=['GET','POST'])
def add_transaction():
    if request.method == 'POST':
        account_no = request.form.get("account_no")
        if not account_no:
            return jsonify({"message":"Account number is required"}), 400
        date_created = request.form.get("date_created")
        if not date_created:
            return jsonify({"message":"Date is required"}), 400
        transaction_details =  request.form.get("transaction_details")
        if not transaction_details:
            return jsonify({"message":"Transaction details is required"}), 400
        value_date = request.form.get("value_date")
        if not value_date:
            return jsonify({"message":"Value date is required"}), 400
        withdrawal_amt =  request.form.get("withdrawal_amt")
        if not withdrawal_amt:
            return jsonify({"message":"Withdrawal amount is required"}), 400
        deposit_amt = request.form.get("deposit_amt")
        if not deposit_amt:
            return jsonify({"message":"Deposit amount is required"}), 400
        balance_amt = request.form.get("balance_amt")
        if not balance_amt:
            return jsonify({"message":"Balance amount is required"}), 400
        new_transaction = Accounts(account_no, date_created, transaction_details, value_date, withdrawal_amt, deposit_amt, balance_amt)
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction added successfully!'})
    return jsonify({'message': 'Something went wrong!'})

@app.route('/details/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Accounts.query.get(id)
    if transaction:
        return jsonify({'account_no': transaction.account_no, 'date_created': transaction.date_created, 'transaction_details': transaction.transaction_details, 'value_date': transaction.value_date, 'withdrawal_amt': transaction.withdrawal_amt, 'deposit_amt': transaction.deposit_amt, 'balance_amt': transaction.balance_amt})
    return jsonify({'message': 'No transaction found on this date'})

@app.route('/transactions/<date>', methods=['GET'])
def get_transaction_by_date(date):
    transaction = Accounts.query.filter_by(date_created=date).all()
    if transaction:
        result = []
        for transaction in transaction:
            result.append({'id': transaction.id, 'account_no': transaction.account_no, 'date_created': transaction.date_created, 'transaction_details': transaction.transaction_details, 'value_date': transaction.value_date, 'withdrawal_amt': transaction.withdrawal_amt, 'deposit_amt': transaction.deposit_amt, 'balance_amt': transaction.balance_amt})
        return jsonify(result)
    return jsonify({'message': 'No transaction found on this date'})

@app.route('/balance/<date>', methods=['GET'])
def get_balance_by_date(date):
    transactions = Accounts.query.filter_by(date_created=date).all()
    if transactions:
        result = []
        for transaction in transactions:
            result.append({'account_no': transaction.account_no, 'date_created': transaction.date_created, 'balance_amt': transaction.balance_amt})
        return jsonify(result)
    return jsonify({'message': 'No transaction found on this date'})

if __name__ == "__main__":
    app.run(port=3000,debug=True)


