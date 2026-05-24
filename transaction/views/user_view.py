from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from transaction.serializers.user_serializer import UserSerializer

from transaction.service.user_service import (
    create_user,
    get_users
)

from transaction.utils.exceptions import (
    DuplicateUserError,
    UserDatabaseError,
    UserDatabaseUnavailableError
)


@api_view(["POST"])
def create_user_view(request):

    serializer = UserSerializer(
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

        user = create_user(
            serializer.validated_data["name"]
        )

        return Response(
            {
                "success": True,
                "data": {
                    "user_id": user.user_id,
                    "name": user.name
                }
            },
            status=status.HTTP_201_CREATED
        )

    except DuplicateUserError as e:

        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    except (
        UserDatabaseError,
        UserDatabaseUnavailableError
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
def get_users_view(request):

    try:

        users = get_users()

        serializer = UserSerializer(
            users,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except (
        UserDatabaseError,
        UserDatabaseUnavailableError
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