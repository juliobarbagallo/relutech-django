from developers.models import Developer
from django.db import models


class Asset(models.Model):
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type_choices = [
        ("laptop", "Laptop"),
        ("keyboard", "Keyboard"),
        ("mouse", "Mouse"),
        ("headset", "Headset"),
        ("monitor", "Monitor"),
    ]
    type = models.CharField(max_length=255, choices=type_choices)
    assigned_to = models.ForeignKey(
        Developer, on_delete=models.CASCADE, related_name="assets", null=True
    )

    def __str__(self):
        return f"{self.brand} {self.model}"
