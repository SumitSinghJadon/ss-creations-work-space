from django.views import View
from django.shortcuts import redirect, render
# from IntelliSync_db.models import CommonMaster
# import IS_Nexus
from Payroll_db.models import TimeMaster, EmployeeMaster
from django.db.models import F

class Dashboard(View):
    def get(self, request):
        data = EmployeeMaster.objects.filter(time_master_emp_code__month_no='9').annotate(
            idt1= F('time_master_emp_code__idt1'),
            idt2= F('time_master_emp_code__idt2'),
            idt3= F('time_master_emp_code__idt3'),
            idt4= F('time_master_emp_code__idt4'),
            idt5= F('time_master_emp_code__idt5'),
            idt6= F('time_master_emp_code__idt6'),
            idt7= F('time_master_emp_code__idt7'),
            idt8= F('time_master_emp_code__idt8'),
            idt9= F('time_master_emp_code__idt9'),
            idt10= F('time_master_emp_code__idt10'),
            idt11= F('time_master_emp_code__idt11'),
            idt12= F('time_master_emp_code__idt12'),
            idt13= F('time_master_emp_code__idt13'),
            idt14= F('time_master_emp_code__idt14'),
            idt15= F('time_master_emp_code__idt15'),
            idt16= F('time_master_emp_code__idt16'),
            idt17= F('time_master_emp_code__idt17'),
            idt18= F('time_master_emp_code__idt18'),
            idt19= F('time_master_emp_code__idt19'),
            idt20= F('time_master_emp_code__idt20'),
            idt21= F('time_master_emp_code__idt21'),
            idt22= F('time_master_emp_code__idt22'),
            idt23= F('time_master_emp_code__idt23'),
            idt24= F('time_master_emp_code__idt24'),
            idt25= F('time_master_emp_code__idt25'),
            idt26= F('time_master_emp_code__idt26'),
            idt27= F('time_master_emp_code__idt27'),
            idt28= F('time_master_emp_code__idt28'),
            idt29= F('time_master_emp_code__idt29'),
            idt30= F('time_master_emp_code__idt30'),
            idt31= F('time_master_emp_code__idt31'),
            odt1= F('time_master_emp_code__odt1'),
            odt2= F('time_master_emp_code__odt2'),
            odt3= F('time_master_emp_code__odt3'),
            odt4= F('time_master_emp_code__odt4'),
            odt5= F('time_master_emp_code__odt5'),
            odt6= F('time_master_emp_code__odt6'),
            odt7= F('time_master_emp_code__odt7'),
            odt8= F('time_master_emp_code__odt8'),
            odt9= F('time_master_emp_code__odt9'),
            odt10= F('time_master_emp_code__odt10'),
            odt11= F('time_master_emp_code__odt11'),
            odt12= F('time_master_emp_code__odt12'),
            odt13= F('time_master_emp_code__odt13'),
            odt14= F('time_master_emp_code__odt14'),
            odt15= F('time_master_emp_code__odt15'),
            odt16= F('time_master_emp_code__odt16'),
            odt17= F('time_master_emp_code__odt17'),
            odt18= F('time_master_emp_code__odt18'),
            odt19= F('time_master_emp_code__odt19'),
            odt20= F('time_master_emp_code__odt20'),
            odt21= F('time_master_emp_code__odt21'),
            odt22= F('time_master_emp_code__odt22'),
            odt23= F('time_master_emp_code__odt23'),
            odt24= F('time_master_emp_code__odt24'),
            odt25= F('time_master_emp_code__odt25'),
            odt26= F('time_master_emp_code__odt26'),
            odt27= F('time_master_emp_code__odt27'),
            odt28= F('time_master_emp_code__odt28'),
            odt29= F('time_master_emp_code__odt29'),
            odt30= F('time_master_emp_code__odt30'),
            odt31= F('time_master_emp_code__odt31'),
        ).values(
            'emp_code', 'emp_cardno', 'emp_name',
            'resign', 'idt1', 'idt2', 'idt3', 'idt4', 'idt5', 'idt6', 'idt7', 'idt8', 'idt9', 'idt10',
            'idt11', 'idt12', 'idt13', 'idt14', 'idt15', 'idt16', 'idt17', 'idt18', 'idt19', 'idt20',
            'idt21', 'idt22', 'idt23', 'idt24', 'idt25', 'idt26', 'idt27', 'idt28', 'idt29', 'idt30', 'idt31',
            'odt1', 'odt2', 'odt3', 'odt4', 'odt5', 'odt6', 'odt7', 'odt8', 'odt9', 'odt10', 'odt11', 'odt12',
            'odt13', 'odt14', 'odt15', 'odt16', 'odt17', 'odt18', 'odt19', 'odt20', 'odt21', 'odt22', 'odt23',
            'odt24', 'odt25', 'odt26', 'odt27', 'odt28', 'odt29', 'odt30', 'odt31'
        ).order_by('emp_code').filter(emp_code='220').filter(emp_code='221').using('payroll_db')
        

        return render(request, 'dashboard.html')

