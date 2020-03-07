'''
表单封装模块
'''
# 导入需要的模块
from django import forms

class CustomerForm(forms.Form):
    '''
    定义一个客户表单类型
    用于封装客户登录表单数据
    '''
    username = forms.CharField(
        max_length=18,
        label="用户名",
        widget=forms.TextInput(attrs={"class":"form-control"})
    )

    userpass = forms.CharField(
            widget=forms.PasswordInput(attrs={"class":"form-control"}),
            max_length=18,
            label="密码",
    )

