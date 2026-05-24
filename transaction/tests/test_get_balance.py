from decimal import Decimal

from rest_framework.test import APITestCase
from rest_framework import status

from transaction.models import (
    User,
    Wallet,
    Symbol
)


class GetBalanceAPITest(APITestCase):

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
            balance=Decimal("750")
        )

    def test_get_balance(self):

        res = self.client.get(
            f"/api/wallet/balance/?wallet_id={self.wallet.wallet_id}&user_id={self.user.user_id}"
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            Decimal(res.data["data"]["balance"]),
            Decimal("750")
        )