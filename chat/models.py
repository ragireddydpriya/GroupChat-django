from django.db import models

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

User = get_user_model()

class Group(models.Model):
    name=models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True,default='')
    members = models.ManyToManyField(User,blank=True,related_name='group_members')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['name']


class GroupMessage(models.Model):
    msg = models.CharField(max_length=1000)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,related_name='membership')
    is_liked = models.ManyToManyField(User, blank=True, related_name='group_msg')
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.msg

