import uuid
import threading
from decimal import Decimal
from django.test import TransactionTestCase
from rest_framework.test import APIClient
from transaction.models import (User , Symbol , Wallet , TransactionLog)



class DepositRaceConditionTest(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            name = "Bita"
        )
        self.symbol = Symbol.objects.create(
            name = "BTC"
        )
        self.wallet = Wallet.objects.create(
            user = self.user , 
            symbol = self.symbol 
        )
    
    def make_deposit(self , amount):
        client = APIClient()  
        res = client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : str(self.wallet.wallet_id) , 
                "user_id" : str(self.user.user_id) , 
                "amount" : str(amount) , 
                "refrence_key" : str(uuid.uuid4())
            },
           
             format = "json"
        )
        print(res.data)
    def test_concurrent_deposits(self):
        threads = [] 
        numOfThreads = 10

        for _ in range(numOfThreads):
            thread = threading.Thread(
                target=self.make_deposit,
                args=(10,)
            )
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.wallet.refresh_from_db()
        
        print(self.wallet.balance)
        self.assertEqual(
            self.wallet.balance , 
            Decimal("100")
        )
        