from django.db import models


class Style(models.Model):
    stylehdrid = models.BigAutoField(primary_key=True, unique=True, db_column='StyleHdrId')
    styleno = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    stylename = models.CharField(max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    styledesc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    location = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    source = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    itemcode = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    costmanf = models.FloatField(blank=True, null=True)
    saleprice = models.FloatField(blank=True, null=True)
    wholesaleprice = models.FloatField(db_column='WholeSalePrice', blank=True, null=True)
    mrp = models.FloatField(db_column='Mrp', blank=True, null=True)
    datecosted = models.DateTimeField(blank=True, null=True)
    minordqty = models.SmallIntegerField(blank=True, null=True)
    currencycosted = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datelastmodified = models.DateTimeField(blank=True, null=True)
    userlastmodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    currencyfld = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    currencyconvrate = models.FloatField(blank=True, null=True)
    segment = models.CharField(max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stylepicture = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stylepicture1 = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    othercost = models.FloatField(db_column='OtherCost', blank=True, null=True)
    complxfact = models.FloatField(db_column='ComplxFact', blank=True, null=True)
    buyer = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    season = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    brandname = models.CharField(db_column='BrandName', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stylefor = models.CharField(db_column='StyleFor', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    sizedistrtype = models.CharField(db_column='SizeDistrType', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    dismargin = models.FloatField(db_column='DisMargin', blank=True, null=True)
    retmargin = models.FloatField(db_column='RetMargin', blank=True, null=True)
    baserate = models.FloatField(db_column='BaseRate', blank=True, null=True)
    r1 = models.FloatField(db_column='R1', blank=True, null=True)
    r2 = models.FloatField(db_column='R2', blank=True, null=True)
    r3 = models.FloatField(db_column='R3', blank=True, null=True)
    r4 = models.FloatField(db_column='R4', blank=True, null=True)
    r5 = models.FloatField(db_column='R5', blank=True, null=True)
    r6 = models.FloatField(db_column='R6', blank=True, null=True)
    r7 = models.FloatField(db_column='R7', blank=True, null=True)
    r8 = models.FloatField(db_column='R8', blank=True, null=True)
    r9 = models.FloatField(db_column='R9', blank=True, null=True)
    r10 = models.FloatField(db_column='R10', blank=True, null=True)
    r11 = models.FloatField(db_column='R11', blank=True, null=True)
    r12 = models.FloatField(db_column='R12', blank=True, null=True)
    r13 = models.FloatField(db_column='R13', blank=True, null=True)
    r14 = models.FloatField(db_column='R14', blank=True, null=True)
    r15 = models.FloatField(db_column='R15', blank=True, null=True)
    r16 = models.FloatField(db_column='R16', blank=True, null=True)
    r17 = models.FloatField(db_column='R17', blank=True, null=True)
    r18 = models.FloatField(db_column='R18', blank=True, null=True)
    r19 = models.FloatField(db_column='R19', blank=True, null=True)
    r20 = models.FloatField(db_column='R20', blank=True, null=True)
    param1 = models.CharField(db_column='Param1', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    value1 = models.CharField(db_column='Value1', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    param2 = models.CharField(db_column='Param2', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    value2 = models.CharField(db_column='Value2', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    param3 = models.CharField(db_column='Param3', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    value3 = models.CharField(db_column='Value3', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    param4 = models.CharField(db_column='Param4', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    value4 = models.CharField(db_column='Value4', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    isexport = models.IntegerField(db_column='IsExport', blank=True, null=True)
    isdomestic = models.IntegerField(db_column='IsDomestic', blank=True, null=True)
    isinternal = models.IntegerField(db_column='IsInternal', blank=True, null=True)
    gmtsize = models.CharField(db_column='GmtSize', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    gsm = models.FloatField(db_column='GSM', blank=True, null=True)
    fabtemplate = models.CharField(db_column='FabTemplate', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    consunit = models.CharField(db_column='ConsUnit', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    consparam1 = models.CharField(db_column='ConsParam1', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    consparam2 = models.CharField(db_column='ConsParam2', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    consparam3 = models.CharField(db_column='ConsParam3', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    consparamval1 = models.FloatField(db_column='ConsParamVal1', blank=True, null=True)
    consparamval2 = models.FloatField(db_column='ConsParamVal2', blank=True, null=True)
    consparamval3 = models.FloatField(db_column='ConsParamVal3', blank=True, null=True)
    allow1 = models.FloatField(db_column='Allow1', blank=True, null=True)
    allow2 = models.FloatField(db_column='Allow2', blank=True, null=True)
    allow3 = models.FloatField(db_column='Allow3', blank=True, null=True)
    chartcode = models.CharField(db_column='ChartCode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remarks = models.CharField(db_column='REMARKS', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    attachfile = models.CharField(db_column='AttachFile', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    merchandiser = models.CharField(db_column='Merchandiser', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    appstatus = models.CharField(db_column='AppStatus', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    appdate = models.DateTimeField(db_column='AppDate', blank=True, null=True)
    locked = models.IntegerField(db_column='Locked', blank=True, null=True)
    lockedby = models.CharField(db_column='LockedBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    lockeddate = models.DateTimeField(db_column='LockedDate', blank=True, null=True)
    lockedremarks = models.CharField(db_column='LockedRemarks', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stylesmv = models.FloatField(db_column='StyleSMV', blank=True, null=True)
    styleyr = models.CharField(db_column='StyleYr', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    salesmargin = models.FloatField(db_column='SalesMargin')
    salesincrement = models.FloatField(db_column='SalesIncrement')
    sizeseries = models.CharField(db_column='SizeSeries', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    stylebarcode = models.CharField(db_column='StyleBarcode', max_length=12, db_collation='SQL_Latin1_General_CP1_CI_AS')
    styleeff = models.FloatField(db_column='StyleEff')
    salepriceon = models.SmallIntegerField(db_column='SalePriceOn')
    mrpwefdate = models.DateTimeField(db_column='MRPWefDate', blank=True, null=True)
    r21 = models.FloatField(db_column='R21')
    r22 = models.FloatField(db_column='R22')
    r23 = models.FloatField(db_column='R23')
    r24 = models.FloatField(db_column='R24')
    r25 = models.FloatField(db_column='R25')
    r26 = models.FloatField(db_column='R26')
    r27 = models.FloatField(db_column='R27')
    r28 = models.FloatField(db_column='R28')
    r29 = models.FloatField(db_column='R29')
    r30 = models.FloatField(db_column='R30')
    r31 = models.FloatField(db_column='R31')
    r32 = models.FloatField(db_column='R32')
    r33 = models.FloatField(db_column='R33')
    r34 = models.FloatField(db_column='R34')
    r35 = models.FloatField(db_column='R35')
    r36 = models.FloatField(db_column='R36')
    r37 = models.FloatField(db_column='R37')
    r38 = models.FloatField(db_column='R38')
    r39 = models.FloatField(db_column='R39')
    r40 = models.FloatField(db_column='R40')
    r41 = models.FloatField(db_column='R41')
    r42 = models.FloatField(db_column='R42')
    r43 = models.FloatField(db_column='R43')
    r44 = models.FloatField(db_column='R44')
    r45 = models.FloatField(db_column='R45')
    colorassortment = models.SmallIntegerField(db_column='ColorAssortment')
    costrevisionno = models.IntegerField(db_column='CostRevisionNo')
    revisionby = models.CharField(db_column='RevisionBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    revisiondate = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)
    costrevremarks = models.CharField(db_column='CostRevRemarks', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    printshortcode = models.CharField(db_column='PrintShortCode', max_length=2, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    attachfile2 = models.CharField(db_column='AttachFile2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    attachfile3 = models.CharField(db_column='AttachFile3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    printcodetwo = models.CharField(db_column='PrintCodeTwo', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS')
    composition = models.CharField(db_column='Composition', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    noofmachines = models.FloatField(db_column='NoOfMachines')
    setstyle = models.SmallIntegerField(db_column='SetStyle')
    stylegroup = models.CharField(db_column='StyleGroup', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    samplingstyleno = models.CharField(db_column='SamplingStyleNo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    styleprodsmv = models.FloatField(db_column='StyleProdSMV', blank=True, null=True)
    styleprodeff = models.FloatField(db_column='StyleProdEff', blank=True, null=True)
    sdbapprby = models.CharField(db_column='SDBApprBy', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    sdbappron = models.DateTimeField(db_column='SDBApprOn', blank=True, null=True)
    param5 = models.CharField(db_column='Param5', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    value5 = models.CharField(db_column='Value5', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    param6 = models.CharField(db_column='Param6', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    value6 = models.CharField(db_column='Value6', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    param7 = models.CharField(db_column='Param7', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    value7 = models.CharField(db_column='Value7', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    param8 = models.CharField(db_column='Param8', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    value8 = models.CharField(db_column='Value8', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')
    multicurr1 = models.CharField(db_column='MultiCurr1', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')
    multicurr2 = models.CharField(db_column='MultiCurr2', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')
    multiexrate1 = models.FloatField(db_column='MultiExRate1')
    multiexrate2 = models.FloatField(db_column='MultiExRate2')
    multisaleprice1 = models.FloatField(db_column='MultiSalePrice1')
    multisaleprice2 = models.FloatField(db_column='MultiSalePrice2')
    aliasstyleno = models.CharField(db_column='AliasStyleNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    multisalepricem1 = models.FloatField(db_column='MultiSalePriceM1')
    multisalepricem2 = models.FloatField(db_column='MultiSalePriceM2')

    class Meta:
        managed = False
        app_label = 'ERP_db'
        db_table = 'Style'

