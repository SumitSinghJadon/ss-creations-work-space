from django.contrib import admin
from IntelliSync_db.models import (
    CommonMasterType, CommonMaster,  
    FirstLevelMaster, SecondLevelMaster, 
    LocationMaster, CompanyMaster, CountryMaster, StateMaster, DistrictMaster,
    name_code_list
)


class CommonMasterTypeAdmin(admin.ModelAdmin):
    list_display = ['display_code', 'name', 'parent', 'label_type', 'editable', 'is_active']
    ordering = ['code']
    
    def display_code(self, obj):
        for code, name in name_code_list:
            if code == obj.code:
                return code
        return obj.code


class CommonMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'master_type', 'value']
    list_editable = ['value']


admin.site.register(CommonMasterType, CommonMasterTypeAdmin)
admin.site.register(CommonMaster, CommonMasterAdmin)
admin.site.register(CountryMaster)
admin.site.register(CompanyMaster)
admin.site.register(LocationMaster)
admin.site.register(StateMaster)
admin.site.register(DistrictMaster)
