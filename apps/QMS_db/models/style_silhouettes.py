from django.db import models

class StyleSilhouettes(models.Model):
    front_image = models.ImageField(upload_to='assets/media/sketches')
    back_image = models.ImageField(upload_to='assets/media/sketches')
    buyer = models.CharField(max_length=50)
    style_no = models.CharField(max_length=120)
    
    def __str__(self):
        return self.buyer

    class Meta:
        unique_together = ('buyer','style_no')
        app_label = 'QMS_db'
        db_table = 'style_silhouettes'