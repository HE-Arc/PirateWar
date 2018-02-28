from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView
from pirateWarApp.models import *


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'


class ProfileView(generic.TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if Player.objects.filter(user=user).count() < 1:
            Player.objects.create(user=user, money=10, wood=10, iron=10, crew=3, cannons=1)
        player = Player.objects.filter(user=user).first()
        return render(request, self.template_name, {'player': player})


class PlayView(generic.TemplateView):
    template_name = 'play.html'

    def get_player(self, user):
        if Player.objects.filter(user=user).count() < 1:
            Player.objects.create(user=user, money=10, wood=10, iron=10, crew=3, cannons=1)
        return Player.objects.filter(user=user).first()

    def get(self, request, *args, **kwargs):
        user = request.user
        player = self.get_player(user)
        ships = Ship.objects.filter(player=player).all()
        nbships = len(ships)
        return render(request, self.template_name, {'player': player, 'nbships': nbships, 'ships': ships})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('shipname', 'my ship')
        user = request.user
        player = self.get_player(user)
        Ship.objects.create(player=player, name=name)
        ships = Ship.objects.filter(player=player).all()
        nbships = len(ships)
        return render(request, self.template_name, {'player': player, 'nbships': nbships, 'ships': ships})


class EditShipView(generic.UpdateView):
    template_name = 'edit_ship.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        logged = request.user.is_authenticated
        username = ''
        if logged:
            username = request.user.username
        return render(request, self.template_name, {'logged': logged, 'username': username})
