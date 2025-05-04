from connection import get_connection

class ExchangeManager:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def add_user(self, user):
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        self.cursor.execute(query, (user.name, user.email))
        self.conn.commit()

    def add_currency(self, currency):
        query = "INSERT INTO currencies (code, name) VALUES (%s, %s)"
        self.cursor.execute(query, (currency.code, currency.name))
        self.conn.commit()

    def set_exchange_rate(self, rate):
        query = """INSERT INTO exchange_rates (from_currency, to_currency, rate)
                   VALUES (%s, %s, %s)"""
        self.cursor.execute(query, (rate.from_currency, rate.to_currency, rate.rate))
        self.conn.commit()

    def exchange(self, transaction):
        exchanged = transaction.amount * transaction.rate_used
        transaction.exchanged_amount = exchanged
        query = """INSERT INTO transactions (user_id, from_currency, to_currency,
                   amount, exchanged_amount, rate_used)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(query, (
            transaction.user_id, transaction.from_currency,
            transaction.to_currency, transaction.amount,
            transaction.exchanged_amount, transaction.rate_used
        ))
        self.conn.commit()

    def get_rates(self):
        self.cursor.execute("SELECT * FROM exchange_rates")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
