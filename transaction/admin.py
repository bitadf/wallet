from django.contrib import admin

from .models import Wallet , TransactionLog , Symbol , User

# Register your models here.
admin.site.register(Wallet)
admin.site.register(TransactionLog)
admin.site.register(Symbol)
admin.site.register(User)