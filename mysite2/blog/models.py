from datetime import datetime

from django.db import models

from  django.contrib.auth.models import User
# Create your models here.

class Author(models.Model):
    '''
    博客作者类型
    '''
    # 作者编号
    id = models.AutoField(primary_key=True)
    # # 登录账号
    # username = models.CharField(max_length=50)
    # # 登录密码
    # userpass = models.CharField(max_length=50)
    # 真实姓名
    realname = models.CharField(max_length=50)
    # 生日
    birthday = models.DateField(null=True,blank=True)
    # 性别
    age = models.CharField(max_length=10,default='请完善')
    # 邮箱
    email = models.CharField(max_length=100,default='请完善')
    # 电话
    phone = models.CharField(max_length=20,default='请完善')
    # 用户地址
    address = models.TextField(null=True,blank=True,default='请完善')
    # 个人介绍
    intro = models.TextField(null=True,blank=True,default='请完善')

    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Article(models.Model):
    '''
    文章类型
    '''
    # 文章编号
    id = models.AutoField(primary_key=True)
    # 文章标题
    title = models.CharField(max_length=50)
    # 文章内容
    content = models.TextField()
    # 发布时间
    publish = models.DateTimeField(default=datetime.now())
    # 点击量【2019.11.2】
    count = models.IntegerField(default=0)
    # 文章作者
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    # Django 数据模型的内部数据限制类
    class Meta:
        ordering = ["-publish"]











