from django.contrib import admin
from IntelliSync_db.models import (
    ModuleMaster, MenuMaster, SubMenuMaster, 
    PermissionMaster, PagePermissionMaster, ProjectMaster, NumberingMethod
)
from IntelliSync_db.models import User 


class ModuleMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'separate_menu']
    list_editable = ['image']


class SubMenuMasterInline(admin.TabularInline):
    model = MenuMaster


class PagePermissionMasterInline(admin.TabularInline):
    model = PagePermissionMaster
    list_display = ['page', 'permission']


class MenuMasterAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'parent', 'index', 'url', 'is_active']
    list_editable = ['name','index', 'url', 'is_active']
    list_filter = ['name', 'parent', 'module']
    ordering = ['parent', 'index']
    inlines = [SubMenuMasterInline, PagePermissionMasterInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "page":
            kwargs["queryset"] = MenuMaster.objects.filter(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_editable = ['code', 'is_active']


class PagePermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['page', 'permission', 'is_active']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'location', 'email', 'reporting_manager', 'is_superuser', 'is_super_staff', 'is_active']
    exclude = ['last_login', 'groups', 'user_permissions']
    list_filter = ['username', 'is_active', 'location', 'reporting_manager']
    list_editable = ['location', 'email', 'reporting_manager']


admin.site.register(User, UserAdmin)
admin.site.register(ProjectMaster)
admin.site.register(ModuleMaster, ModuleMasterAdmin)
admin.site.register(MenuMaster, MenuMasterAdmin)

admin.site.register(PermissionMaster, PermissionMasterAdmin)
admin.site.register(PagePermissionMaster, PagePermissionMasterAdmin)
admin.site.register(NumberingMethod)
