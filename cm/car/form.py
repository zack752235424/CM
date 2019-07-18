from django import forms


class FileForm(forms.Form):
    files = forms.FileField(label="用例文件")

    def clean(self):
        xls = self.cleaned_data['files']
        if not xls.name.endswith('.xls'):
            raise forms.ValidationError({'files': '请上传xls文件！'})
        return self.cleaned_data
