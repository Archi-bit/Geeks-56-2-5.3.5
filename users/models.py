from django.db import models
from django.conf import settings
import random

User = settings.AUTH_USER_MODEL

class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Code {self.code} for {self.user}"

    @staticmethod
    def generate_code():
        while True:
            code = f"{random.randint(0, 999999):06d}"
            if not ConfirmationCode.objects.filter(code=code).exists():
                return code
