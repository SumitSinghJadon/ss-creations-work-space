from django.db import models


class Color(models.Model):
    colorid = models.BigAutoField(primary_key=True, unique=True, db_column='ColorId')
    itemtype = models.CharField(db_column='ItemType', max_length=1, db_collation='SQL_Latin1_General_CP1_CI_AS')
    color = models.CharField(db_column='Color', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS')
    datecreated = models.DateTimeField(blank=True, null=True)
    usercreated = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    datelastmodified = models.DateTimeField(blank=True, null=True)
    userlastmodified = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    colorgrp = models.CharField(db_column='ColorGrp', max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    active = models.BooleanField(db_column='Active')
    alltypes = models.SmallIntegerField(db_column='AllTypes')

    class Meta:
        managed = False
        db_table = 'Color'
        app_label = 'ERP_db'
        unique_together = (('itemtype', 'color'),)

