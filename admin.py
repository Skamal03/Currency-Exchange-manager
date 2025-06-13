# admin_interface.py
from models import User, Currency, ExchangeRate
from manager import ExchangeManager

def admin_interface():
    manager = ExchangeManager()
    while True:
        print("\nAdmin Menu")
        print("1. Add User")
        print("2. Add Currency")
        print("3. Set Exchange Rate")
        print("4. View All Users")
        print("5. View Exchange Rates")
        print("6. View Transaction Summary")
        print("7. Top Currency Pair")
        print("8. Users Above Avg Transaction")
        print("9. View User Transaction History")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Name: ")
            email = input("Email: ")
            manager.add_user(User(name, email))
            print("User added.")
        elif choice == '2':
            code = input("Currency Code (e.g., USD): ").upper()
            name = input("Currency Name: ")
            manager.add_currency(Currency(code, name))
            print("Currency added.")
        elif choice == '3':
            from_currency = input("From Currency Code: ").upper()
            to_currency = input("To Currency Code: ").upper()
            rate = float(input("Exchange Rate: "))
            manager.set_exchange_rate(ExchangeRate(from_currency, to_currency, rate))
            print("Exchange rate set.")
        elif choice == '4':
            for user in manager.get_users():
                print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        elif choice == '5':
            for r in manager.get_exchange_rates():
                print(f"{r[0]} -> {r[1]}: {r[2]}")
        elif choice == '6':
            for row in manager.get_transaction_summary():
                print(f"User: {row[0]}, Email: {row[1]}, Total Exchanged: {row[2]}")
        elif choice == '7':
            result = manager.get_top_currency_pair()
            print(f"Top Pair: {result[0]} -> {result[1]}, Count: {result[2]}")
        elif choice == '8':
            users = manager.get_above_avg_users()
            for u in users:
                print(f"Name: {u[0]}, Email: {u[1]}")
        elif choice == '9':
            user_id = int(input("Enter User ID to view transaction history: "))
            if not manager.user_exists(user_id):
                print("User ID does not exist.")
            else:
                transactions = manager.get_user_transaction_history(user_id)
                for t in transactions:
                    print(
                        f"ID: {t[0]}, From: {t[1]}, To: {t[2]}, Amount: {t[3]}, Exchanged: {t[4]}, Rate: {t[5]}, Date: {t[6]}")
        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")
    manager.close()
