# 💼 FinTrust - CLI Python Application

**FinTrust** is a command-line Python application that simulates a full-featured banking system. Designed for portfolio demonstration and practice with object-oriented programming (OOP), file persistence, testing, and user authentication.

---

## ✅ Key Features

### 🔐 User Management
- User registration and login
- Two-factor authentication via security question
- File-based persistence (`users.json`)

### 💸 Account Functionality
- Deposit, withdraw, and transfer funds
- Daily withdrawal limits
- Locking and unlocking accounts
- Closing and resetting accounts
- Custom exceptions for invalid operations

### 📈 Advanced Features
- Bonus for large deposits
- Transaction history tracking
- Export history to `.xlsx`
- Currency conversion (USD, EUR, RSD)
- Multi-step security: auto-lock after 3 failed attempts
- Configurable language/contact info

### 🧪 Testing
- Automated unit tests using `unittest`
- Test coverage for both `authentication` and `fintrust_account`
- Easy test discovery via `unittest discover`

---

## 📂 Folder Structure

```
FinTrust/
├── src/
│   ├── fintrust_account.py       # All bank account logic
│   ├── authentication.py         # User registration/authentication
│   ├── cli_app.py                # Main CLI interface
│
├── tests/
│   ├── test_fintrust_account.py # Tests for account features
│   ├── test_authentication.py   # Tests for user management
│
├── users.json                   # Stores all registered users
├── requirements.txt             # Python dependencies
├── README.txt                   # Project overview
```

---

## ▶️ Running the App

### 🔧 Setup
Install dependencies:
```bash
pip install -r requirements.txt
```

### 🏁 Start the CLI App
```bash
python src/cli_app.py
```

### 🧪 Run Tests
```bash
python -m unittest discover -s tests
```

---

## 🔄 Currency Conversion
Automatic currency conversion is applied when switching between supported currencies (USD, EUR, RSD) using predefined exchange rates.

---

## ⚙️ Future Extensions
- GUI version with Tkinter or PyQt
- SQLite/PostgreSQL integration
- Encrypted passwords (hashing)
- Admin user roles

---

## 📜 License
MIT License — free for personal, educational, and demo use.

---

## 👨‍💻 Author
Created by Ivan Djordjevic as a portfolio project to demonstrate full-stack Python application development and testing.
