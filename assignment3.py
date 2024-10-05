import random
from abc import ABC, abstractmethod

existing_account_numbers = []

def generate_account_number():
    new_account_number = random.randint(1000, 9999)

    while new_account_number in existing_account_numbers:
        new_account_number = random.randint(1000, 9999)
    existing_account_numbers.append(new_account_number)

    return new_account_number

def display_largest_account(accounts_list):
    if not Account.list_accounts:
        return "No accounts available."
    
    largest_balance = max(account.balance for account in Account.list_accounts)
    largest_accounts = [account for account in Account.list_accounts if account.balance == largest_balance]
    
    result = ""
    for index, account in enumerate(largest_accounts, start=1):
        result += account.display_info() + "\n"
    
    if len(largest_accounts) == 1:
        result += "There is one account with the largest balance."
    else:
        result += f"There are {len(largest_accounts)} accounts with the largest balance."
    return result.strip()

def display_oldest_account(accounts_list):
    if not Account.list_accounts:
        return "No accounts available."
    
    oldest_date = min(account.open_date for account in Account.list_accounts)
    oldest_accounts = [account for account in Account.list_accounts if account.open_date == oldest_date]
    
    result = ""
    for index, account in enumerate(oldest_accounts, start=1):
        result += account.display_info() + "\n"
    
    result += f"There are {len(oldest_accounts)} oldest accounts."
    return result.strip()

class Account(ABC):
    list_accounts = []

    def __init__(self, name, open_date, balance):
        self.account_number = generate_account_number()
        self.name = name
        self.open_date = open_date
        self.balance = balance
        Account.list_accounts.append(self)

    def withdraw(self, amount):
        if amount > self.balance:
            return f"${amount} Amount invalid.\nAvailable balance: ${self.balance}"
        self.balance -= amount
        return f"${amount} withdrawn.\nNew balance: ${self.balance}"
    
    def deposit(self, amount):
        if amount <= 0:
            return "Amount invalid."
        self.balance += amount
        return f"${amount} deposited.\nBalance: ${self.balance}"

    @abstractmethod
    def display_info(self):
        pass


class SavingsAccount(Account):
    def __init__(self, name, open_date, balance, interest_rate):
        super().__init__(name, open_date, balance)
        self.interest_rate = interest_rate
    
    def display_info(self):
        return (f"Saving account number: {self.account_number}\n"
                f"Name: {self.name}\n"
                f"Open date: {self.open_date}\n"
                f"Interest rate: {self.interest_rate}\n"
                f"Balance: ${self.balance}")

        
class CheckingAccount(Account):
    def __init__(self, name, open_date, balance):
        super().__init__(name, open_date, balance)

    def display_info(self):
        return (f"Checking account number: {self.account_number}\n"
                f"Name: {self.name}\n"
                f"Open date: {self.open_date}\n"
                f"Balance: ${self.balance}")

if __name__ == "__main__":
    s1 = SavingsAccount("Emma Smith", "2022-04-03", 550, 0.1)
    print(s1.display_info())

    c1 = CheckingAccount("Jackson Johnson", "2021-07-27", 300)
    c2 = CheckingAccount("Charlie Lee", "2021-07-27", 500)

    print(c1.display_info())
    print("")
    print(s1.withdraw(1000))
    print("")
    print(s1.withdraw(50))
    print("")
    print(c1.deposit(40))
    print("")
    print(c1.deposit(-100))
    print("")
    
    print(display_largest_account(Account.list_accounts))
    print(display_oldest_account(Account.list_accounts))