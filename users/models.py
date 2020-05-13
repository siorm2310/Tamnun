from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Squadron(models.Model):
    bases = [
        ("B1", "Base1"),
        ("B4", "Base4"),
        ("B6", "Base6"),
        ("B8", "Base8"),
        ("B10", "Base10"),
        ("B25", "Base25"),
        ("B28", "Base28"),
        ("B30", "Base30"),
    ]

    homebase = models.CharField(max_length=3, choices=bases, default="B1")
    Squadron_number = models.CharField(max_length=3, default="000")

    def __str__(self):
        return self.Squadron_number


class OperationalUser(models.Model):
    """User model for the operational users.
    This model extends on Django's authentication systems and adds a "Squadron" fields
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    squadron = models.ForeignKey(Squadron, on_delete=models.CASCADE)
