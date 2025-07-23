import json
import os
from src.fintrust_account import FinTrustAccount




class Users:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = self.load_users()
        
    def load_users(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename,"r") as file:
            data = json.load(file)
            users = {}
            for username,info in data.items():
                account = FinTrustAccount(info["balance"], username)
                account.set_security_question(info["security_question"])
                account.set_currency(info.get("currency", "USD"))
                account.set_overdraft_limit(info.get("overdraft_limit",0))
                users[username] = {
                    "password": info["password"],
                    "security_question": info["security_question"],
                    "security_answer": info["security_answer"],
                    "account": account
                } 
            return users
        
    def save_users(self):
        data = {}
        for username,info in self.users.items():
            acc = info["account"]
            data[username] = {
                "password": info["password"],
                "security_question": info["security_question"],
                "security_answer": info["security_answer"],
                "balance": acc.balance,
                "currency": acc.currency,
                "overdraft_limit": acc.overdraft_limit
            }
        with open(self.filename,"w") as file:
            json.dump(data,file,indent=4)
            
    
    def register_users(self,username,password,security_question,security_answer,initial_balance=0):
        if username in self.users:
            print(f"Username '{username}' already exists.")
            return None
        account = FinTrustAccount(initial_balance,username)
        account.set_security_question(security_question)
        self.users[username] = {
            "password": password,
            "security_question": security_question,
            "security_answer": security_answer.lower(),
            "account": account
        }
        self.save_users()
        print(f"User '{username}' registered successfully.")
        
    def login_users(self,username,password):
        user = self.users.get(username)
        if user and user["password"] == password:
            print(f"Security question: {user['security_question']}")
            answer = input("Answer: ").strip().lower()
            if answer == user["security_answer"]:
                print(f"Login successful. Welcome, {username}!")
                return user["account"]
            else:
                print("Incorrect answer to security question.")
                return None
        else:
            print("Login failed. Invalid username or password.")
            return None
        
    def list_users(self):
        print("\nRegistered users: ")
        for username in self.users:
            print(f" - {username}")    
    
            
        