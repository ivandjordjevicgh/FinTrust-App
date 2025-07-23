from src.authentication import Users

manager = Users()
current_account = None

def register_user():
    print("\n---- REGISTER ----")
    username = input("Username: ")
    password = input("Password: ")
    question = input("Security question (e.g. What was the model of your first mobile phone?): ")
    answer = input("Answer: ")
    try:
        initial = float(input("Initial deposit: "))
    except ValueError:
        print("Invalid amount.")
        return
    manager.register_users(username,password,question,answer,initial)
    
    
def login_user():
    global current_account
    print("\n---- LOGIN ----")
    username = input("Username: ")
    password = input("Password: ")
    account = manager.login_users(username,password)
    if account:
        current_account = account
        
def account_menu():
    global current_account
    while current_account:
        print("""
---- ACCOUNT MENU ----
1. View Balance
2. Deposit
3. Withdraw    
4. Transfer
5. Export to Excel
6. Reset Account
7. Lock/Unlock Account
8. Set Currency
9. Apply Interest Rate
10. Logout
------------------------    
              """)
        
        choice = input("Choose option: ")
        
        if choice == "1":
            current_account.get_balance()
        elif choice == "2": 
            try:
                amt = float(input("Amount to deposit: "))
                current_account.depo(amt)
            except ValueError:
                print("Invalid amount.")
        elif choice == "3":
            try:
                amt = float(input("Amount to withdraw: "))
                current_account.withdraw_money(amt)
            except ValueError:
                print("Invalid amount.")
        elif choice == "4":
            to_user = input("Transfer to username: ")
            try:
                amt = float(input("Amount to transfer: "))
                to_acc = manager.users.get(to_user,{}).get("account")
                if to_acc:
                    current_account.transfer_money(amt,to_acc)
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid amount.")
        elif choice == "5":
            current_account.export_history_to_excel()
        elif choice == "6":
            current_account.reset_account()
        elif choice == "7":
            if current_account.locked:
                current_account.unlock_account()
            else:
                current_account.lock_account()
        elif choice == "8":
            cur = input("Set new currency (USD,EUR,RSD): ")
            try:
                current_account.set_currency(cur)
            except ValueError as e:
                print(e)
        elif choice == "9":
            current_account.apply_daily_interest()
        elif choice == "10":
            current_account.logout()
            current_account = None
        else:
            print("Invalid choice.")
            

def main():
    while True:
        print("""
------ MAIN MENU ------
1. Register
2. Login
3. Exit
-----------------------
              """)
        choice = input("Choose option: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
            if current_account:
                account_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            
            
if __name__ == "__main__":
    main()