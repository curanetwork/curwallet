from django.contrib import admin
from base.conf import settings

admin.site.site_title = f'{settings.ICO_TOKEN_NAME} Wallet'
admin.site.site_header = f'{settings.ICO_TOKEN_NAME} Wallet Administration'