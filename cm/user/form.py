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
