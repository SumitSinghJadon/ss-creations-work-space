from IntelliSync_db.models import User
from django.db import models
# from ..location_master import LocationMaster


class LocationPermission(models.Model):
    location = models.ForeignKey("LocationMaster", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'location_permission'
        app_label = 'IntelliSync_db'

