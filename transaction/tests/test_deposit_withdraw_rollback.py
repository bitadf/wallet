from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from transaction.models import (
    User,
    Wallet,
    Symbol,
    TransactionLog
)

from transaction.service.transaction_service import (deposit , withdraw)


class AtomicRollbackTest(TestCase):

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
    def test_atomic_deposit_rollback(self, mock_create):

        mock_create.side_effect = Exception(
            "Forced database failure"
        )

        try:
            deposit(
                wallet_id=self.wallet.wallet_id,
                amount=Decimal("50"),
                user_id=self.user.user_id,
                refrence_key="rollback-test"
            )
        except Exception:
            pass

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
    def test_atomic_withdraw_rollback(self, mock_create):

        mock_create.side_effect = Exception(
            "Forced database failure"
        )

        try:
            withdraw(
                wallet_id=self.wallet.wallet_id,
                amount=Decimal("50"),
                user_id=self.user.user_id,
                refrence_key="rollback-test"
            )
        except Exception:
            pass

        self.wallet.refresh_from_db()

        self.assertEqual(
            self.wallet.balance,
            Decimal("100")
        )

        self.assertEqual(
            TransactionLog.objects.count(),
            0
        )
    