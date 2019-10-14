import hashlib

from django import forms

from user.models import User


class UserForm(forms.Form):
    """
    对request中的传递的参数进行校验
    """
    username = forms.CharField(required=True, error_messages={'required': '请填写用户名！'}, label='用户名')
    pwd = forms.CharField(required=True, error_messages={'required': '请填写密码！'}, label='密码')

    def clean(self):
        """
        自定义form表单验证项目：需以clean开头
        :return:
        """
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if not user:
            raise forms.ValidationError({'username': '没有该帐号,请通知管理员开通！'})
        if user.pwd != self.cleaned_data.get('pwd'):
            raise forms.ValidationError({'pwd': '密码错误,请重新输入！'})
        return self.cleaned_data


class UserFormAdd(forms.Form):
    """
    校验添加的用户
    """
    username = forms.CharField(required=True, error_messages={'required': '请填写用户名！'}, label='用户名')
    passd = forms.CharField(max_length=16, min_length=6, required=True, error_messages={'required': '请填写密码！',
                                                                                        'max_length': '密码长度超出16位',
                                                                                        'min_length': '密码长度少于6位'
                                                                                        }, label='密码')
    repassd = forms.CharField(max_length=16, min_length=6, required=True, error_messages={'required': '请填写密码！',
                                                                                          'max_length': '密码长度超出16位',
                                                                                          'min_length': '密码长度少于6位'
                                                                                          })
    write = forms.CharField(required=False)
    read = forms.CharField(required=False)
    ledao = forms.CharField(required=False)

    def clean(self):
        """
        自定义form表单验证项目
        :return:
        """
        user = User.objects.filter(username=self.cleaned_data.get('username')).first()
        if user:
            raise forms.ValidationError({'username': '帐号已存在,请勿重复添加'})
        if self.cleaned_data.get('passd') != self.cleaned_data.get('repassd'):
            raise forms.ValidationError({'repassd': '两次密码不相同'})
        if not self.cleaned_data.get('write') and not self.cleaned_data.get('read') and not self.cleaned_data.get('ledao'):
            raise forms.ValidationError({'read': '请勾选帐号角色'})
        if self.cleaned_data.get('write') and self.cleaned_data.get('read') and self.cleaned_data.get('ledao'):
            raise forms.ValidationError({'read': '一个帐号只能有一个角色'})
        return self.cleaned_data


class UserFormEdit(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '请填写用户名！'}, label='用户名')
    passd = forms.CharField(max_length=16, min_length=6, required=True, error_messages={'required': '请填写密码！',
                                                                                        'max_length': '密码长度超出16位',
                                                                                        'min_length': '密码长度少于6位'
                                                                                        }, label='密码')
    repassd = forms.CharField(max_length=16, min_length=6, required=True, error_messages={'required': '请填写密码！',
                                                                                          'max_length': '密码长度超出16位',
                                                                                          'min_length': '密码长度少于6位'
                                                                                          })
    write = forms.CharField(required=False)
    read = forms.CharField(required=False)

    def clean(self):
        """
        自定义form表单验证项目
        :return:
        """
        user = User.objects.filter(username=self.cleaned_data['username']).first()
        m = hashlib.md5(self.cleaned_data['passd'].encode())
        if user.pwd == m.hexdigest():
            raise forms.ValidationError({'repassd': '与上次密码相同'})
        if self.cleaned_data.get('passd') != self.cleaned_data.get('repassd'):
            raise forms.ValidationError({'repassd': '两次密码不相同'})
        if not self.cleaned_data.get('write') and not self.cleaned_data.get('read'):
            raise forms.ValidationError({'read': '请勾选帐号角色'})
        if self.cleaned_data.get('write') and self.cleaned_data.get('read'):
            raise forms.ValidationError({'read': '一个帐号只能有一个角色'})
        return self.cleaned_data
