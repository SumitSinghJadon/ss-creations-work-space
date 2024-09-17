from django.contrib import admin
from QMS_db.models import OrderDt,OrderMt,OrderProcess
from QMS_db.models.defect_master import ProcessMaster,DefectMaster


class OrderDtInline(admin.StackedInline):
    model = OrderDt
    extra = 1

class OrderMtAdmin(admin.ModelAdmin):
    list_display = ['ouuref', 'style_no', 'quantity']
    search_fields = ['style_no']
    inlines = [OrderDtInline]
    
admin.site.register(OrderMt)
admin.site.register(OrderDt)
admin.site.register(OrderProcess)


class OrderDtAdmin(admin.ModelAdmin):
    list_display = ["buyer", "ourref_no", 'style_name', 'quantity']
    search_fields = ['ourref_no','buyer']

admin.site.register(ProcessMaster)
admin.site.register(DefectMaster)