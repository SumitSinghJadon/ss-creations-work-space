from django.db import models

class Invoice(models.Model):

    yr = models.CharField(db_column='Yr', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase. The composite primary key (Yr, Company, InvoiceNo) found, that is not supported. The first column is selected.
    invoiceno = models.CharField(db_column='InvoiceNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    company = models.IntegerField(db_column='Company')  # Field name made lowercase.
    prefix = models.CharField(max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    suffix = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    buyer = models.CharField(db_column='Buyer', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    agent = models.CharField(db_column='Agent', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    contractterm = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mode = models.CharField(db_column='Mode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dated = models.DateTimeField(blank=True, null=True)
    lcno = models.CharField(db_column='lcNo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    freight = models.FloatField(blank=True, null=True)
    insurence = models.FloatField(blank=True, null=True)
    commission = models.FloatField(blank=True, null=True)
    discount = models.FloatField(blank=True, null=True)
    othercharge = models.FloatField(db_column='otherCharge', blank=True, null=True)  # Field name made lowercase.
    invval = models.FloatField(db_column='invVal', blank=True, null=True)  # Field name made lowercase.
    frrs = models.FloatField(db_column='frRs', blank=True, null=True)  # Field name made lowercase.
    insrs = models.FloatField(db_column='insRs', blank=True, null=True)  # Field name made lowercase.
    commrs = models.FloatField(db_column='commRs', blank=True, null=True)  # Field name made lowercase.
    discrs = models.FloatField(db_column='discRs', blank=True, null=True)  # Field name made lowercase.
    otherrs = models.FloatField(db_column='otherRs', blank=True, null=True)  # Field name made lowercase.
    frexch = models.FloatField(db_column='frExch', blank=True, null=True)  # Field name made lowercase.
    insexch = models.FloatField(db_column='insExch', blank=True, null=True)  # Field name made lowercase.
    commexch = models.FloatField(db_column='commExch', blank=True, null=True)  # Field name made lowercase.
    disexch = models.FloatField(db_column='disExch', blank=True, null=True)  # Field name made lowercase.
    otherexch = models.FloatField(db_column='Otherexch', blank=True, null=True)  # Field name made lowercase.
    sbno = models.CharField(db_column='sbNo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    grno = models.CharField(db_column='grNo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sbdate = models.DateTimeField(db_column='sbDate', blank=True, null=True)  # Field name made lowercase.
    grdate = models.DateTimeField(db_column='grDate', blank=True, null=True)  # Field name made lowercase.
    postyear = models.CharField(db_column='PostYear', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    postinvno = models.CharField(db_column='PostInvNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rs = models.FloatField(db_column='Rs', blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datelastmodified = models.DateTimeField(blank=True, null=True)
    userlastmodified = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    totalqty = models.FloatField(db_column='TotalQty', blank=True, null=True)  # Field name made lowercase.
    fobvalue = models.FloatField(db_column='FOBValue', blank=True, null=True)  # Field name made lowercase.
    dbkamount = models.FloatField(db_column='DBKAmount', blank=True, null=True)  # Field name made lowercase.
    fobvaluefc = models.FloatField(db_column='FOBVALUEFC', blank=True, null=True)  # Field name made lowercase.
    fobvalueinword = models.CharField(db_column='FobValueInWord', max_length=155, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld1 = models.CharField(db_column='SCustomFld1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld2 = models.CharField(db_column='SCustomFld2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld3 = models.CharField(db_column='SCustomFld3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld4 = models.CharField(db_column='SCustomFld4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld5 = models.CharField(db_column='SCustomFld5', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    orderfromlc = models.BooleanField(db_column='OrderFromLC', blank=True, null=True)  # Field name made lowercase.
    shiptype = models.CharField(db_column='ShipType', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invreceipt = models.CharField(db_column='InvReceipt', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invvesflightno = models.CharField(db_column='InvVesFlightNo', max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invloading = models.CharField(db_column='InvLoading', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invdischarge = models.CharField(db_column='InvDischarge', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invfinaldestn = models.CharField(db_column='InvFinalDestn', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invcountryorigin = models.CharField(db_column='InvCountryOrigin', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invgrosswt = models.FloatField(db_column='InvGrossWt', blank=True, null=True)  # Field name made lowercase.
    invnetwt = models.FloatField(db_column='InvNetWt', blank=True, null=True)  # Field name made lowercase.
    shipto = models.CharField(db_column='ShipTo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invamtwords = models.CharField(db_column='InvAmtWords', max_length=155, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    perccomm = models.FloatField(db_column='PercComm', blank=True, null=True)  # Field name made lowercase.
    percdisc = models.FloatField(db_column='PercDisc', blank=True, null=True)  # Field name made lowercase.
    shipped = models.IntegerField(db_column='Shipped', blank=True, null=True)  # Field name made lowercase.
    printno = models.CharField(db_column='PrintNo', max_length=32, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    truckoffdate = models.DateTimeField(db_column='TruckoffDate', blank=True, null=True)  # Field name made lowercase.
    lcnoorg = models.CharField(db_column='LCNoOrg', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    paymentterm = models.CharField(db_column='PaymentTerm', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    homelocation = models.CharField(db_column='HomeLocation', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    consignee = models.CharField(db_column='Consignee', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invoicetype = models.CharField(db_column='InvoiceType', max_length=6, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    samplepaid = models.IntegerField(db_column='SamplePaid', blank=True, null=True)  # Field name made lowercase.
    hangerlc = models.FloatField(db_column='HangerLC', blank=True, null=True)  # Field name made lowercase.
    hangerexchrt = models.FloatField(db_column='HangerExchRt', blank=True, null=True)  # Field name made lowercase.
    hangerfc = models.FloatField(db_column='HangerFC', blank=True, null=True)  # Field name made lowercase.
    templatecode = models.CharField(db_column='TemplateCode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    buyerbank = models.CharField(db_column='BuyerBank', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    dbkacno = models.CharField(db_column='DBKAcNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    exporterbank = models.CharField(db_column='ExporterBank', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    currentacno = models.CharField(db_column='CurrentAcNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    marksfrom = models.CharField(db_column='MarksFrom', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    invhomelocation = models.CharField(db_column='InvHomeLocation', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld6 = models.CharField(db_column='SCustomFld6', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld7 = models.CharField(db_column='SCustomFld7', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld8 = models.CharField(db_column='SCustomFld8', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld9 = models.CharField(db_column='SCustomFld9', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld10 = models.CharField(db_column='SCustomFld10', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld11 = models.CharField(db_column='SCustomFld11', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld12 = models.CharField(db_column='SCustomFld12', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld13 = models.CharField(db_column='SCustomFld13', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld14 = models.CharField(db_column='SCustomFld14', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    scustomfld15 = models.CharField(db_column='ScustomFld15', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    noofpackages = models.CharField(db_column='NoOfPackages', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='Remarks', max_length=2000, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    rowid = models.BigAutoField(db_column='RowId',primary_key=True)  # Field name made lowercase.
    segment = models.CharField(db_column='Segment', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    prodfact = models.CharField(db_column='ProdFact', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    revisionno = models.IntegerField(db_column='RevisionNo', blank=True, null=True)  # Field name made lowercase.
    upcharge = models.FloatField(db_column='Upcharge', blank=True, null=True)  # Field name made lowercase.
    upchargelc = models.FloatField(db_column='UpchargeLC', blank=True, null=True)  # Field name made lowercase.
    upchargeper = models.FloatField(db_column='UpchargePer', blank=True, null=True)  # Field name made lowercase.
    upchargeexrate = models.FloatField(db_column='UpchargeExRate', blank=True, null=True)  # Field name made lowercase.
    ocname = models.CharField(db_column='OCName', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    ocper = models.FloatField(db_column='OCPer')  # Field name made lowercase.
    leodate = models.DateTimeField(db_column='LEODate', blank=True, null=True)  # Field name made lowercase.
    epcopy = models.DateTimeField(db_column='EPCopy', blank=True, null=True)  # Field name made lowercase.
    addbuildno = models.CharField(db_column='AddBuildNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    addmachno = models.CharField(db_column='AddMachNo', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    editbuildno = models.CharField(db_column='EditBuildNo', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    editmachno = models.CharField(db_column='EditMachNo', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tpcommper = models.FloatField(db_column='TPCommPer')  # Field name made lowercase.
    tpcommlc = models.FloatField(db_column='TPCommLC')  # Field name made lowercase.
    tpcommfc = models.FloatField(db_column='TPCommFC')  # Field name made lowercase.
    tpcommexrate = models.FloatField(db_column='TPCommExRate')  # Field name made lowercase.
    shiptoloc = models.CharField(db_column='ShipToLoc', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    shiptoaddrcode = models.BigIntegerField(db_column='ShipToAddrCode', blank=True, null=True)  # Field name made lowercase.
    erpcalcdbkamt = models.FloatField(db_column='ERPCalcDBKAmt')  # Field name made lowercase.
    newsbdbkamount = models.FloatField(db_column='NewSBDBKAmount')  # Field name made lowercase.
    newsbstamount = models.FloatField(db_column='NewSBSTAmount')  # Field name made lowercase.
    invoicefor = models.SmallIntegerField(db_column='InvoiceFor')  # Field name made lowercase.
    cbm = models.FloatField(db_column='CBM')  # Field name made lowercase.
    invoicefrom = models.SmallIntegerField(db_column='InvoiceFrom')  # Field name made lowercase.
    buyermultiaddcode = models.BigIntegerField(db_column='BuyerMultiAddCode')  # Field name made lowercase.
    consigneemultiaddcode = models.BigIntegerField(db_column='ConsigneeMultiAddCode')  # Field name made lowercase.
    ocbasedon = models.SmallIntegerField(db_column='OCBasedOn')  # Field name made lowercase.
    excper = models.FloatField(db_column='Excper')  # Field name made lowercase.
    excexrate = models.FloatField(db_column='ExcExRate')  # Field name made lowercase.
    excfc = models.FloatField(db_column='ExcFC')  # Field name made lowercase.
    exclc = models.FloatField(db_column='ExcLC')  # Field name made lowercase.
    excamt = models.FloatField(db_column='ExcAmt')  # Field name made lowercase.
    hdrmeisamt = models.FloatField(db_column='HdrMEISAmt')  # Field name made lowercase.
    destcountry = models.CharField(db_column='DestCountry', max_length=3, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sbroslamt = models.FloatField(db_column='SBROSLAmt')  # Field name made lowercase.
    invshortcode = models.CharField(db_column='InvShortCode', max_length=5, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    invtypelev = models.CharField(db_column='InvTypeLEV', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    gstbond = models.SmallIntegerField(db_column='GSTBond')  # Field name made lowercase.
    salesinvoiceno = models.CharField(db_column='SalesInvoiceNo', max_length=16, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    attachfilename = models.CharField(db_column='AttachFileName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sbrosctlamt = models.FloatField(db_column='SBRoSCTLAmt')  # Field name made lowercase.
    payreqdate = models.DateTimeField(db_column='PayReqDate', blank=True, null=True)  # Field name made lowercase.
    docsubdate = models.DateTimeField(db_column='DocSubDate', blank=True, null=True)  # Field name made lowercase.
    scustomfld16 = models.DateTimeField(db_column='SCustomFld16', blank=True, null=True)  # Field name made lowercase.
    scustomfld17 = models.DateTimeField(db_column='SCustomFld17', blank=True, null=True)  # Field name made lowercase.
    licsrno = models.BigIntegerField(db_column='LicSrNo')  # Field name made lowercase.
    advauthlicno = models.CharField(db_column='AdvAuthLicNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    invgstncode = models.CharField(db_column='InvGSTNCode', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    taxinvno = models.CharField(db_column='TaxInvNo', max_length=16, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    taxinvdate = models.DateTimeField(db_column='TaxInvDate', blank=True, null=True)  # Field name made lowercase.
    cancelled = models.SmallIntegerField(db_column='Cancelled')  # Field name made lowercase.
    leono = models.CharField(db_column='LEONo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    sbrotdepamt = models.FloatField(db_column='SBRoTDEPAmt')  # Field name made lowercase.
    erprosctlstateamt = models.FloatField(db_column='ERPRoSCTLStateAmt')  # Field name made lowercase.
    erprosctlcenteramt = models.FloatField(db_column='ERPRoSCTLCenterAmt')  # Field name made lowercase.
    erprodtepstateamt = models.FloatField(db_column='ERPRoDTEPStateAmt')  # Field name made lowercase.
    upchargename = models.CharField(db_column='UpChargeName', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Invoice'
        unique_together = (('yr', 'company', 'invoiceno'),)
        app_label = 'ERP_db'
 