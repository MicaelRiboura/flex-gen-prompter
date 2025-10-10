from django.db import models

# Create your models here.
class Dataset(models.Model):
    name = models.CharField(max_length=255, unique=True)
    filename = models.CharField(max_length=255, unique=True)
    
    class Meta:
        verbose_name = 'dataset'
        verbose_name_plural = 'datasets'
    
    def __str__(self):
        return self.name