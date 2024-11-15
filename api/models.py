from django.db import models

class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32,unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    # phone = models.CharField(verbose_name="手机号", max_length=64)
    role_choices = (
        ("admin","管理员"),
        ("user", "用户"),
    )
    role = models.CharField(verbose_name="角色", max_length=16,choices=role_choices,default="user")

class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo',on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
class Depart(models.Model):
    pt100 = models.CharField(verbose_name="pt100", max_length=32)
    temper = models.CharField(verbose_name="temper", max_length=32)
    humid = models.CharField(verbose_name="humid", max_length=32)
    mq7 = models.CharField(verbose_name="mq7", max_length=32)
    time = models.DateTimeField(auto_now_add=True)