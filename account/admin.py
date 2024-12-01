from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .views import UserChangeForm, UserCreationForm

# Register your models here.
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email']

admin.site.register(User, UserAdmin)