from django.db import models


class DesignationMaster(models.Model):
    des_code = models.BigIntegerField(unique=True,primary_key=True, db_column='des_code')
    des_name = models.CharField(max_length=100, blank=True, null=True)
    cmp_code = models.IntegerField()
    tmp = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tbdes'
        app_label = 'Payroll_db'
    
    def __str__(self):
        return self.des_name

