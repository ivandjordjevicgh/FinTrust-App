import unittest
import os
from src.authentication import Users


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_users.json"
        self.manager = Users(filename=self.test_file)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_register_and_login_success(self):
        self.manager.register_users("ivan", "ivan123", "Favourite color?", "blue", 500)
        account = self.manager.users["ivan"]["account"]
        self.assertEqual(account.name, "ivan")
        self.assertEqual(account.balance, 500)
        
    def test_register_duplicate_username(self):
        self.manager.register_users("zeljko", "zeljko123","Pet?", "dog", 300)
        result = self.manager.register_users("zeljko", "newpass", "Pet?", "dog", 300)
        self.assertIsNone(result)
        
    def test_login_fail_wrong_pass(self):
        self.manager.register_users("aleksa", "aleksa123", "Food?", "chicken", 100)
        account = self.manager.login_users("aleksa", "wrong")
        self.assertIsNone(account)
        
    def test_login_fail_unknown_user(self):
        account = self.manager.login_users("noneexistent", "1234")
        self.assertIsNone(account)
        
    def test_user_file_persistence(self):
        self.manager.register_users("jovan","mypass","City?", "London", 700)
        new_manager = Users(filename=self.test_file)
        self.assertIn("jovan", new_manager.users)
        self.assertEqual(new_manager.users["jovan"]["account"].balance, 700)
        
if __name__ == "__main__":
    unittest.main()