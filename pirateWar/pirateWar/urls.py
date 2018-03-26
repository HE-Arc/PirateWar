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

from pirateWarApp.views import HomeView, AboutView, PlayView, ShipDeleteView, ShipCreateView, ShipUpdateView, \
    ProfileView, ActivityListView

from registration.views import RegistrationView

from registration.views import RegistrationView

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('play/activity', login_required(ActivityListView.as_view()), name='select-quest'),
    path('play/', login_required(PlayView.as_view()), name='play'),
    path('play/ship/<int:pk>/delete',
         login_required(ShipDeleteView.as_view()), name='delete-ship'),
    path('play/ship/create',
         login_required(ShipCreateView.as_view()), name='create-ship'),
    path('play/ship/<int:pk>/edit',
         login_required(ShipUpdateView.as_view()), name='edit-ship'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', RegistrationView.as_view(), name='register')

]
