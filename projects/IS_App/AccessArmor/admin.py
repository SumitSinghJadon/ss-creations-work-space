from django.contrib import admin
from IntelliSync_db.models import (
    ModuleMaster, MenuMaster, SubMenuMaster, 
    PermissionMaster, PagePermissionMaster, ProjectMaster
)
from IntelliSync_db.models import User 


class ModuleMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'separate_menu']
    list_editable = ['image']

class SubMenuMasterInline(admin.TabularInline):
    model = MenuMaster

class MenuMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'index', 'is_active']
    list_editable = ['index', 'is_active']
    ordering = ['-module', 'index']
    inlines = [SubMenuMasterInline]


class PermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_editable = ['code', 'is_active']


class PagePermissionMasterInline(admin.TabularInline):
    model = PagePermissionMaster
    list_display = ['page', 'permission']


class PagePermissionMasterAdmin(admin.ModelAdmin):
    list_display = ['page', 'permission', 'is_active']


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'full_name', 'is_superuser', 'is_active']
    exclude = ['last_login', 'groups', 'user_permissions']


admin.site.register(User, UserAdmin)
admin.site.register(ProjectMaster)
admin.site.register(ModuleMaster, ModuleMasterAdmin)
admin.site.register(MenuMaster, MenuMasterAdmin)

admin.site.register(PermissionMaster, PermissionMasterAdmin)
admin.site.register(PagePermissionMaster, PagePermissionMasterAdmin)


