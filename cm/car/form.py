from django import forms


class FileForm(forms.Form):
    files = forms.FileField(label="用例文件")
