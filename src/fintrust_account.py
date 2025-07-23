from openpyxl import Workbook


class FinTrustBalanceException(Exception):
    pass

class CloseAccountException(Exception):
    def __init__(self, message = "This account is closed."):
        super().__init__(message)
        
        
class LockedAccountException(Exception):
    def __init__(self, message = "This account is locked."):
        super().__init__(message)


class FinTrustAccount:
    
    DAILY_WITHDRAW_LIMIT = 1000
    DAILY_INTEREST_RATE = 0.01  # 1% kamata.
    CONVERSION_RATES = {
        "USD": 1.0,
        "EUR": 0.93,
        "RSD": 110.0
    }
    

    def __init__(self,amount,person):
        self.balance = amount
        self.name = person
        self.active_account = True
        self.locked = False
        self.history_transaction = []
        self.failed_attempts = 0
        self.withdraw_today = 0
        self.daily_login_attempts = 0
        self.phone_number = None
        self.email = None
        self.fraud_attempts = False
        self.notes = []
        self.tags = set()
        self.login_status = False
        self.overdraft_limit = 0
        self.currency = "USD"
        self.language = "EN"
        self.security_question = None
        print(f"\nAccount '{self.name}' created.\nBalance = ${self.balance:.2f}")
    
    def check_active_account(self):
        if not self.active_account:
            raise CloseAccountException()
        if self.locked:
            raise LockedAccountException()
    
    def get_balance(self):
        self.check_active_account()
        converted = self.convert_rates(self.currency)
        print(f"\nAccount '{self.name}' balance = {converted:.2f} {self.currency}")
        
    def convert_rates(self, target_currency):
        if target_currency not in self.CONVERSION_RATES:
            raise ValueError(f"Unsupported currency: {target_currency}")
        convert = self.CONVERSION_RATES[target_currency] / self.CONVERSION_RATES[self.currency]
        return self.balance * convert
    
        
    def depo(self,amount):
        self.check_active_account()
        bonus = 0
        if amount > 1000:
            bonus = 50
            self.history_transaction.append(f"Bonus reward for large deposit: + $50.00")
        self.balance += amount + bonus
        self.history_transaction.append(f"Deposit: +${amount:.2f}")
        print(f"\nDeposit complete. {'Bonus applied!' if bonus else ''}")
        self.get_balance()

    def success_transaction(self,amount):
        self.check_active_account()
        if self.balance + self.overdraft_limit >= amount:
            return
        else:
            raise FinTrustBalanceException(f"\nSorry, account '{self.name}' only has a balance of ${self.balance:.2f} and overdraft limit ${self.overdraft_limit:.2f}")
    
    def withdraw_money(self,amount):
        try:
            if self.withdraw_today + amount > self.DAILY_WITHDRAW_LIMIT:
                raise Exception(f"\nWithdrawal exceeds daily limit of ${self.DAILY_WITHDRAW_LIMIT}.")
            self.success_transaction(amount)
            self.balance -= amount
            self.withdraw_today += amount
            self.history_transaction.append(f"Withdraw: -${amount:.2f}")
            print("\nWithdraw money complete.")
            self.get_balance()
            self.failed_attempts = 0
        except (FinTrustBalanceException, CloseAccountException , LockedAccountException) as error:
            self.failed_attempts += 1
            print(f'\nWithdraw money interrupted: {error}')
            if self.failed_attempts >= 3:
                self.locked = True
                print("Account locked due to multiple failed attempts.")
        
    def transfer_money(self,amount,account):
        try:
            self.check_active_account()
            account.check_active_account()
            print('\nIn Porgress...\n\nBeginning Transfer...')
            self.success_transaction(amount)
            self.withdraw_money(amount)
            account.depo(amount)
            self.history_transaction.append(f"Transfer to {account.name}: -${amount:.2f}")
            account.history_transaction.append(f"Transfer from {self.name}: +${amount:.2f}")
            print('\nTransfer complete.\n\nSUCCESS!')
            self.failed_attempts = 0
        except (FinTrustBalanceException, CloseAccountException, LockedAccountException) as error:
            self.failed_attempts += 1
            print(f'\nTransfer interrupted. {error}')
            if self.failed_attempts >= 3:
                self.locked = True
                print("Account locked due to multiple failed attempts.")
            
    def close_account(self):
        self.active_account = False
        self.history_transaction.append("Account closed.")
        print(f"\nAccount '{self.name}' has been closed.")
        
    def change_account_name(self,new_account_name):
        old_account_name = self.name
        self.name = new_account_name
        self.history_transaction.append(f"Account name changed from {old_account_name} to {new_account_name}")
        print(f"\nAccount name changed to '{self.name}'.")
        
        
    def export_history_to_excel(self):
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = f"{self.name} _History"
            ws.append(["Transaction History"])
            ws.append([""])
            for content in self.history_transaction:
                ws.append([content])
            filename = f"{self.name} _history_transaction.xlsx"
            wb.save(filename)
            print(f"\nHistory exported to Excel file '{filename}'.")
        except Exception as e:
            print(f"\nFailed to export history to Excel: {e}")
            
            
    def apply_daily_interest(self):
        if self.balance > 0:
            interest = self.balance * self.DAILY_INTEREST_RATE
            self.balance += interest
            self.history_transaction.append(f"Interest applied: + ${interest:.2f}")
            print(f"\nDaily interest of ${interest:.2f} added to '{self.name}'.")
            
    
    def set_currency(self, currency):
        if currency not in self.CONVERSION_RATES:
            raise ValueError("Unsupported currency.")

        if currency == self.currency:
            print(f"Currency already set to {currency}.")
            return
        
        old_balance = self.balance
        old_currency = self.currency
        self.balance = self.convert_rates(currency)
        self.currency = currency
        self.history_transaction.append(f"Currency changed from {old_currency} to {currency}. Balance adjusted from {old_balance:.2f} {old_currency} to {self.balance:.2f} {currency}.")
        print(f"Currency set to '{currency}' for '{self.name}'. Balance converted to {self.balance:.2f}{currency}.")
        
        
    def lock_account(self):
        self.locked = True
        self.history_transaction.append("Account manually locked.")
        print(f"\nAccount '{self.name}' has been locked.")
        
    def unlock_account(self):
        self.locked = False
        self.failed_attempts = 0
        self.history_transaction.append("Account manually unlocked.")
        print(f"\nAccount '{self.name}' has been unlocked.")
        
    
    def reset_account(self):
        self.balance = 0
        self.active_account = True
        self.locked = False
        self.failed_attempts = 0
        self.withdraw_today = 0
        self.history_transaction.clear()
        self.history_transaction.append("Account reset to default state.")
        print(f"\nAccount '{self.name}' has been reset.")
        
    def reset_daily_limit(self):
        self.withdraw_today = 0
        print(f"\nDaily withdrawal limit for '{self.name}' has been reset.")
        
    def set_contact_info(self,phone,email):
        self.phone_number = phone
        self.email = email
        print(f"\nContact info updated for '{self.name}'.")
        
    def fraud(self):
        self.fraud_attempts = True
        self.history_transaction.append("Fraud attempts on account.")
        print(f"\nFraud attempts alert on acount '{self.name}'.")
        
    def add_notes(self,note):
        self.notes.append(note)
        print(f"\nNote added to '{self.name}': {note}")
        
    def add_tags(self,tag):
        self.tags.add(tag)
        print(f"\nTag '{tag}' added to account '{self.name}'.")
        
    
    def show_history_transaction(self):
        print(f"\nTransaction history for '{self.name}':")
        if not self.history_transaction:
            print("No transactions yet.")
        else:
            for content in self.history_transaction:
                print(f" - {content}")
                
    def clear_all_history_transactions(self):
        self.history_transaction.clear()
        print(f"\nTransaction history for '{self.name}' cleared.")
     
    
    def login(self):
        self.login_status = True
        print(f"\nUser '{self.name}' is now logged in.")
        
    def logout(self):
        self.login_status = False
        print(f"\nUser '{self.name}' is now logged out.")
        
    def set_overdraft_limit(self,amount):
        self.overdraft_limit = amount
        print(f"\nOverdraft limit set to ${amount:.2f} for '{self.name}'.")
        
        
    def set_language(self,language):
        self.language = language
        print(f"\nLanguage preference set to '{language}' for '{self.name}'.")
        
    def set_security_question(self,question):
        self.security_question = question
        print(f"\nSecurity question set for '{self.name}'.")
        
    