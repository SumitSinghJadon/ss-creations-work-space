from django.db import models

class ImageMaster(models.Model):
  image1 = models.ImageField(upload_to='assets/media/')
  image2 = models.ImageField(upload_to='assets/media/')
  buyer = models.CharField(max_length=50)
  style = models.CharField(max_length=120)
  
  def __str__(self):
    return self.ourref_no