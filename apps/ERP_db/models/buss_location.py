from django.db import models

class Busslocation(models.Model):
    busslocatcode = models.CharField(db_column='BussLocatCode', primary_key=True, max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    busslocatname = models.CharField(db_column='BussLocatName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    blocatshortcode = models.CharField(db_column='BLocatShortCode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    blocattype = models.CharField(db_column='BLocatType', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address1 = models.CharField(db_column='Address1', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address2 = models.CharField(db_column='Address2', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address3 = models.CharField(db_column='Address3', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    address4 = models.CharField(db_column='Address4', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone1 = models.CharField(db_column='Phone1', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    phone2 = models.CharField(db_column='Phone2', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='Mobile', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pager = models.CharField(db_column='Pager', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    userlastmodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datelastmodified = models.DateTimeField(blank=True, null=True)
    contact = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    shortcode = models.CharField(max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    frmname = models.CharField(db_column='FrmName', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invoiceshortcode = models.CharField(db_column='InvoiceShortCode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    curr = models.CharField(db_column='Curr', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    designnoshortcode = models.CharField(db_column='DesignNoShortCode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    firstweekoff = models.IntegerField(db_column='FirstWeekoff')  # Field name made lowercase.
    businessgroup = models.CharField(db_column='BusinessGroup', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    statesrno = models.BigIntegerField(db_column='StateSrno')  # Field name made lowercase.
    gstno = models.CharField(db_column='GSTNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    issez = models.SmallIntegerField(db_column='IsSEZ')  # Field name made lowercase.
    # busslocid = models.AutoField(db_column='BussLocId')  # Field name made lowercase.
    deffloc = models.CharField(db_column='DefFLoc', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    defaloc = models.CharField(db_column='DefALoc', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    defyloc = models.CharField(db_column='DefYLoc', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    defggloc = models.CharField(db_column='DefGGLoc', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    defgarloc = models.CharField(db_column='DefGarLoc', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BussLocation'
        app_label = 'ERP_db'