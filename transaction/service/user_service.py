from django.db import (
    IntegrityError,
    OperationalError,
    DatabaseError
)

from transaction.models import User

from transaction.utils.messages import (
    databaseError,
    databaseUnavaiableError,
    userExistsError
)

from transaction.utils.exceptions import (
    UserDatabaseError,
    UserDatabaseUnavailableError,
    DuplicateUserError
)


def create_user(name):

    try:

        user = User.objects.create(
            name=name.strip()
        )

        return user

    except IntegrityError:

        raise DuplicateUserError(
            userExistsError
        )

    except OperationalError:

        raise UserDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise UserDatabaseError(
            databaseError
        )


def get_users():

    try:

        return User.objects.values(
            "user_id",
            "name"
        )

    except OperationalError:

        raise UserDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise UserDatabaseError(
            databaseError
        )