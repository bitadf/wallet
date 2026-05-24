from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from transaction.serializers.transaction_serializer import (TransactionSerializer )
from transaction.serializers.transaction_log_serializer import (TransactionLogSerializer)
from transaction.service.transaction_service import (withdraw , deposit , get_transactions , get_balance)
from transaction.utils.exceptions import(TransactionDatabaseError , TransactionDatabaseUnavailableError , DuplicateTransactionError ,WalletUnauthorizedError , WithdrawLargeAmount)
from transaction.utils.messages import (userIdAndWalletIdAreRequired)
@api_view(["POST"])
def deposit_view(request):
    serializer = TransactionSerializer(
        data = request.data
    )

    if not serializer.is_valid():
        return Response(
            {
                "success": False ,
                "message" : serializer.errors
            },
            status = status.HTTP_400_BAD_REQUEST
        )
    try : 
        result = deposit(
            wallet_id=serializer.validated_data["wallet_id"],
            amount=serializer.validated_data["amount"],
            user_id=serializer.validated_data["user_id"] ,
                          refrence_key=serializer.validated_data["refrence_key"] ,
        )

        return Response(
            {
                "success": True ,
                "data" : {
                    "walletId" : str(result["wallet"].wallet_id) , 
                    "balance" : result["wallet"].balance,
                    "transactionId" : str(result["transaction"].transaction_id)
                }
            },
            status = status.HTTP_200_OK
        )
    
    except WalletUnauthorizedError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_403_FORBIDDEN
        )

    except (
        TransactionDatabaseUnavailableError,
        TransactionDatabaseError
    ) as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(["POST"])
def withdraw_view(request):
    serializer = TransactionSerializer(
        data = request.data
    )
    if not serializer.is_valid():
        return Response(
            {
                "success" : False,
                "message" : serializer.errors
            } , 
            status = status.HTTP_400_BAD_REQUEST
        )
    
    try :
        res = withdraw(
            wallet_id=serializer.validated_data["wallet_id"],
            amount=serializer.validated_data["amount"] ,
             user_id=serializer.validated_data["user_id"] ,
              refrence_key=serializer.validated_data["refrence_key"] ,
             

        )
        return Response({
            "success" : True , 
            "data" : {
                "walletId" : str(res["wallet"].wallet_id),
                "balance" : res["wallet"].balance , 
                "transactionId" : str(res["transaction"].transaction_id )
            }
        },
        status = status.HTTP_200_OK)
    except WithdrawLargeAmount as e:
        return Response(
            {
                "success" : False,
                "message" : str(e)
            } , 
            status = status.HTTP_400_BAD_REQUEST
        )

    except WalletUnauthorizedError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_403_FORBIDDEN
        )

    except (
        TransactionDatabaseUnavailableError,
        TransactionDatabaseError
    ) as e:
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(["GET"])
def get_transactions_view(request):

    try:

        wallet_id = request.query_params.get("wallet_id")
        user_id = request.query_params.get("user_id")

        transactions = get_transactions(
            wallet_id=wallet_id,
            user_id=user_id
        )
        serializer = TransactionLogSerializer(transactions , many = True)

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except (
        TransactionDatabaseError,
        TransactionDatabaseUnavailableError
    ) as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(["GET"])
def get_balance_view(request):
    try:
        
        wallet_id = request.query_params.get("wallet_id")
        user_id = request.query_params.get("user_id")

        if not wallet_id or not user_id:

            return Response(
                {
                    "success": False,
                    "message": userIdAndWalletIdAreRequired
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        balance = get_balance(
            wallet_id=wallet_id,
            user_id=user_id
        )
        return Response(
            {
                "success": True,
                "data": {
                    "balance": balance
                }
            },
            status=status.HTTP_200_OK
        )
    
    except WalletUnauthorizedError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_403_FORBIDDEN
        )

    except (
        TransactionDatabaseUnavailableError,
        TransactionDatabaseError
    ) as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

     