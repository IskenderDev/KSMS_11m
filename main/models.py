from django.db import models

# Create your models here.
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    photo_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name