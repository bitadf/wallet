from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from transaction.serializers.wallet_serializer import WalletSerializer
from transaction.service.wallet_service import create_wallet, get_wallets
from transaction.utils.messages import (
    walletCreated
)
from transaction.utils.exceptions import (
    DuplicateWalletError,
    WalletDatabaseError,
    WalletDatabaseUnavailableError,
    UserNotFoundError,
    SymbolNotFoundError
)

@api_view(["POST"])
def create_wallet_veiw(request):
    serializer = WalletSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "success" : False ,
            "message": serializer.errors
        } ,
        status = status.HTTP_400_BAD_REQUEST)
    
    try : 
        wallet = create_wallet(
            user_id = serializer.validated_data["user_id"], 
            symbol_name=serializer.validated_data["symbol_name"]
        )
        return Response({
            "success" : True , 
            "message" : walletCreated,
            "data" : {
                "walletId" : wallet.wallet_id,
                
            }    
        } , 
        status = status.HTTP_201_CREATED)
    except (UserNotFoundError , SymbolNotFoundError , DuplicateWalletError) as e :
        return Response({
            "success" : False ,
            "message": str(e)
        } ,
        status = status.HTTP_400_BAD_REQUEST)
    except (WalletDatabaseError , WalletDatabaseUnavailableError) as e: 
        return Response(
            {
                "success" : False , 
                "message" : str(e)
            } ,
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
def get_wallets_view(request):
    try:

        wallets = get_wallets()

        serializer = WalletSerializer(
            wallets,
            many=True
        )
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except (WalletDatabaseError , WalletDatabaseUnavailableError) as e:
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
