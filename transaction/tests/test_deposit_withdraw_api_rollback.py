from decimal import Decimal
from unittest.mock import patch
import uuid

from django.test import TestCase

from transaction.models import (
    User,
    Wallet,
    Symbol,
    TransactionLog
)
from rest_framework import status
from rest_framework.test import APITestCase

from transaction.service.transaction_service import (deposit , withdraw)
class AtomicRollbackApiTest(TestCase):
    def setUp(self):

        self.user = User.objects.create(
            name="Bita"
        )

        self.symbol = Symbol.objects.create(
            name="BTC"
        )

        self.wallet = Wallet.objects.create(
            user=self.user,
            symbol=self.symbol,
            balance=Decimal("100")
        )
    @patch("transaction.models.transaction.TransactionLog.objects.create")
    def test_atomic_deposit_api_rollback(self, mock_create):

        mock_create.side_effect = Exception(
            "Forced database failure"
        )
        res = self.client.post(
            "/api/wallet/deposit/" , 
            {
                "wallet_id" : self.wallet.wallet_id, 
                "user_id" : self.user.user_id , 
                "amount" : "80" , 
                "refrence_key" : uuid.uuid4()
            } ,
            format="json"
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("100")
        )

        self.assertEqual(
            TransactionLog.objects.count(),
            0
        )
    @patch("transaction.models.transaction.TransactionLog.objects.create")
    def test_atomic_withdraw_api_rollback(self, mock_create):

        mock_create.side_effect = Exception(
            "Forced database failure"
        )
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
        
        self.assertEqual(
            res.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
       

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("100")
        )

        self.assertEqual(
            TransactionLog.objects.count(),
            0
        )