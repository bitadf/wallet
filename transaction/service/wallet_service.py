from django.db import (transaction , 
                       IntegrityError ,
                       OperationalError,
                       DatabaseError)

from transaction.models import Wallet , Symbol
from transaction.models import User
from transaction.utils.messages import (walletExistsError , databaseError , databaseUnavaiableError , userNotFoundError , symbolNotFoundError)

from transaction.utils.exceptions import (
    DuplicateWalletError,
    WalletDatabaseError,
    WalletDatabaseUnavailableError,
    UserNotFoundError,
    SymbolNotFoundError
)


def create_wallet(user_id , symbol_name):
    try:
        user = User.objects.get(user_id = user_id)
        
        symbol_name = symbol_name.upper().strip()
        symbol = Symbol.objects.get(name = symbol_name)

        wallet , created = Wallet.objects.get_or_create(
            user = user,
            symbol = symbol,
            defaults={
                "balance" : 0
            }
            
        )
        if not created:
            raise DuplicateWalletError(walletExistsError)
        return wallet
    except Symbol.DoesNotExist:
        raise SymbolNotFoundError(symbolNotFoundError)
    except User.DoesNotExist:
        raise UserNotFoundError(userNotFoundError)
    except IntegrityError:
        raise DuplicateWalletError(walletExistsError)
    except OperationalError:
        raise WalletDatabaseUnavailableError(databaseUnavaiableError)
    except DatabaseError:
        raise WalletDatabaseError(databaseError)

def get_wallets():
    try:

        return Wallet.objects.select_related(
            "user"
        ).all()

    except OperationalError:
        raise WalletDatabaseUnavailableError(databaseUnavaiableError)
    except DatabaseError:
        raise WalletDatabaseError(databaseError)
