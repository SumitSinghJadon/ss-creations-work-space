from django.db import models 


class SystemParameter(models.Model):
    pass 


    class Meta:
        db_table = 'system_parameter'
        app_label = 'IntelliSync_db'
