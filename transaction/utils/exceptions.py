class WalletUnauthorizedError(Exception):
    pass
class InvalidAmountError(Exception):
    pass
class TransactionDatabaseUnavailableError(Exception):
    pass
class TransactionDatabaseError(Exception):
    pass
class DuplicateTransactionError(Exception):
    pass
class DuplicateWalletError(Exception):
    pass
class WalletDatabaseError(Exception):
    pass
class WalletDatabaseUnavailableError(Exception):
    pass
class UserNotFoundError(Exception):
    pass
class SymbolNotFoundError(Exception):
    pass
class SymbolDatabaseError(Exception):
    pass
class SymbolDatabaseUnavailableError(Exception):
    pass
class BalanceNotFound(Exception):
    pass
class UserDatabaseUnavailableError(Exception):
    pass
class UserDatabaseError(Exception):
    pass
class DuplicateUserError(Exception):
    pass
class DuplicateSymbolError(Exception):
    pass
class WithdrawLargeAmount(Exception): 
    pass
