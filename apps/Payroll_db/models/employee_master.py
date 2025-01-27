from django.db import models
from .department_master import DepartmentMaster
from .designation_master import DesignationMaster


class EmployeeMaster(models.Model):
    emp_code = models.BigIntegerField(unique=True,primary_key=True, db_column='emp_code')
    dep_code = models.ForeignKey(DepartmentMaster,on_delete=models.DO_NOTHING,db_constraint=False, db_column='dep_code')
    des_code = models.ForeignKey(DesignationMaster,on_delete=models.DO_NOTHING,db_constraint=False, db_column='des_code')
    emp_paycode = models.CharField(unique=True, max_length=10, blank=True, null=True)
    emp_cardno = models.CharField(max_length=10, blank=True, null=True)
    emp_name = models.CharField(max_length=300, blank=True, null=True)
    emp_fname = models.CharField(max_length=300, blank=True, null=True)
    emp_mname = models.CharField(max_length=300, blank=True, null=True)
    emp_wname = models.CharField(max_length=300, blank=True, null=True)
    emp_dob = models.DateTimeField(blank=True, null=True)
    emp_mdate = models.DateTimeField(blank=True, null=True)
    emp_phn = models.CharField(max_length=20, blank=True, null=True)
    emp_email = models.CharField(max_length=20, blank=True, null=True)
    emp_pann = models.CharField(max_length=25, blank=True, null=True)
    emp_dln = models.CharField(max_length=25, blank=True, null=True)
    emp_passn = models.CharField(max_length=25, blank=True, null=True)
    emp_marks = models.CharField(max_length=35, blank=True, null=True)
    emp_handi = models.CharField(max_length=35, blank=True, null=True)
    emp_sex = models.SmallIntegerField()
    emp_marital = models.SmallIntegerField()
    emp_bg = models.SmallIntegerField()
    emp_relg = models.SmallIntegerField()
    emp_height = models.CharField(max_length=10, blank=True, null=True)
    emp_weight = models.CharField(max_length=10, blank=True, null=True)
    emp_edu = models.CharField(max_length=300, blank=True, null=True)
    emp_teq = models.CharField(max_length=300, blank=True, null=True)
    emp_ladd = models.CharField(max_length=100, blank=True, null=True)
    emp_padd = models.CharField(max_length=100, blank=True, null=True)
    emp_remarks = models.CharField(max_length=30, blank=True, null=True)
    emp_act = models.SmallIntegerField()
    emp_spl = models.IntegerField()
    emp_doj = models.DateTimeField(blank=True, null=True)
    emp_doc = models.DateTimeField(blank=True, null=True)
    cmp_code = models.BigIntegerField()
    sub_code = models.IntegerField()
    loc_code = models.IntegerField()
    dhead_code = models.IntegerField()
    cat_code = models.IntegerField()
    sal_code = models.IntegerField()
    leave_code = models.IntegerField()
    shift_code = models.IntegerField()
    shift_type = models.IntegerField()
    wk_off = models.IntegerField()
    ext_off = models.IntegerField()
    punch_type = models.IntegerField()
    rel_any = models.CharField(max_length=30, blank=True, null=True)
    emp_vip = models.SmallIntegerField()
    doj_p = models.SmallIntegerField()
    totsal = models.FloatField()
    totsal1 = models.FloatField()
    food1 = models.FloatField()
    food2 = models.FloatField()
    food_alw = models.SmallIntegerField()
    tea1 = models.FloatField()
    tea2 = models.FloatField()
    tea_alw = models.SmallIntegerField()
    incent1 = models.FloatField()
    incent2 = models.FloatField()
    incent_alw = models.SmallIntegerField()
    conv1 = models.FloatField()
    conv2 = models.FloatField()
    conv_alw = models.SmallIntegerField()
    add_s1 = models.FloatField()
    add_s2 = models.FloatField()
    add_s_alw = models.SmallIntegerField()
    night1 = models.FloatField()
    night2 = models.FloatField()
    night_alw = models.SmallIntegerField()
    sales1 = models.FloatField()
    sales2 = models.FloatField()
    sales_alw = models.SmallIntegerField()
    bonus_per = models.FloatField()
    bonus_min = models.FloatField()
    bonus_max = models.FloatField()
    bonus_alw = models.SmallIntegerField()
    ex_gratia = models.SmallIntegerField()
    ot_type = models.IntegerField()
    ot_rate = models.SmallIntegerField()
    ot_limit = models.FloatField()
    ot_alw = models.SmallIntegerField()
    bus_amt = models.FloatField()
    bus_alw = models.SmallIntegerField()
    lwf_app = models.SmallIntegerField()
    late_app = models.SmallIntegerField()
    ptax_app = models.SmallIntegerField()
    sal_mode = models.SmallIntegerField()
    pay_mode = models.SmallIntegerField()
    bank_code = models.SmallIntegerField()
    bankac_no = models.CharField(max_length=30, blank=True, null=True)
    bank_br = models.CharField(max_length=30, blank=True, null=True)
    ifsc_no = models.CharField(max_length=20, blank=True, null=True)
    cid_no = models.CharField(max_length=20, blank=True, null=True)
    pf_alw = models.SmallIntegerField()
    pf1_alw = models.SmallIntegerField()
    pfel_lmt_ignr = models.SmallIntegerField()
    pf_el_lmt = models.FloatField()
    pfper_elignr = models.SmallIntegerField()
    pfper_el = models.FloatField()
    pfer_lmt_ignr = models.SmallIntegerField()
    pf_er_lmt = models.FloatField()
    pfper_erignr = models.SmallIntegerField()
    pfper_er = models.FloatField()
    pf_no = models.CharField(max_length=25, blank=True, null=True)
    old_pfno = models.CharField(max_length=25, blank=True, null=True)
    epf_nomm = models.CharField(max_length=25, blank=True, null=True)
    epf_nommadd = models.CharField(max_length=80, blank=True, null=True)
    esi_alw = models.SmallIntegerField()
    esi1_alw = models.SmallIntegerField()
    esi_no = models.CharField(max_length=25, blank=True, null=True)
    esi_lmt = models.FloatField()
    esi_ot = models.SmallIntegerField()
    emp_dol = models.DateTimeField(blank=True, null=True)
    resign = models.IntegerField()
    f_final = models.IntegerField()
    esiamt = models.FloatField()
    pfamt = models.FloatField()
    pframt = models.FloatField()
    tmp_att = models.SmallIntegerField()
    tmp_pesi = models.SmallIntegerField()
    tmp_sal = models.SmallIntegerField()
    disp_esi = models.CharField(max_length=60, blank=True, null=True)
    sal_mode1 = models.IntegerField()
    stype = models.IntegerField()
    reason = models.CharField(max_length=40, blank=True, null=True)
    oel = models.FloatField()
    ocl = models.FloatField()
    osl = models.FloatField()
    eel = models.FloatField()
    ecl = models.FloatField()
    esl = models.FloatField() 
    eedu = models.IntegerField()
    etedu = models.IntegerField()
    tempdt = models.DateTimeField(blank=True, null=True)
    pad1 = models.CharField(max_length=50, blank=True, null=True)
    pad2 = models.CharField(max_length=35, blank=True, null=True)
    pcity = models.CharField(max_length=35, blank=True, null=True)
    pdist = models.CharField(max_length=35, blank=True, null=True)
    pstate = models.CharField(max_length=35, blank=True, null=True)
    ppin = models.CharField(max_length=11, blank=True, null=True)
    mob = models.CharField(max_length=15, blank=True, null=True)
    pass_dtf = models.DateTimeField(blank=True, null=True)
    pass_dtt = models.DateTimeField(blank=True, null=True)
    old_empr_no = models.CharField(max_length=30, blank=True, null=True)
    adhar_no = models.CharField(max_length=20, blank=True, null=True)
    dl_exp_dt = models.DateTimeField(blank=True, null=True)
    kyc_name = models.CharField(max_length=100, blank=True, null=True)
    dtl_oldemp = models.CharField(max_length=10, blank=True, null=True)
    intw_wo = models.IntegerField()
    edu_id = models.IntegerField()
    edu_doc_sym = models.CharField(max_length=1, blank=True, null=True)
    pf_bank_no = models.CharField(max_length=30, blank=True, null=True)
    pfb_ifsc = models.CharField(max_length=30, blank=True, null=True)
    handi_id = models.IntegerField()
    handi_yn = models.IntegerField()
    handi_sym = models.CharField(max_length=1, blank=True, null=True)
    elc_card = models.CharField(max_length=30, blank=True, null=True)
    ration_card = models.CharField(max_length=30, blank=True, null=True)
    submit_yn = models.IntegerField()
    npr_no = models.CharField(max_length=30, blank=True, null=True)
    pan_kyc = models.CharField(max_length=150, blank=True, null=True)
    adhar_kyc = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbemp'
        app_label = 'Payroll_db'

    def __str__(self):
        return self.emp_name