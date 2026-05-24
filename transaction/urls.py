from django.urls import path

from transaction.views.symbol_view import (
    create_symbol_view,
    delete_symbol_view , 
    get_symbols_view
)
from transaction.views.user_view import create_user_view, get_users_view
from transaction.views.wallet_view import (
    create_wallet_veiw , 
    get_wallets_view 
)
from transaction.views.transcaction_view import (deposit_view , withdraw_view , get_transactions_view , get_balance_view)
urlpatterns = [

    path( "symbol/",create_symbol_view),
    path("symbols/" , get_symbols_view),
    path("symbols/<uuid:symbol_id>/", delete_symbol_view),
    path("wallet/", create_wallet_veiw),
    path("wallets/" , get_wallets_view) ,
    path("users/",get_users_view),
    path("user/",create_user_view ),
    path("wallet/deposit/" , deposit_view ),
    path("wallet/withdraw/" , withdraw_view) , 
    path("wallet/balance/" , get_balance_view) , 
    path("transactions/" , get_transactions_view)
]
