# models.py
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Currency:
    def __init__(self, code, name):
        self.code = code
        self.name = name

class ExchangeRate:
    def __init__(self, from_currency, to_currency, rate):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rate = rate

class Transaction:
    def __init__(self, user_id, from_currency, to_currency, amount, exchanged_amount, rate_used):
        self.user_id = user_id
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount
        self.exchanged_amount = exchanged_amount
        self.rate_used = rate_used