from django.db import models



class Developer(models.Model):
    fullname = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.fullname
    