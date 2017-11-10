from django.contrib import admin
from wallet.models import (Transaction, Coupon)

admin.site.register(Transaction)
admin.site.register(Coupon)
