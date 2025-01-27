from django.db import models
from .employee_master import EmployeeMaster


class TimeHourDay(models.Model):
    emp_code = models.ForeignKey(EmployeeMaster,on_delete=models.DO_NOTHING,db_constraint=False, related_name='time_hour_day_emp_code', db_column='emp_code')
    month_no = models.IntegerField()
    cmp_code = models.IntegerField()
    atp1 = models.CharField(max_length=7, blank=True, null=True)
    atp2 = models.CharField(max_length=7, blank=True, null=True)
    atp3 = models.CharField(max_length=7, blank=True, null=True)
    atp4 = models.CharField(max_length=7, blank=True, null=True)
    atp5 = models.CharField(max_length=7, blank=True, null=True)
    atp6 = models.CharField(max_length=7, blank=True, null=True)
    atp7 = models.CharField(max_length=7, blank=True, null=True)
    atp8 = models.CharField(max_length=7, blank=True, null=True)
    atp9 = models.CharField(max_length=7, blank=True, null=True)
    atp10 = models.CharField(max_length=7, blank=True, null=True)
    atp11 = models.CharField(max_length=7, blank=True, null=True)
    atp12 = models.CharField(max_length=7, blank=True, null=True)
    atp13 = models.CharField(max_length=7, blank=True, null=True)
    atp14 = models.CharField(max_length=7, blank=True, null=True)
    atp15 = models.CharField(max_length=7, blank=True, null=True)
    atp16 = models.CharField(max_length=7, blank=True, null=True)
    atp17 = models.CharField(max_length=7, blank=True, null=True)
    atp18 = models.CharField(max_length=7, blank=True, null=True)
    atp19 = models.CharField(max_length=7, blank=True, null=True)
    atp20 = models.CharField(max_length=7, blank=True, null=True)
    atp21 = models.CharField(max_length=7, blank=True, null=True)
    atp22 = models.CharField(max_length=7, blank=True, null=True)
    atp23 = models.CharField(max_length=7, blank=True, null=True)
    atp24 = models.CharField(max_length=7, blank=True, null=True)
    atp25 = models.CharField(max_length=7, blank=True, null=True)
    atp26 = models.CharField(max_length=7, blank=True, null=True)
    atp27 = models.CharField(max_length=7, blank=True, null=True)
    atp28 = models.CharField(max_length=7, blank=True, null=True)
    atp29 = models.CharField(max_length=7, blank=True, null=True)
    atp30 = models.CharField(max_length=7, blank=True, null=True)
    atp31 = models.CharField(max_length=7, blank=True, null=True)
    oth1 = models.CharField(max_length=5, blank=True, null=True)
    oth2 = models.CharField(max_length=5, blank=True, null=True)
    oth3 = models.CharField(max_length=5, blank=True, null=True)
    oth4 = models.CharField(max_length=5, blank=True, null=True)
    oth5 = models.CharField(max_length=5, blank=True, null=True)
    oth6 = models.CharField(max_length=5, blank=True, null=True)
    oth7 = models.CharField(max_length=5, blank=True, null=True)
    oth8 = models.CharField(max_length=5, blank=True, null=True)
    oth9 = models.CharField(max_length=5, blank=True, null=True)
    oth10 = models.CharField(max_length=5, blank=True, null=True)
    oth11 = models.CharField(max_length=5, blank=True, null=True)
    oth12 = models.CharField(max_length=5, blank=True, null=True)
    oth13 = models.CharField(max_length=5, blank=True, null=True)
    oth14 = models.CharField(max_length=5, blank=True, null=True)
    oth15 = models.CharField(max_length=5, blank=True, null=True)
    oth16 = models.CharField(max_length=5, blank=True, null=True)
    oth17 = models.CharField(max_length=5, blank=True, null=True)
    oth18 = models.CharField(max_length=5, blank=True, null=True)
    oth19 = models.CharField(max_length=5, blank=True, null=True)
    oth20 = models.CharField(max_length=5, blank=True, null=True)
    oth21 = models.CharField(max_length=5, blank=True, null=True)
    oth22 = models.CharField(max_length=5, blank=True, null=True)
    oth23 = models.CharField(max_length=5, blank=True, null=True)
    oth24 = models.CharField(max_length=5, blank=True, null=True)
    oth25 = models.CharField(max_length=5, blank=True, null=True)
    oth26 = models.CharField(max_length=5, blank=True, null=True)
    oth27 = models.CharField(max_length=5, blank=True, null=True)
    oth28 = models.CharField(max_length=5, blank=True, null=True)
    oth29 = models.CharField(max_length=5, blank=True, null=True)
    oth30 = models.CharField(max_length=5, blank=True, null=True)
    oth31 = models.CharField(max_length=5, blank=True, null=True)
    lth1 = models.CharField(max_length=5, blank=True, null=True)
    lth2 = models.CharField(max_length=5, blank=True, null=True)
    lth3 = models.CharField(max_length=5, blank=True, null=True)
    lth4 = models.CharField(max_length=5, blank=True, null=True)
    lth5 = models.CharField(max_length=5, blank=True, null=True)
    lth6 = models.CharField(max_length=5, blank=True, null=True)
    lth7 = models.CharField(max_length=5, blank=True, null=True)
    lth8 = models.CharField(max_length=5, blank=True, null=True)
    lth9 = models.CharField(max_length=5, blank=True, null=True)
    lth10 = models.CharField(max_length=5, blank=True, null=True)
    lth11 = models.CharField(max_length=5, blank=True, null=True)
    lth12 = models.CharField(max_length=5, blank=True, null=True)
    lth13 = models.CharField(max_length=5, blank=True, null=True)
    lth14 = models.CharField(max_length=5, blank=True, null=True)
    lth15 = models.CharField(max_length=5, blank=True, null=True)
    lth16 = models.CharField(max_length=5, blank=True, null=True)
    lth17 = models.CharField(max_length=5, blank=True, null=True)
    lth18 = models.CharField(max_length=5, blank=True, null=True)
    lth19 = models.CharField(max_length=5, blank=True, null=True)
    lth20 = models.CharField(max_length=5, blank=True, null=True)
    lth21 = models.CharField(max_length=5, blank=True, null=True)
    lth22 = models.CharField(max_length=5, blank=True, null=True)
    lth23 = models.CharField(max_length=5, blank=True, null=True)
    lth24 = models.CharField(max_length=5, blank=True, null=True)
    lth25 = models.CharField(max_length=5, blank=True, null=True)
    lth26 = models.CharField(max_length=5, blank=True, null=True)
    lth27 = models.CharField(max_length=5, blank=True, null=True)
    lth28 = models.CharField(max_length=5, blank=True, null=True)
    lth29 = models.CharField(max_length=5, blank=True, null=True)
    lth30 = models.CharField(max_length=5, blank=True, null=True)
    lth31 = models.CharField(max_length=5, blank=True, null=True)
    ot1 = models.IntegerField()
    ot2 = models.IntegerField()
    ot3 = models.IntegerField()
    ot4 = models.IntegerField()
    ot5 = models.IntegerField()
    ot6 = models.IntegerField()
    ot7 = models.IntegerField()
    ot8 = models.IntegerField()
    ot9 = models.IntegerField()
    ot10 = models.IntegerField()
    ot11 = models.IntegerField()
    ot12 = models.IntegerField()
    ot13 = models.IntegerField()
    ot14 = models.IntegerField()
    ot15 = models.IntegerField()
    ot16 = models.IntegerField()
    ot17 = models.IntegerField()
    ot18 = models.IntegerField()
    ot19 = models.IntegerField()
    ot20 = models.IntegerField()
    ot21 = models.IntegerField()
    ot22 = models.IntegerField()
    ot23 = models.IntegerField()
    ot24 = models.IntegerField()
    ot25 = models.IntegerField()
    ot26 = models.IntegerField()
    ot27 = models.IntegerField()
    ot28 = models.IntegerField()
    ot29 = models.IntegerField()
    ot30 = models.IntegerField()
    ot31 = models.IntegerField()
    lt1 = models.IntegerField()
    lt2 = models.IntegerField()
    lt3 = models.IntegerField()
    lt4 = models.IntegerField()
    lt5 = models.IntegerField()
    lt6 = models.IntegerField()
    lt7 = models.IntegerField()
    lt8 = models.IntegerField()
    lt9 = models.IntegerField()
    lt10 = models.IntegerField()
    lt11 = models.IntegerField()
    lt12 = models.IntegerField()
    lt13 = models.IntegerField()
    lt14 = models.IntegerField()
    lt15 = models.IntegerField()
    lt16 = models.IntegerField()
    lt17 = models.IntegerField()
    lt18 = models.IntegerField()
    lt19 = models.IntegerField()
    lt20 = models.IntegerField()
    lt21 = models.IntegerField()
    lt22 = models.IntegerField()
    lt23 = models.IntegerField()
    lt24 = models.IntegerField()
    lt25 = models.IntegerField()
    lt26 = models.IntegerField()
    lt27 = models.IntegerField()
    lt28 = models.IntegerField()
    lt29 = models.IntegerField()
    lt30 = models.IntegerField()
    lt31 = models.IntegerField()
    twm1 = models.IntegerField()
    twm2 = models.IntegerField()
    twm3 = models.IntegerField()
    twm4 = models.IntegerField()
    twm5 = models.IntegerField()
    twm6 = models.IntegerField()
    twm7 = models.IntegerField()
    twm8 = models.IntegerField()
    twm9 = models.IntegerField()
    twm10 = models.IntegerField()
    twm11 = models.IntegerField()
    twm12 = models.IntegerField()
    twm13 = models.IntegerField()
    twm14 = models.IntegerField()
    twm15 = models.IntegerField()
    twm16 = models.IntegerField()
    twm17 = models.IntegerField()
    twm18 = models.IntegerField()
    twm19 = models.IntegerField()
    twm20 = models.IntegerField()
    twm21 = models.IntegerField()
    twm22 = models.IntegerField()
    twm23 = models.IntegerField()
    twm24 = models.IntegerField()
    twm25 = models.IntegerField()
    twm26 = models.IntegerField()
    twm27 = models.IntegerField()
    twm28 = models.IntegerField()
    twm29 = models.IntegerField()
    twm30 = models.IntegerField()
    twm31 = models.IntegerField()
    thr1 = models.CharField(max_length=5, blank=True, null=True)
    thr2 = models.CharField(max_length=5, blank=True, null=True)
    thr3 = models.CharField(max_length=5, blank=True, null=True)
    thr4 = models.CharField(max_length=5, blank=True, null=True)
    thr5 = models.CharField(max_length=5, blank=True, null=True)
    thr6 = models.CharField(max_length=5, blank=True, null=True)
    thr7 = models.CharField(max_length=5, blank=True, null=True)
    thr8 = models.CharField(max_length=5, blank=True, null=True)
    thr9 = models.CharField(max_length=5, blank=True, null=True)
    thr10 = models.CharField(max_length=5, blank=True, null=True)
    thr11 = models.CharField(max_length=5, blank=True, null=True)
    thr12 = models.CharField(max_length=5, blank=True, null=True)
    thr13 = models.CharField(max_length=5, blank=True, null=True)
    thr14 = models.CharField(max_length=5, blank=True, null=True)
    thr15 = models.CharField(max_length=5, blank=True, null=True)
    thr16 = models.CharField(max_length=5, blank=True, null=True)
    thr17 = models.CharField(max_length=5, blank=True, null=True)
    thr18 = models.CharField(max_length=5, blank=True, null=True)
    thr19 = models.CharField(max_length=5, blank=True, null=True)
    thr20 = models.CharField(max_length=5, blank=True, null=True)
    thr21 = models.CharField(max_length=5, blank=True, null=True)
    thr22 = models.CharField(max_length=5, blank=True, null=True)
    thr23 = models.CharField(max_length=5, blank=True, null=True)
    thr24 = models.CharField(max_length=5, blank=True, null=True)
    thr25 = models.CharField(max_length=5, blank=True, null=True)
    thr26 = models.CharField(max_length=5, blank=True, null=True)
    thr27 = models.CharField(max_length=5, blank=True, null=True)
    thr28 = models.CharField(max_length=5, blank=True, null=True)
    thr29 = models.CharField(max_length=5, blank=True, null=True)
    thr30 = models.CharField(max_length=5, blank=True, null=True)
    thr31 = models.CharField(max_length=5, blank=True, null=True)
    otamt = models.FloatField()
    s1 = models.CharField(max_length=5, blank=True, null=True)
    s2 = models.CharField(max_length=5, blank=True, null=True)
    s3 = models.CharField(max_length=5, blank=True, null=True)
    s4 = models.CharField(max_length=5, blank=True, null=True)
    s5 = models.CharField(max_length=5, blank=True, null=True)
    s6 = models.CharField(max_length=5, blank=True, null=True)
    s7 = models.CharField(max_length=5, blank=True, null=True)
    s8 = models.CharField(max_length=5, blank=True, null=True)
    s9 = models.CharField(max_length=5, blank=True, null=True)
    s10 = models.CharField(max_length=5, blank=True, null=True)
    s11 = models.CharField(max_length=5, blank=True, null=True)
    s12 = models.CharField(max_length=5, blank=True, null=True)
    s13 = models.CharField(max_length=5, blank=True, null=True)
    s14 = models.CharField(max_length=5, blank=True, null=True)
    s15 = models.CharField(max_length=5, blank=True, null=True)
    s16 = models.CharField(max_length=5, blank=True, null=True)
    s17 = models.CharField(max_length=5, blank=True, null=True)
    s18 = models.CharField(max_length=5, blank=True, null=True)
    s19 = models.CharField(max_length=5, blank=True, null=True)
    s20 = models.CharField(max_length=5, blank=True, null=True)
    s21 = models.CharField(max_length=5, blank=True, null=True)
    s22 = models.CharField(max_length=5, blank=True, null=True)
    s23 = models.CharField(max_length=5, blank=True, null=True)
    s24 = models.CharField(max_length=5, blank=True, null=True)
    s25 = models.CharField(max_length=5, blank=True, null=True)
    s26 = models.CharField(max_length=5, blank=True, null=True)
    s27 = models.CharField(max_length=5, blank=True, null=True)
    s28 = models.CharField(max_length=5, blank=True, null=True)
    s29 = models.CharField(max_length=5, blank=True, null=True)
    s30 = models.CharField(max_length=5, blank=True, null=True)
    s31 = models.CharField(max_length=5, blank=True, null=True)
    salrate = models.FloatField()
    otrate = models.FloatField()
    inc = models.FloatField()

    class Meta:
        managed = False
        db_table = 'tbtimeh'
        app_label='Payroll_db'
        unique_together = (('emp_code', 'month_no'),)