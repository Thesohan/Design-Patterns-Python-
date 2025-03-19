"""
Designing a Digital Wallet Service

Requirements

1. The digital wallet should allow users to create an account and manage their personal information.
2. Users should be able to add and remove payment methods, such as credit cards or bank accounts.
3. The digital wallet should support fund transfers between users and to external accounts. (Asumption--->external accounts as third party systems)
4. The system should handle transaction history and provide a statement of transactions.
5. The digital wallet should support multiple currencies and perform currency conversion --> assumption mapping available
6. The system should be scalable to handle a large number of users and transactions. ---> concurrency handling

a. Entities:


# User --> 

all attr that are in userRequest and userResponse
# userRequest

# userResponse:

    User
        --> id
        --> name
        --> mobile
        has accounts
        has payment_methods

        + add_account(account)
        + update_user(updated_user:userRequest) -- method overloading
        + add_payment_method(payment_method)
        + remove_payment_method(payment_method)

        
    Account
        ---> number
        has balance

        Wallet
        BankAccount

    PaymentMethod
       
        CreditCard
        BankAccount

    FundManager:
      --> responsible for fund transfer

      + fund_transfer(transaction)

    Account
    Transaction

    TransactionHistory
     + transactions

    Balance
      ---> amount
      ----> currency --> ENUM 
      
    Currency --> ENUM:
       INR
       USD
b. Relationship b/w entities
c. Runner --> 
d. APIs using which we can perform any action
"""

import uuid
from abc import ABC, abstractmethod
from enum import StrEnum
from datetime import datetime
import threading

class Currency(StrEnum):
    USD = "USD"
    INR = "INR"

currency_conversion = {
    Currency.USD:{Currency.INR:100},
    Currency.INR:{Currency.USD:0.01}
}

class Balance:
    
    def __init__(self,currency:Currency,amount:float=0.0):
        self.amount:float = amount
        self.currency:Currency = currency

class Account(ABC):
    
    def __init__(self,number:str,balance:Balance):
        self.number:str = number
        self.balance:Balance = balance
        self.lock = threading.Lock()

    @abstractmethod
    def get_account_type(self):
        pass

    def add_balance(self,amount:float,currency:Currency):
        with self.lock:
            if self.balance.currency == currency:
                self.balance.amount+=amount
            else:
                conversion_rate=currency_conversion.get(currency,{}).get(self.balance.currency)
                self.balance.amount += amount * conversion_rate
    
    def remove_balance(self,amount:float,currency:Currency):
        with self.lock:
            if self.balance.currency == currency:
                if self.balance.amount < amount:
                    raise ValueError("Insufficient balance")
                self.balance.amount-=amount
            else:
                conversion_rate=currency_conversion.get(currency,{}).get(self.balance.currency)
                if conversion_rate is None:
                    raise ValueError(f"Currency conversion rate not found from {currency} to {self.balance.currency}")
                converted_amount = amount * conversion_rate
                if self.balance.amount < converted_amount:
                    raise ValueError("Insufficient balance after currency conversion")
                self.balance.amount -= converted_amount
            

class Wallet(Account):
    
    def get_account_type(self):
        return 'Wallet'

class BankAccount(Account):

    def get_account_type(self):
        return 'BankAccount'
  
class PaymentMethod(ABC):

    def __init__(self,method_type:str,token:str)->None:
        self.id: str = str(uuid.uuid4())
        self.method_type: str = method_type
        self.created_at: datetime = datetime.now()
        self.token = token

    @abstractmethod
    def generate_token(self)->str:
        pass

    @abstractmethod
    def validate(self):
        pass        
    
class CreditCard(PaymentMethod):

    def __init__(self,last4digit:str,expiry_date:str,cardholder_name:str)->None:
        self.last4digit = last4digit
        self.expiry_date = expiry_date
        self.cardholder_name = cardholder_name
        super().__init__(method_type='CreditCard',token=self.generate_token())

    def generate_token(self)->str:
        token  = "aaxvadfgg534sddfg"
        return token

    def validate(self):
        pass

class BankAccountPaymentMethod(PaymentMethod):
    def __init__(self, account_number: str, bank_name: str, ifsc_code: str):
        self.account_number = account_number
        self.bank_name = bank_name
        self.ifsc_code = ifsc_code
        super().__init__(method_type='BankAccount',token=self.getnerate_token())

    def generate_token(self)->str:
        token  = "aaxvadfgg534sddfg"
        return token

    def validate(self) -> bool:
        """Simple validation for bank account"""
        if len(self.account_number) < 6:  # Basic length check
            return False
        if not self.ifsc_code or len(self.ifsc_code) != 11:  # IFSC code is typically 11 characters
            return False
        return True
    
class User:
    
    def __init__(self,name:str,mobile:str):
        self.id:str  = str(uuid.uuid4())
        self.name:str = name 
        self.mobile:str = mobile 
        self.accounts:dict[str,Account] = {}
        self.payment_methods: dict[str,PaymentMethod] = {}

    def add_account(self,account:Account):
        self.accounts[account.number] = account

    def remove_account(self,account_number:str):
        if account_number in self.accounts:
            del self.accounts[account_number]
        else:
            raise ValueError(f"account doesn't exist with number :{account_number}")  
    
    def update_user(self,user:"User"):
        self.name = user.name 
        self.mobile = user.mobile
    
    def add_payment_method(self,payment_method:PaymentMethod)->None:
        self.payment_methods[payment_method.id] = payment_method

    def remove_payment_method(self,payment_method_id:str)->None:
        if payment_method_id in self.payment_methods:
            del self.payment_methods[payment_method_id]
        else:
            raise ValueError(f"payment method doens't exist: {payment_method_id}")

class Transaction:
    def __init__(self, sender_id:str, receiver_id: str, amount: float, currency: Currency):
        self.id = str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.currency = currency 

    def __str__(self):
        return f'{self.id}, {self.sender_id}, {self.receiver_id},{self.amount},{self.currency}'

class FundManager:
    _instance = None
    _lock =threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.transactions = []
        return cls._instance
    
    def fund_transfer(self,sender: Account, receiver: Account, amount: float, currency: Currency,sender_user:User,receiver_user:User):
        if sender.balance.amount < amount:
            raise ValueError("Insufficient balance")
        transaction = Transaction(sender_id=sender_user.id,receiver_id=receiver_user.id,amount=amount,currency=currency)
        try:
            sender.remove_balance(amount, currency)
        except Exception as e:
            return
        try:
            receiver.add_balance(amount, currency)
        except Exception as e:
            sender.add_balance(amount=amount,currency=currency)
            return 
        self.transactions.append(transaction)
        print(f"Transferred {amount} {currency} from {sender.number} to {receiver.number}")

    def get_transactions(self,user:User)->list[Transaction]:
        user_transactions = []
        for transaction in self.transactions:
            if transaction.sender_id == user.id or transaction.receiver_id == user.id:
                user_transactions.append(transaction)
        return user_transactions
    
    @classmethod
    def get_instance(cls)->"FundManager":
        return FundManager()
if __name__ == "__main__":
    
    sohan = User(name="sohan",mobile="8126583671")
    amit = User(name="amit",mobile="9876543213")
    sohan_wallet = Wallet(number="1234566",balance=Balance(currency=Currency.INR,amount=100))
    sohan.add_account(account=sohan_wallet)
    sohan.add_account(account=BankAccount(number="1234566",balance=Balance(currency=Currency.INR,amount=100)))
    sohan.add_payment_method(payment_method=CreditCard(last4digit='6543',expiry_date="2024-01-01",cardholder_name="sohan"))
    amit_wallet = Wallet(number="4244566",balance=Balance(currency=Currency.INR,amount=0))
    amit.add_account(account=amit_wallet)

    FundManager.get_instance().fund_transfer(sender_user=sohan,receiver_user=amit, sender=sohan_wallet,receiver=amit_wallet,amount=50,currency=Currency.INR)
    print(FundManager.get_instance().get_transactions(sohan)[0])
    print(FundManager.get_instance().get_transactions(amit)[0])
