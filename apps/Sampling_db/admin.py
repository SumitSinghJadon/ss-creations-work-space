from django.contrib import admin
from .models import SampleBookingMt, FinishTransactionDt


class SampleBookingMtAdmin(admin.ModelAdmin):
    list_display = ["booking_no", "merchant_name", "created_at", "is_active"]
    list_filter = ["booking_no", "merchant_name", "is_active"]


class FinishTransactionDtAdmin(admin.ModelAdmin):
    list_display = ['booking_no', 'transaction_no', 'finish_qty', 'created_at']
    list_filter = ['booking_no']
    list_editable = ['created_at']

admin.site.register(SampleBookingMt)
admin.site.register(FinishTransactionDt, FinishTransactionDtAdmin)


