from django.db import models

class Expolot(models.Model):
    ourref = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    lotno = models.SmallIntegerField(blank=True, null=True)
    delvdate = models.DateTimeField(blank=True, null=True)
    destination = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    country = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    category = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mode = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    expdcurr = models.IntegerField(blank=True, null=True)
    totalqty = models.IntegerField(blank=True, null=True)
    totalamt = models.FloatField(blank=True, null=True)
    costref = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    curr = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    qtyorperwise = models.CharField(db_column='QtyOrPerWise', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datemodified = models.DateTimeField(blank=True, null=True)
    usermodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remarks = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    buyref = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    baserate = models.FloatField(blank=True, null=True)
    pi1 = models.FloatField(blank=True, null=True)
    pi2 = models.FloatField(blank=True, null=True)
    pi3 = models.FloatField(blank=True, null=True)
    pi4 = models.FloatField(blank=True, null=True)
    pi5 = models.FloatField(blank=True, null=True)
    pi6 = models.FloatField(blank=True, null=True)
    pi7 = models.FloatField(blank=True, null=True)
    pi8 = models.FloatField(blank=True, null=True)
    pi9 = models.FloatField(blank=True, null=True)
    pi10 = models.FloatField(blank=True, null=True)
    pi11 = models.FloatField(blank=True, null=True)
    pi12 = models.FloatField(blank=True, null=True)
    pi13 = models.FloatField(blank=True, null=True)
    pi14 = models.FloatField(blank=True, null=True)
    pi15 = models.FloatField(blank=True, null=True)
    pi16 = models.FloatField(blank=True, null=True)
    pi17 = models.FloatField(blank=True, null=True)
    pi18 = models.FloatField(blank=True, null=True)
    pi19 = models.FloatField(blank=True, null=True)
    pi20 = models.FloatField(blank=True, null=True)
    pi21 = models.FloatField(blank=True, null=True)
    pi22 = models.FloatField(blank=True, null=True)
    pi23 = models.FloatField(blank=True, null=True)
    pi24 = models.FloatField(blank=True, null=True)
    pi25 = models.FloatField(blank=True, null=True)
    pi26 = models.FloatField(blank=True, null=True)
    pi27 = models.FloatField(blank=True, null=True)
    pi28 = models.FloatField(blank=True, null=True)
    pi29 = models.FloatField(blank=True, null=True)
    pi30 = models.FloatField(blank=True, null=True)
    exdelvdate = models.DateTimeField(db_column='ExDelvDate', blank=True, null=True)  # Field name made lowercase.
    agegroup = models.CharField(db_column='AgeGroup', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pcddate = models.DateTimeField(db_column='PCDDate', blank=True, null=True)  # Field name made lowercase.
    tnano = models.IntegerField(db_column='TNANo', blank=True, null=True)  # Field name made lowercase.
    eoyr = models.CharField(db_column='EOYr', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    canceldate = models.DateTimeField(db_column='CancelDate', blank=True, null=True)  # Field name made lowercase.
    edgisbookid = models.CharField(db_column='EDGISBookID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        app_label = 'ERP_db'
        db_table = 'ExpoLot'
