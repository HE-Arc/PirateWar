"""pirateWar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.contrib.auth import views as auth_views

from pirateWarApp.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('play/', login_required(PlayView.as_view()), name='play'),
    path('play/delete-ship/<int:pk>',
         login_required(ShipDeleteView.as_view()), name='delete-ship'),
    path('play/create-ship/',
         login_required(ShipCreateView.as_view()), name='create-ship'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
         name='logout')

]
