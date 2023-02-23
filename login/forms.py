from django import forms
from .models import User


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('user_name', 'user_org', 'user_bind_num', 'phone', 'email', 'profile_photo', 'realname')


class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ("password", "user_uuid", "email", 'user_name')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")
