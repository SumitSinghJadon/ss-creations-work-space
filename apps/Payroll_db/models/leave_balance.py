from django.db import models
from .employee_master import models

class LeaveBalance(models.Model):
    cmp_code = models.IntegerField()
    emp_code = models.IntegerField(primary_key=True)
    month_no = models.IntegerField()
    el = models.FloatField(db_column='EL')
    pl = models.FloatField(db_column='PL')
    cl = models.FloatField(db_column='CL')
    sl = models.FloatField(db_column='SL')
    co = models.FloatField(db_column='CO')
    sp = models.FloatField(db_column='SP')
    mt = models.FloatField(db_column='MT')
    bel = models.FloatField(db_column='BEL')
    bpl = models.FloatField(db_column='BPL')
    bcl = models.FloatField(db_column='BCL')
    bsl = models.FloatField(db_column='BSL')
    bco = models.FloatField(db_column='BCO')
    bsp = models.FloatField(db_column='BSP')
    bmt = models.FloatField(db_column='BMT')
    wd = models.FloatField()
    wo = models.FloatField()
    hd = models.FloatField()
    ab = models.FloatField()
    pd = models.FloatField()
    wom = models.IntegerField()
    otm = models.IntegerField()
    lm = models.IntegerField()
    womt = models.CharField(max_length=7, blank=True, null=True)
    otmt = models.CharField(max_length=7, blank=True, null=True)
    lmt = models.CharField(max_length=7, blank=True, null=True)
    otrat = models.FloatField()
    netm = models.IntegerField()
    netmt = models.CharField(max_length=7, blank=True, null=True)
    mot = models.FloatField()
    maninc = models.FloatField()
    ehrs = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tbmatd'
        unique_together = (('emp_code', 'month_no'),)
