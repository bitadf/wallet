from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status

from transaction.models import (
    User,
    Symbol,
    Wallet
)

class CreateWalletApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(name = "Bita")
        self.symbol = Symbol.objects.create(name = "BTC")

    def test_create_wallet_invalid_user_id(self):

        res = self.client.post(
            "/api/wallet/",
            {
                "symbol_name": "BTC",
                "user_id": "123"
            },
            format="json"
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            res.data["success"],
            False
        )
        self.assertEqual(
        Wallet.objects.count(),
        0
        )
    def test_create_wallet_invalid_symbol_name(self):

        res = self.client.post(
            "/api/wallet/",
            {
                "symbol_name": "INVALID",
                "user_id": str(self.user.user_id)
            },
            format="json"
        )
        self.assertEqual(
            res.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertFalse(
            res.data["success"]
          
        )
        self.assertEqual(
        Wallet.objects.count(),
        0
        )

    def test_create_wallet_missing_symbol_name(self):
        res = self.client.post(
            "/api/wallet/",
            {
                "user_id" : str(self.user.user_id) 
            },
            format="json"
        )
        
        self.assertEqual(
            res.status_code ,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res.data['success'] , 
            False
        ) 

    def test_create_wallet_missing_user_id(self):
        res = self.client.post(
            "/api/wallet/",
            {
                "symbol_name": "BTC",  
            },
            format="json"
        )
        
        self.assertEqual(
            res.status_code ,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res.data['success'] , 
            False
        )
        
        self.assertEqual(
        Wallet.objects.count(),
        0
    ) 

    def test_duplicated_wallet(self):
        Wallet.objects.create(
            user = self.user,
            symbol = self.symbol
        )
        res = self.client.post(
            "/api/wallet/",
            {
                "symbol_name": "BTC",
                "user_id": str(self.user.user_id)
            },
            format="json"
        )
        
        self.assertEqual(
            res.status_code ,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            res.data['success'] , 
            False
        ) 
     
        self.assertEqual(
        Wallet.objects.count(),
        1
        )
    
    def test_creaet_wallet_successful(self):
        res = self.client.post(
            "/api/wallet/",
            {
                "symbol_name": "BTC",
                "user_id": str(self.user.user_id)
            },
            format="json"
        )
            
        self.assertEqual(
             res.status_code,
             status.HTTP_201_CREATED
        )
        self.assertEqual(
            res.data["success"],
            True
        )
        self.assertTrue(
            Wallet.objects.filter(
                user=self.user,
                symbol=self.symbol
            ).exists()
        )
        self.assertEqual(
        Wallet.objects.count(),
        1
    )