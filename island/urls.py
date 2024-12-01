"""
URL configuration for island project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import sys
sys.path.append('../')

from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from account.views import SignUpView, ResourcesView, StatisticsView  # CreateSuperUserView
# from account.views import register, logout_user

# def rungame():
#     with open('F:/Python/Kurs/Game_island/island/main.py') as f:
#         code = f.read()
#         exec(code)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('resources', ResourcesView.as_view(), name='resources'),
    path('statistics', StatisticsView.as_view(), name='statistics'),
    # path('createsuper', CreateSuperUserView.as_view(), name="createsuper"),
    # path('signup/', register, name='register'),
    # path('accounts', include('django.contrib.auth.urls'), name='login_page'),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', RedirectView.as_view(url='/home', permanent=True)),
    # path('logout/', logout_user, name='logout'),
    # path('mining', rungame()),
    # path('mining',

]
