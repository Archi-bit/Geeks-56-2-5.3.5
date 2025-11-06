from django.contrib import admin
from .models import ConfirmationCode

@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'used', 'created_at')
    search_fields = ('user__username', 'code')
    list_filter = ('used',)