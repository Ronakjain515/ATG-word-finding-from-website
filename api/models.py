from django.db import models

# Create your models here.
class urls_data(models.Model):
    url = models.CharField(max_length=200)

class keywords(models.Model):
    urlId = models.ForeignKey(urls_data, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=100)
    frequency = models.IntegerField()