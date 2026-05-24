from django.db import (transaction , IntegrityError , OperationalError , DatabaseError)

from transaction.models import(Wallet , TransactionLog)
from transaction.utils.messages import (invalidAmountError , walletUnAuthorizedError , 
                                        databaseUnavaiableError , databaseError , transactionLogDuplicatedError , balanceNotFound , 
                                        largeAmountError)

from transaction.utils.exceptions import(TransactionDatabaseError , TransactionDatabaseUnavailableError , DuplicateTransactionError ,WalletUnauthorizedError , BalanceNotFound , WithdrawLargeAmount)

def get_balance(wallet_id , user_id):
    try : 
        balance = Wallet.objects.values("balance" ).get(
            user__user_id = user_id,
            wallet_id = wallet_id
        )
        return balance['balance']

    except Wallet.DoesNotExist :
        raise WalletUnauthorizedError(
            walletUnAuthorizedError
        )
    except OperationalError:
        raise TransactionDatabaseUnavailableError(
            databaseUnavaiableError
        )
    except DatabaseError : 
        raise TransactionDatabaseError(
            databaseError
        )
def deposit(wallet_id , amount , user_id , refrence_key):
    try : 
        exists = TransactionLog.objects.filter(
                refrence_key=refrence_key,

            ).first()
        if exists : 
                return {
                    "wallet" : exists.wallet,
                    "transaction" : exists ,
                    "duplicated" : True
                }
        with transaction.atomic():
            
            
            wallet = Wallet.objects.select_for_update().get(
                wallet_id=wallet_id,
                user__user_id=user_id
            )


        # wallet = Wallet.objects.select_for_update().get(
        #     wallet_id = wallet_id ,
        #    )
        # if wallet.user.user_id != user_id :
        #     raise ValueError(
        #         walletUnAuthorizedError
        #     )
        

        
            wallet.balance += amount
            wallet.save()  

            transactionRes = TransactionLog.objects.create(
                wallet = wallet ,
                transaction_type = TransactionLog.TransactionType.DEPOSIT,
                amount = amount , 
                refrence_key = refrence_key,
            )
            return{
                "wallet" : wallet ,
                "transaction" : transactionRes ,
                "duplicated" : False
            }
    except Wallet.DoesNotExist :
        raise WalletUnauthorizedError(
            walletUnAuthorizedError
        )
    except IntegrityError:
        raise DuplicateTransactionError(
            transactionLogDuplicatedError
        )
    except OperationalError:
        raise TransactionDatabaseUnavailableError(
            databaseUnavaiableError
        )
    except DatabaseError : 
        raise TransactionDatabaseError(
            databaseError
        )

def withdraw(wallet_id , amount , user_id , refrence_key):
    try:
        exists = TransactionLog.objects.filter(
                refrence_key=refrence_key,

            ).first()
        if exists : 
                return {
                    "wallet" : exists.wallet,
                    "transaction" : exists ,
                    "duplicated" : True
                }
        with transaction.atomic():   
           
                

            wallet = Wallet.objects.select_for_update().get(
                    wallet_id=wallet_id,
                    user__user_id=user_id
                )

        # wallet = Wallet.objects.select_for_update().get(
        #     wallet_id = wallet_id
        # )
        # if wallet.user.user_id != user_id :
        #     raise ValueError(
        #         walletUnAuthorizedError
        #     )
            if wallet.balance < amount:
                raise WithdrawLargeAmount(
                    largeAmountError
                )
                
        
            wallet.balance -= amount
            wallet.save()

            transactionRes = TransactionLog.objects.create(
                wallet = wallet ,
                transaction_type = TransactionLog.TransactionType.WITHDRAW ,
                amount = amount , 
                refrence_key = refrence_key,
            )

            return {
                "wallet" : wallet ,
                "transaction" : transactionRes ,
                "duplicated":False
            }

    except Wallet.DoesNotExist :
        raise WalletUnauthorizedError(
            walletUnAuthorizedError
        )
    except IntegrityError:
        raise DuplicateTransactionError(
            transactionLogDuplicatedError
        )
    except OperationalError:
        raise TransactionDatabaseUnavailableError(
            databaseUnavaiableError
        )
    except DatabaseError : 
        raise TransactionDatabaseError(
            databaseError
        )

def get_transactions(wallet_id=None, user_id=None):

    try:

        queryset = TransactionLog.objects.select_related(
            "wallet",
            "wallet__user"
        )

        if wallet_id:

            queryset = queryset.filter(
                wallet__wallet_id=wallet_id
            )

        if user_id:

            queryset = queryset.filter(
                wallet__user__user_id=user_id
            )

        return queryset.order_by("-created_at")

    except OperationalError:

        raise TransactionDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise TransactionDatabaseError(
            databaseError
        )