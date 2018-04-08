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

from pirateWarApp.views import AboutView, PlayView, ShipDeleteView, ShipCreateView, ShipUpdateView, \
    ProfileView, ActivityListView, SelectShipView, AddActivityView, ResultView, BuyCannonView, RecruitCrewManView

from registration.views import RegistrationView

urlpatterns = [
    path('', login_required(PlayView.as_view()), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('result', login_required(ResultView.as_view()), name='result'),
    path('activity', login_required(
        ActivityListView.as_view()), name='select-activity'),
    path('fight', login_required(
        ActivityListView.as_view()), name='fight'),
    path('activity/<int:pk>/selectship',
         login_required(SelectShipView.as_view()), name='select-ship'),
    path('activity/addactivity', login_required(AddActivityView.as_view()),
         name='add-activity'),
    # path('play/', login_required(PlayView.as_view()), name='play'),
    path('ship/<int:pk>/delete',
         login_required(ShipDeleteView.as_view()), name='delete-ship'),
    path('ship/create',
         login_required(ShipCreateView.as_view()), name='create-ship'),
    path('ship/<int:pk>/edit',
         login_required(ShipUpdateView.as_view()), name='edit-ship'),
    path('player/build-cannon',
         login_required(BuyCannonView.as_view()), name='build-cannon'),
    path('player/recruit-crewman',
         login_required(RecruitCrewManView.as_view()), name='recruit'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('registration.backends.simple.urls')),
    path('accounts/profile/', login_required(ProfileView.as_view()), name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/register/', RegistrationView.as_view(), name='register')
]
