from django.db import models


class HolidayMaster(models.Model):
    h_code = models.IntegerField()
    h_name = models.CharField(max_length=100, blank=True, null=True)
    h_date = models.DateTimeField(blank=True, null=True)
    h_type = models.IntegerField()
    cmp_code = models.IntegerField()
    tmp = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tbholi'
