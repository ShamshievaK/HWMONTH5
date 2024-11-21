from django.db import models


class SmsCode(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='sms')
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


