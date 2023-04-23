from developers.models import Developer
from django.db import models


class License(models.Model):
    software = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(
        Developer, on_delete=models.CASCADE, related_name="licenses", null=True
    )

    def __str__(self):
        return self.software
