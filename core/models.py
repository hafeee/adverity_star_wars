from django.db import models

# We will automatically save all the matadata that we need in here

class Collection(models.Model):
    name = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    pathToCSV = models.CharField(max_length=50, blank=True)
