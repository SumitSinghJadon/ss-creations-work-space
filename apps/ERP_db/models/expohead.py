from django.db import models

class OrderStMt(models.Model):
    order_no = models.CharField(primary_key=True,db_column="ourref", max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    orderdate = models.DateTimeField(blank=True, null=True)
    buyer = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    buyord = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    firm = models.IntegerField(blank=True, null=True)
    segment = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    closed = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    agent = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    merchandiser = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    extraallowed = models.FloatField(db_column='ExtraAllowed', blank=True, null=True)  # Field name made lowercase.
    season = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    paymentterms = models.CharField(max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    runit = models.CharField(db_column='rUnit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    qunit = models.CharField(db_column='qUnit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    planname = models.CharField(db_column='PlanName', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    deliveryterms = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ratiobased = models.BooleanField(blank=True, null=True)
    r1 = models.SmallIntegerField(blank=True, null=True)
    r2 = models.SmallIntegerField(blank=True, null=True)
    r3 = models.SmallIntegerField(blank=True, null=True)
    r4 = models.SmallIntegerField(blank=True, null=True)
    r5 = models.SmallIntegerField(blank=True, null=True)
    r6 = models.SmallIntegerField(blank=True, null=True)
    r7 = models.SmallIntegerField(blank=True, null=True)
    r8 = models.SmallIntegerField(blank=True, null=True)
    r9 = models.SmallIntegerField(blank=True, null=True)
    r10 = models.SmallIntegerField(blank=True, null=True)
    r11 = models.SmallIntegerField(blank=True, null=True)
    r12 = models.SmallIntegerField(blank=True, null=True)
    r13 = models.SmallIntegerField(blank=True, null=True)
    r14 = models.SmallIntegerField(blank=True, null=True)
    r15 = models.SmallIntegerField(blank=True, null=True)
    r16 = models.SmallIntegerField(blank=True, null=True)
    r17 = models.SmallIntegerField(blank=True, null=True)
    r18 = models.SmallIntegerField(blank=True, null=True)
    r19 = models.SmallIntegerField(blank=True, null=True)
    r20 = models.SmallIntegerField(blank=True, null=True)
    r21 = models.SmallIntegerField(blank=True, null=True)
    r22 = models.SmallIntegerField(blank=True, null=True)
    r23 = models.SmallIntegerField(blank=True, null=True)
    r24 = models.SmallIntegerField(blank=True, null=True)
    r25 = models.SmallIntegerField(blank=True, null=True)
    r26 = models.SmallIntegerField(blank=True, null=True)
    r27 = models.SmallIntegerField(blank=True, null=True)
    r28 = models.SmallIntegerField(blank=True, null=True)
    r29 = models.SmallIntegerField(blank=True, null=True)
    r30 = models.SmallIntegerField(blank=True, null=True)
    packingtype = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pcsperctn = models.SmallIntegerField(blank=True, null=True)
    noofctn = models.SmallIntegerField(blank=True, null=True)
    shippingmarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    foldinginstructions = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    avgrateperpc = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    totalpcs = models.FloatField(blank=True, null=True)
    notepad = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datelastmodified = models.DateTimeField(blank=True, null=True)
    userlastmodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ordertype = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sizetype = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    costref = models.CharField(db_column='Costref', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cur = models.CharField(db_column='Cur', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    closeddate = models.DateTimeField(db_column='ClosedDate', blank=True, null=True)  # Field name made lowercase.
    closedremark = models.CharField(db_column='ClosedRemark', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    closedby = models.CharField(db_column='ClosedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    garmentrejection = models.FloatField(db_column='GarmentRejection', blank=True, null=True)  # Field name made lowercase.
    washtype = models.CharField(db_column='WashType', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    locked = models.BooleanField(db_column='Locked', blank=True, null=True)  # Field name made lowercase.
    lockdate = models.DateTimeField(db_column='LockDate', blank=True, null=True)  # Field name made lowercase.
    customfld1 = models.CharField(db_column='CustomFld1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld2 = models.CharField(db_column='CustomFld2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld3 = models.CharField(db_column='CustomFld3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld4 = models.CharField(db_column='CustomFld4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld5 = models.CharField(db_column='CustomFld5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    buydiv = models.CharField(db_column='BuyDiv', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    buydep = models.CharField(db_column='BuyDep', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    importedfab = models.BooleanField(db_column='ImportedFab', blank=True, null=True)  # Field name made lowercase.
    exchangerate = models.FloatField(db_column='ExchangeRate', blank=True, null=True)  # Field name made lowercase.
    isprepack = models.IntegerField(db_column='IsPrePack', blank=True, null=True)  # Field name made lowercase.
    isprepackcomplete = models.IntegerField(db_column='IsPrePackComplete', blank=True, null=True)  # Field name made lowercase.
    salesordertype = models.CharField(db_column='SalesOrderType', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    isincomplete = models.IntegerField(db_column='IsIncomplete', blank=True, null=True)  # Field name made lowercase.
    prodcenter = models.CharField(db_column='ProdCenter', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    generalinstruction = models.TextField(db_column='GeneralInstruction', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    embroinstruction = models.TextField(db_column='EmbroInstruction', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    shiptype = models.CharField(db_column='ShipType', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    homelocation = models.CharField(db_column='HomeLocation', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    inccanitem = models.IntegerField(db_column='IncCanItem', blank=True, null=True)  # Field name made lowercase.
    shipfrom = models.CharField(db_column='ShipFrom', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld6 = models.CharField(db_column='customFld6', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld7 = models.CharField(db_column='customFld7', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld8 = models.CharField(db_column='customFld8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld9 = models.CharField(db_column='customFld9', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld10 = models.CharField(db_column='customFld10', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld11 = models.CharField(db_column='customFld11', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld12 = models.CharField(db_column='customFld12', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld13 = models.CharField(db_column='customFld13', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld14 = models.CharField(db_column='customFld14', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld15 = models.CharField(db_column='customFld15', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addbuildno = models.CharField(db_column='AddBuildNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    editbuildno = models.CharField(db_column='EditBuildNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    addmachno = models.CharField(db_column='AddMachNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    editmachno = models.CharField(db_column='EditMachNo', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prodapprv = models.IntegerField(db_column='ProdApprv', blank=True, null=True)  # Field name made lowercase.
    ordergroup = models.CharField(db_column='OrderGroup', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    customfld16 = models.DateTimeField(db_column='CustomFld16', blank=True, null=True)  # Field name made lowercase.
    customfld17 = models.DateTimeField(db_column='CustomFld17', blank=True, null=True)  # Field name made lowercase.
    eoyr = models.CharField(db_column='EOYr', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sampletype = models.CharField(db_column='SampleType', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    agentcomm = models.FloatField(db_column='AgentComm')  # Field name made lowercase.
    marketper = models.CharField(db_column='MarketPer', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    bomlocked = models.SmallIntegerField(db_column='BOMLOCKED')  # Field name made lowercase.
    revisionno = models.SmallIntegerField(db_column='REVISIONNO')  # Field name made lowercase.
    sentforapprv = models.SmallIntegerField(db_column='SentForApprv', blank=True, null=True)  # Field name made lowercase.
    sentapprvby = models.CharField(db_column='SentApprvBY', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sentapprvdate = models.DateTimeField(db_column='SentApprvDate', blank=True, null=True)  # Field name made lowercase.
    buyeraddcode = models.BigIntegerField(db_column='BuyerAddCode', blank=True, null=True)  # Field name made lowercase.
    pricecateg = models.CharField(db_column='PriceCateg', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    couriercompany = models.CharField(db_column='CourierCompany', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    garrejectslabwise = models.SmallIntegerField(db_column='GarRejectSlabwise')  # Field name made lowercase.
    closededitdate = models.DateTimeField(db_column='ClosedEditDate', blank=True, null=True)  # Field name made lowercase.
    pocountrybom = models.CharField(db_column='POCountryBOM', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    raterevremarks = models.CharField(db_column='RateRevRemarks', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rateoption = models.SmallIntegerField(db_column='RateOption')  # Field name made lowercase.
    printarea = models.CharField(db_column='PrintArea', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    printtype = models.CharField(db_column='PrintType', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    gisbookid = models.CharField(db_column='GISBookID', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    # ourrefid = models.BigAutoField(db_column='OurrefID')  # Field name made lowercase.
    ratiopack = models.SmallIntegerField(db_column='RatioPack')  # Field name made lowercase.
    copiedfromourref = models.CharField(db_column='CopiedFromOurRef', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ratechangeprepack = models.SmallIntegerField(db_column='RateChangePrePack')  # Field name made lowercase.
    isapiuploaded = models.IntegerField(db_column='IsAPIUploaded')  # Field name made lowercase.
    orderapiid = models.BigIntegerField(db_column='OrderAPIID')  # Field name made lowercase.
    garrejslabwise = models.FloatField(db_column='GarRejSlabWise')  # Field name made lowercase.

    class Meta:
        managed = False
        app_label = 'ERP_db'
        db_table = 'ExpoHead'