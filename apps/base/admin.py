from django.contrib import admin
#from django.contrib.auth.decorators import login_required

from base import helpers
from .models import *
from .conf import settings


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'balance', 'is_active', 'is_admin', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_admin', 'is_staff', 'date_joined')
    search_fields = ('email',)

    def balance(self, obj):
        return helpers.get_token_balance(obj.address)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'description', 'modified', 'created')
    list_filter = ('created',)
    search_fields = ('user__email',)


admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)

#admin.site.login = login_required(admin.site.login)
#admin.autodiscover()

admin.site.site_title = settings.ICO_TOKEN_NAME
admin.site.site_header = "{0} Administrator".format(settings.ICO_TOKEN_NAME)

