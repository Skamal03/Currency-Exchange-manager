# manager.py
from connection import get_connection

class ExchangeManager:
    def __init__(self):
        self.conn = get_connection()
        if not self.conn:
            raise Exception("Database connection failed")
        self.cursor = self.conn.cursor()

    def add_user(self, user):
        self.cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (user.name, user.email))
        self.conn.commit()

    def add_currency(self, currency):
        self.cursor.execute("INSERT INTO currencies (code, name) VALUES (%s, %s)", (currency.code, currency.name))
        self.conn.commit()

    def set_exchange_rate(self, rate):
        self.cursor.execute("""
            INSERT INTO exchange_rates (from_currency, to_currency, rate)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE rate = VALUES(rate), last_updated = CURRENT_TIMESTAMP
        """, (rate.from_currency, rate.to_currency, rate.rate))
        self.conn.commit()

    def user_exists(self, user_id):
        self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone() is not None

    def exchange_currency(self, transaction):
        if not self.user_exists(transaction.user_id):
            raise ValueError("User ID does not exist. Cannot proceed with transaction.")

        exchanged = transaction.amount * transaction.rate_used
        transaction.exchanged_amount = exchanged
        self.cursor.execute("""
            INSERT INTO transactions (user_id, from_currency, to_currency,
               amount, exchanged_amount, rate_used)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transaction.user_id, transaction.from_currency,
            transaction.to_currency, transaction.amount,
            transaction.exchanged_amount, transaction.rate_used
        ))
        self.conn.commit()
        return exchanged

    def get_exchange_rates(self):
        self.cursor.execute("SELECT from_currency, to_currency, rate, last_updated FROM exchange_rates")
        return self.cursor.fetchall()

    def get_users(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        return self.cursor.fetchall()

    def get_transaction_summary(self):
        self.cursor.execute("""
            SELECT name, email, total_exchanged FROM user_transaction_summary
        """)
        return self.cursor.fetchall()

    def get_user_transaction_history(self, user_id):
        self.cursor.execute("""
            SELECT t.id, t.from_currency, t.to_currency, t.amount, t.exchanged_amount, t.rate_used, t.date
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE u.id = %s
            ORDER BY t.date DESC""", (user_id,))
        return self.cursor.fetchall()

    def get_top_currency_pair(self):
        self.cursor.execute("""
            SELECT from_currency, to_currency, COUNT(*) AS count
            FROM transactions
            GROUP BY from_currency, to_currency
            ORDER BY count DESC
            LIMIT 1""")
        return self.cursor.fetchone()

    def get_above_avg_users(self):
        self.cursor.execute("""SELECT u.name, u.email
            FROM users u
            JOIN (
                SELECT user_id
                FROM transactions
                GROUP BY user_id
                HAVING AVG(amount) >= (
                SELECT AVG(amount) FROM transactions)) t ON u.id = t.user_id""")
        return self.cursor.fetchall()
    def close(self):
        self.cursor.close()
        self.conn.close()