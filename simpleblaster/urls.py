"""simpleblaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import auth_log.views as auth
import simpleblaster.views as dash
import costumer.views as costumer
import sendmail.views as mymail

urlpatterns = [
    path('admin/', admin.site.urls),
    #auth fiture
    path('', auth.login, name="login"),
    path('register', auth.register, name="register"),
    path('auth_login', auth.login, name="auth_login"),
    path('logout', dash.logout, name="logout"),
    #dashboard
    path('dashboard', dash.dashboard, name="dashboard"),
    #costumer
    path('add-costumer', costumer.add_costumer, name="add-costumer"),
    path('list-costumer', costumer.list_costumer, name="list-costumer"),
    path('edit-show/<int:id>', costumer.edit_show, name="edit-show"),
    path('edit-proses', costumer.edit_proses, name="edit-proses"),
    path('deleted-costumer/<int:id>', costumer.delete_proses, name="deleted-costumer"),
    #sendmail
    path('send-email', mymail.sendmail, name="send-email"),
    path('go-send', mymail.sendmail_process, name="go-send"),
    #users config
    path('config-pass', dash.edit_pass, name="config-pass"),
    path('change-process', dash.edit_proses, name="change-process"),
]
