import unittest
from src.fintrust_account import FinTrustAccount, FinTrustBalanceException, CloseAccountException, LockedAccountException


class TestFinTrustAccount(unittest.TestCase):
    def setUp(self):
        self.acc = FinTrustAccount(1000, "TestUser")
        
    def test_initial_balance(self):
        self.assertEqual(self.acc.balance, 1000)
        
    def test_depo(self):
        self.acc.depo(500)
        self.assertGreater(self.acc.balance, 1000)
        
    def test_withdraw_success(self):
        self.acc.withdraw_money(200)
        self.assertEqual(self.acc.balance, 800)
        
    def test_withdraw_over_balance(self):
        with self.assertRaises(FinTrustBalanceException):
            self.acc.withdraw_money(2000)
            
    def test_transfer(self):
        target_account = FinTrustAccount(500, "TargetUser")
        self.acc.transfer_money(300, target_account)
        self.assertEqual(self.acc.balance, 700)
        self.assertEqual(target_account.balance, 800)
        
    def test_close_account(self):
        self.acc.close_account()
        with self.assertRaises(CloseAccountException):
            self.acc.get_balance()
            
    def test_lock_unlock_account(self):
        self.acc.lock_account()
        with self.assertRaises(LockedAccountException):
            self.acc.get_balance()
        self.acc.unlock_account()
        self.acc.get_balance() # should work now
        
    def test_currency_conversion(self):
        usd_value = self.acc.convert_rates("USD")
        eur_value = self.acc.convert_rates("EUR")
        rsd_value = self.acc.convert_rates("RSD")
        self.assertNotEqual(usd_value, eur_value, rsd_value)
        
if __name__ == "__main__":
    unittest.main()