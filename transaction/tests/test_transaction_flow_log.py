import uuid
from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status

from transaction.models import (
    User,
    Wallet,
    Symbol,
    TransactionLog
)


class TransactionHistoryApiTest(APITestCase):

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
            balance=Decimal("1000")
        )

    def test_transaction_history_empty(self):
        wallet_transactions_res = self.client.get(
            f"/api/transactions/?wallet_id=68164ba2-9f2d-4a1a-b4e0-4100bf9342d5"
        )

        self.assertEqual(
            wallet_transactions_res.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(wallet_transactions_res.data["data"]),
            0
        )


    def test_transaction_history_success(self):

        # ---------- DEPOSIT ----------

        deposit_res = self.client.post(
            "/api/wallet/deposit/",
            {
                "wallet_id": str(self.wallet.wallet_id),
                "user_id": str(self.user.user_id),
                "amount": "200",
                "refrence_key": str(uuid.uuid4())
            },
            format="json"
        )

        self.assertEqual(
            deposit_res.status_code,
            status.HTTP_200_OK
        )

        # ---------- WITHDRAW ----------

        withdraw_res = self.client.post(
            "/api/wallet/withdraw/",
            {
                "wallet_id": str(self.wallet.wallet_id),
                "user_id": str(self.user.user_id),
                "amount": "100",
                "refrence_key": str(uuid.uuid4())
            },
            format="json"
        )

        self.assertEqual(
            withdraw_res.status_code,
            status.HTTP_200_OK
        )

        # ---------- GET ALL TRANSACTIONS ----------

        all_transactions_res = self.client.get(
            "/api/transactions/"
        )

        self.assertEqual(
            all_transactions_res.status_code,
            status.HTTP_200_OK
        )

        # # ---------- GET BY WALLET ----------

        wallet_transactions_res = self.client.get(
            f"/api/transactions/?wallet_id={self.wallet.wallet_id}"
        )

        self.assertEqual(
            wallet_transactions_res.status_code,
            status.HTTP_200_OK
        )

        # # ---------- GET BY USER ----------

        user_transactions_res = self.client.get(
            f"/api/transactions/?user_id={self.user.user_id}"
        )

        self.assertEqual(
            user_transactions_res.status_code,
            status.HTTP_200_OK
        )

        # # ---------- CHECK DATABASE ----------
        balance_res = self.client.get(
            f"/api/wallet/balance/?wallet_id={self.wallet.wallet_id}&user_id={self.user.user_id}",
           
        )

        self.assertEqual(
           balance_res.status_code,
            status.HTTP_200_OK
        )
        # self.wallet.refresh_from_db()
     


        self.assertEqual(
             Decimal(balance_res.data["data"]["balance"]) , 
            Decimal("1100")
        )



        self.assertEqual(
            TransactionLog.objects.count(),
            2
        )

        # # ---------- CHECK RESPONSE DATA ----------

        wallet_data = wallet_transactions_res.data["data"]

        self.assertEqual(
            len(wallet_data),
            2
        )

        print(wallet_transactions_res.data)