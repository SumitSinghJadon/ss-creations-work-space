from django.db import models
from .module_master import ModuleMaster


class MenuMaster(models.Model):
    module = models.ForeignKey(ModuleMaster, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='menu_set')
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)
    is_link = models.BooleanField(default=False)
    index = models.CharField(max_length=255, null=True, blank=True, default='999')
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    class Meta:
        db_table = 'menu_master'
        app_label = 'IntelliSync_db'
        # unique_together = ['module', 'index']
        ordering = ['module__name', 'name']

    def __str__(self):
        # return f"{ self.name } ({ self.module.name })"
        return self.name
    
    def to_dict(self):
        menu_dict = {
            'name': self.name,
            'icon': self.icon,
            'url' : self.url
        }
        children = MenuMaster.objects.filter(parent=self)
        if children.exists():
            menu_dict['children'] = [child.to_dict() for child in children]
        return menu_dict


class SubMenuMaster(models.Model):
    main_menu = models.ForeignKey(MenuMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    url = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True, db_column='updated_at')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    
    class Meta:
        db_table = 'sub_menu_master'
        app_label = 'IntelliSync_db'

    def __str__(self):
        return self.name

