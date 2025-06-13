#adduser
"INSERT INTO users (name, email) VALUES (%s, %s)", (user.name, user.email)


#addcurrency
"INSERT INTO currencies (code, name) VALUES (%s, %s)", (currency.code, currency.name)


#set exchange rate
"""INSERT INTO exchange_rates (from_currency, to_currency, rate)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE rate = VALUES(rate), last_updated = CURRENT_TIMESTAMP"""
    , (rate.from_currency, rate.to_currency, rate.rate)


#user_exist
"SELECT id FROM users WHERE id = %s", (user_id,)


#exchange_currency
"""INSERT INTO transactions (user_id, from_currency, to_currency,
    amount, exchanged_amount, rate_used)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    , (transaction.user_id, transaction.from_currency,
            transaction.to_currency, transaction.amount,
            transaction.exchanged_amount, transaction.rate_used)


#get_exchange_rates
"SELECT from_currency, to_currency, rate, last_updated FROM exchange_rates"


#get_users
"SELECT id, name, email FROM users"


#transaction_summary
"""SELECT name, email, total_exchanged FROM user_transaction_summary """


--------------view and joins---------------------------------
#create a user_transaction_summary
CREATE OR REPLACE VIEW user_transaction_summary AS
SELECT u.name, u.email, SUM(t.exchanged_amount) AS total_exchanged
FROM users u
JOIN transactions t ON u.id = t.user_id
GROUP BY u.id;


-------------Aggregate nested queries---------------------------
#Top_currencies
"""SELECT from_currency, to_currency, COUNT(*) AS count
   FROM transactions
   GROUP BY from_currency, to_currency
   ORDER BY count DESC
   LIMIT 1"""


#above average users
 """SELECT u.name, u.email FROM users u
    WHERE u.id IN (SELECT user_id FROM transactions
    GROUP BY user_id
    HAVING AVG(amount) > (SELECT AVG(amount)
    FROM transactions))"""