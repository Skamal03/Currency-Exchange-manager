# user_interface.py
from models import User, Transaction
from manager import ExchangeManager

def user_interface():
    manager = ExchangeManager()
    while True:
            print("\nUser Menu")
            print("1. Exchange Currency")
            print("2. View Exchange Rates")
            print("0. Exit")

            choice = input("Choose an option: ")

            if choice == '1':
                user_id = int(input("User ID: "))
                from_currency = input("From Currency: ").upper()
                to_currency = input("To Currency: ").upper()
                amount = float(input("Amount: "))
                rate_used = float(input("Exchange Rate: "))
                transaction = Transaction(user_id, from_currency, to_currency, amount, 0, rate_used)
                exchanged = manager.exchange_currency(transaction)
                print(f"Exchanged {amount} {from_currency} to {exchanged:.2f} {to_currency}")

            elif choice == '2':
                for r in manager.get_exchange_rates():
                    print(f"{r[0]} -> {r[1]}: {r[2]}")

            elif choice == '0':
                break
            else:
                print("Invalid choice. Try again.")
    manager.close()
