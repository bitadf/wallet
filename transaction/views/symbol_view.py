from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from transaction.serializers.symbol_serializer import SymbolSerializer

from transaction.service.symbol_servic import (
    create_symbol,
    delete_symbol,
    get_symbols
)

from transaction.utils.messages import (
    symbolCreated,
    symbolDeleted
)

from transaction.utils.exceptions import (
    SymbolDatabaseError,
    SymbolDatabaseUnavailableError,
    SymbolNotFoundError,
    DuplicateSymbolError
)


@api_view(["POST"])
def create_symbol_view(request):

    serializer = SymbolSerializer(
        data=request.data
    )

    if not serializer.is_valid():

        return Response(
            {
                "success": False,
                "message": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    try:

        symbol = create_symbol(
            serializer.validated_data["name"]
        )

        return Response(
            {
                "success": True,
                "message": symbolCreated,
                "symbolId": symbol.symbol_id
            },
            status=status.HTTP_201_CREATED
        )

    except DuplicateSymbolError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except (
        SymbolDatabaseUnavailableError,
        SymbolDatabaseError
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


@api_view(["DELETE"])
def delete_symbol_view(request, symbol_id):

    try:

        delete_symbol(
            symbol_id=symbol_id
        )

        return Response(
            {
                "success": True,
                "message": symbolDeleted
            },
            status=status.HTTP_200_OK
        )

    except SymbolNotFoundError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_404_NOT_FOUND
        )

    except (
        SymbolDatabaseUnavailableError,
        SymbolDatabaseError
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
def get_symbols_view(request):

    try:

        symbols = get_symbols()

        return Response(
            {
                "success": True,
                "data": list(symbols)
            },
            status=status.HTTP_200_OK
        )

    except (
        SymbolDatabaseUnavailableError,
        SymbolDatabaseError
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