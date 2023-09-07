from django.db import models
# Create your models here.
class Twitter(models.Model):
    date = models.DateField()
    tweet = models.TextField()

    # def __str__(self):
    #     return self.date