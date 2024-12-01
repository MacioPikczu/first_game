from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User # SuperUser

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# class SuperUserCreationForm(UserCreationForm):
#     class Meta:
#         model = SuperUser
#         fields = ['username', 'email']


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#     password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirm = cleaned_data.get("password_confirm")
#
#         if password and password != password_confirm:
#             raise forms.ValidationError("Hasła muszą się zgadzać.")
#         return cleaned_data
