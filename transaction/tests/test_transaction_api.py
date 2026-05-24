from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
import uuid

from transaction.models import(User , Symbol , Wallet , TransactionLog)

class DepositApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            name = "Bita"
        )
        self.symbol = Symbol.objects.create(
            name = "BTC"
        )
        self.wallet = Wallet.objects.create(
            user=self.user,
            symbol=self.symbol,
           
        )
    def test_deposit_one_time_success(self):
        refrenceKey = uuid.uuid4()
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "80" , 
                "refrence_key" : refrenceKey
            } ,
            format="json"
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
        res.data["data"]["balance"],
        Decimal("80.00")
        )
        self.assertEqual(
        Wallet.objects.get(wallet_id = self.wallet.wallet_id).balance , 
        Decimal("80")
        )
        self.assertTrue(res.data["success"])
        self.assertEqual(
            TransactionLog.objects.count() , 
            1
        )
    def test_withdraw_one_time_success(self):
        
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "100" , 
                "refrence_key" : uuid.uuid4()
            } ,
            format="json"
        )
        res1 = self.client.post(
            "/api/wallet/withdraw/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "32.6" , 
                "refrence_key" : uuid.uuid4()
            } ,
            format="json"
        )
        
        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
        res1.data["data"]["balance"],
        Decimal("67.4")
        )
        self.assertEqual(
        Wallet.objects.get(wallet_id = self.wallet.wallet_id).balance , 
        Decimal("67.4")
        )
        self.assertTrue(res1.data["success"])
        self.assertEqual(
            TransactionLog.objects.count() , 
            2
        )
    def test_withdraw_larger_than_balance(self):
        
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "100" , 
                "refrence_key" : uuid.uuid4()
            } ,
            format="json"
        )
        res1 = self.client.post(
            "/api/wallet/withdraw/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "110" , 
                "refrence_key" : uuid.uuid4()
            } ,
            format="json"
        )
        self.assertEqual(
            res1.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
        Wallet.objects.get(wallet_id = self.wallet.wallet_id).balance , 
        Decimal("100")
        )
        self.assertFalse(res1.data["success"])
        self.assertEqual(
            TransactionLog.objects.count() , 
            1
        )



    def test_negetive_deposite(self):
        refrenceKey = uuid.uuid4()
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "-80" , 
                "refrence_key" : refrenceKey
            } ,
            format="json"
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
        Wallet.objects.get(wallet_id = self.wallet.wallet_id).balance , 
        Decimal("00")
        )
        self.assertFalse(res.data["success"])
        self.assertEqual(
            TransactionLog.objects.count() , 
            0
        )

    def test_retry_deposite(self):
        refrenceKey = uuid.uuid4()
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "80" , 
                "refrence_key" : refrenceKey
            } ,
            format="json"
        )
        res2 = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "80" , 
                "refrence_key" : refrenceKey
            } ,
            format="json"
        )
        res3 = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "80" , 
                "refrence_key" : refrenceKey
            } ,
            format="json"
        )
        self.assertEqual(
            res3.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
        res3.data["data"]["balance"],
        Decimal("80.00")
        )
        self.assertEqual(
        Wallet.objects.get(wallet_id = self.wallet.wallet_id).balance , 
        Decimal("80")
        )
        self.assertEqual(
            TransactionLog.objects.count() , 
            1
        )

