from django.db import (
    DatabaseError,
    OperationalError,
    IntegrityError
)

from transaction.models import Symbol

from transaction.utils.messages import (
    symbolNotFoundError,
    databaseError,
    databaseUnavaiableError,
    symbolExistsError
)

from transaction.utils.exceptions import (
    SymbolDatabaseError,
    SymbolDatabaseUnavailableError,
    SymbolNotFoundError,
    DuplicateSymbolError
)


def create_symbol(name):

    try:

        name = name.upper().strip()

        symbol = Symbol.objects.create(
            name=name
        )

        return symbol

    except IntegrityError:

        raise DuplicateSymbolError(
            symbolExistsError
        )

    except OperationalError:

        raise SymbolDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise SymbolDatabaseError(
            databaseError
        )


def delete_symbol(symbol_id):

    try:

        symbol = Symbol.objects.get(
            symbol_id=symbol_id
        )

        symbol.delete()

    except Symbol.DoesNotExist:

        raise SymbolNotFoundError(
            symbolNotFoundError
        )

    except OperationalError:

        raise SymbolDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise SymbolDatabaseError(
            databaseError
        )


def get_symbols():

    try:

        return Symbol.objects.values(
            "symbol_id",
            "name"
        )

    except OperationalError:

        raise SymbolDatabaseUnavailableError(
            databaseUnavaiableError
        )

    except DatabaseError:

        raise SymbolDatabaseError(
            databaseError
        )