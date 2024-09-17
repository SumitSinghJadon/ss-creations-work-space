from django.db import models

class DepartmentMaster(models.Model):
    dep_code = models.BigIntegerField(unique=True,primary_key=True, db_column='dep_code')
    dep_name = models.CharField(max_length=100, blank=True, null=True)
    cmp_code = models.IntegerField()
    tdh_code = models.IntegerField()
    tmp = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tbdep'
        app_label = 'Payroll_db'
    
    def __str__(self):
        return self.dep_name  

