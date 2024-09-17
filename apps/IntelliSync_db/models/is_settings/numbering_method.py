from django.db import models 
from datetime import datetime, date


class NumberingMethod(models.Model):
    name      = models.CharField(max_length=100, unique=True)
    code      = models.CharField(max_length=30, unique=True, null=True, blank=True)
    prefix    = models.CharField(max_length=30)
    suffix    = models.CharField(max_length=30)
    next_no   = models.PositiveBigIntegerField(default=1)
    day       = models.BooleanField(default=False)
    year      = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    separator = models.CharField(max_length=1, default='/')
    
    def __str__(self):
        return f"{self.name} | ({self.prefix}{self.separator}{self.suffix}{self.separator}{self.next_no})" 
    
    class Meta:
        db_table = 'numbering_method'
        app_label = 'IntelliSync_db'


    def get_current_financial_year(self):
        today = datetime.today()
        if today.month >= 4:  # Financial year starts from April
            start_date = datetime(today.year, 4, 1)
            end_date = datetime(today.year + 1, 3, 31)
        else:
            start_date = datetime(today.year - 1, 4, 1)
            end_date = datetime(today.year, 3, 31)

        return start_date.strftime('%y') + end_date.strftime('%y')


def get_next_number(code):
    obj = NumberingMethod.objects.get(code=code)
    next_no = 1

    if obj.day:
        today = date.today().strftime("%d%m%y")
        
        if today == obj.suffix:
            next_no = obj.next_no
            obj.next_no = next_no + 1
            print('1', next_no)

        else:
            obj.next_no = next_no
            obj.suffix = today
            print('2', next_no)

    elif obj.year:
        fn_year = obj.get_current_financial_year()
        print('3', next_no)

        if fn_year == obj.suffix:
            next_no = obj.next_no
            obj.next_no = next_no + 1
        else:
            obj.next_no = next_no
            obj.suffix = fn_year
    
    else:
        print('3', next_no)
        next_no = obj.next_no
        obj.next_no = next_no + 1
    
    obj.save()

    next_no = f"{obj.prefix}{obj.separator}{obj.suffix}{obj.separator}{obj.next_no}"
    print('F -> ', next_no)
    return next_no

