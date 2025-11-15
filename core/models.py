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
    
class Prompt(models.Model):
    technique = models.CharField(max_length=255)
    dataset = models.CharField(max_length=255)
    node = models.CharField(max_length=255)
    prompt = models.TextField()
    
    class Meta:
        verbose_name = 'prompt'
        verbose_name_plural = 'prompts'
        unique_together = ('technique', 'dataset', 'node')