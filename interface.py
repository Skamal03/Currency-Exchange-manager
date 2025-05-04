from classes import User, Currency, ExchangeRate, Transaction
from currency_exchange import ExchangeManager

def main():
    manager = ExchangeManager()
    while True:
        print("\nCurrency Exchange Manager")
        print("1. Add User")
        print("2. Add Currency")
        print("3. Set Exchange Rate")
        print("4. Exchange Currency")
        print("5. View Exchange Rates")
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
            user_id = int(input("User ID: "))
            from_currency = input("From Currency: ").upper()
            to_currency = input("To Currency: ").upper()
            amount = float(input("Amount: "))
            rate_used = float(input("Rate: "))
            transaction = Transaction(user_id, from_currency, to_currency, amount, 0, rate_used)
            manager.exchange(transaction)
            print(f"Exchanged {amount} {from_currency} to {transaction.exchanged_amount} {to_currency}")
        elif choice == '5':
            rates = manager.get_rates()
            for r in rates:
                print(f"{r[0]} -> {r[1]}: {r[2]}")

        elif choice == '0':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
