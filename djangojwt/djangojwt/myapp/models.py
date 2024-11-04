from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_role')
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','role')
