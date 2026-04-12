from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLES = (
        ("admin", "Administrador"),
        ("tutor", "Tutor"),
        ("estudiante", "Estudiante"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"