from django.db import models


class Expohead(models.Model):
    ourref = models.CharField(primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    orderdate = models.DateTimeField(blank=True, null=True)
    buyer = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    buyord = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    firm = models.IntegerField(blank=True, null=True)
    segment = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    closed = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    agent = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    merchandiser = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    extraallowed = models.FloatField(db_column='ExtraAllowed', blank=True, null=True)
    season = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    paymentterms = models.CharField(max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    runit = models.CharField(db_column='rUnit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    qunit = models.CharField(db_column='qUnit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    planname = models.CharField(db_column='PlanName', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    deliveryterms = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ratiobased = models.BooleanField(blank=True, null=True)
    r1 = models.SmallIntegerField(blank=True, null=True)
    r2 = models.SmallIntegerField(blank=True, null=True)


    class Meta:
        managed = False  
        db_table = 'ExpoHead'


class Expolotdet(models.Model):
    ourref = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    styleno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    color = models.CharField(max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    totalqty = models.FloatField(blank=True, null=True)
    totalamt = models.FloatField(blank=True, null=True)
    shipped = models.FloatField(db_column='Shipped', blank=True, null=True)
    balance = models.FloatField(db_column='Balance', blank=True, null=True)
    s1 = models.FloatField(blank=True, null=True)
    s2 = models.FloatField(blank=True, null=True)
    s3 = models.FloatField(blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datemodified = models.DateTimeField(blank=True, null=True)
    usermodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExpoLotDet'


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
    qtyorperwise = models.CharField(db_column='QtyOrPerWise', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datemodified = models.DateTimeField(blank=True, null=True)
    usermodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remarks = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    buyref = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    baserate = models.FloatField(blank=True, null=True)
    pi1 = models.FloatField(blank=True, null=True)
    pi2 = models.FloatField(blank=True, null=True)
    # Define other fields as per your schema...

    # Additional fields not present in the provided schema but required in Django model
    exdelvdate = models.DateTimeField(db_column='ExDelvDate', blank=True, null=True)
    agegroup = models.CharField(db_column='AgeGroup', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pcddate = models.DateTimeField(db_column='PCDDate', blank=True, null=True)
    tnano = models.IntegerField(db_column='TNANo', blank=True, null=True)
    eoyr = models.CharField(db_column='EOYr', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    canceldate = models.DateTimeField(db_column='CancelDate', blank=True, null=True)
    edgisbookid = models.CharField(db_column='EDGISBookID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExpoLot'









