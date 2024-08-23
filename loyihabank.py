from abc import ABC, abstractmethod
from datetime import datetime


class AccountInterface(ABC):

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass


class BankAccount(AccountInterface):

    def __init__(self, number: int, name: str) -> None:
        self._account_number = number 
        self._owner_name = name
        self._balance = 0.0
        self._cash_back = 0.0
        self._history_transactions = []

    @property
    def account_number(self) -> int:
        return self._account_number

    @property
    def owner_name(self) -> str:
        return self._owner_name

    def deposit(self, amount: float) -> None:
        self._balance += amount
        self._history_transactions.append(f"deposit: {amount} on {datetime.now()}")
        with open("deposits.txt", "a+") as fl:
            fl.write(f"Ushbu shaxs: {self._owner_name} ushbu kunda: {datetime.now()} {amount} deposit qildi!\n\n")

    def withdraw(self, amount: float) -> None:
        if amount > self._balance:
            print("Hisobingizda yetarli mablag' mavjud emas!")
        else:
            self._balance -= amount
            self._cash_back += (amount / 100)
            self._history_transactions.append(f"withdraw: {amount} on {datetime.now()}")
            with open("withdraws.txt", "a+") as fl:
                fl.write(f"Ushbu shaxs: {self._owner_name} ushbu kunda: {datetime.now()} {amount} miqdorda pul yechdi!\n\n")

    def get_balance(self) -> float:
        return self._balance

    def show_cashback(self) -> float:
        return self._cash_back

    def withdraw_cashback(self) -> None:
        self._balance += self._cash_back
        self._history_transactions.append(f"Cashback: {self._cash_back} on {datetime.now()}")
        self._cash_back = 0
        print("Cashback balance ga o'tkazildi!")

    def show_transactions(self) -> list:
        return self._history_transactions

    def __str__(self) -> str:
        return f"No: {self._account_number}\nName: {self._owner_name}\nBalance: {self._balance}\nCashback: {self._cash_back}"


class BankManager:

    def __init__(self) -> None:
        self._accounts = []

    def create_account(self, acc_number: int, owner_name: str) -> BankAccount:
        for account in self._accounts:
            if account.account_number == acc_number:
                print("Bunday raqamli account oldindan mavjud")
                return None
        new_acc = BankAccount(acc_number, owner_name)
        self._accounts.append(new_acc)
        print("Akkount muvaffaqqiyatli yaratildi!")
        return new_acc

    def find_account(self, acc_number: int) -> BankAccount:
        for account in self._accounts:
            if account.account_number == acc_number:
                return account
        return None

    def transfer(self, from_account: BankAccount, to_account: BankAccount, amount: float) -> None:
        fr = self.find_account(from_account.account_number)
        to = self.find_account(to_account.account_number)

        if fr is None or to is None:
            print("Bunday account mavjud emas")
            return

        if from_account.get_balance() < amount:
            print("Hisobingizda yetarli mablag' mavjud emas!")
            return

        from_account.withdraw(amount)
        to_account.deposit(amount)
        print("Pul o'tkazildi!")

    def show_all_accounts(self) -> None:
        for i in self._accounts:
            print(f"{i.account_number} {i.owner_name} {i.get_balance()}")


if __name__ == "__main__":
    bankmam=BankManager()

    accat11=bankmam.create_account(1999, "Maknun")
    accat11.deposit(100)

    accat2 =bankmam.create_account(77752,"Mirzo")
    accat2.deposit(1000)
    bankmam.transfer(accat2, accat11, 936)

    print(accat2)
    print()
    print(accat11)

    print(f"1999-accountning to'lovlar tarixi:")
    print(accat11.show_transactions())

    print()


    print(f"77752-accountning to'lovlar tarixi:")
    print(accat2.show_transactions())