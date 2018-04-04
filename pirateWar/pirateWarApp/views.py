from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.contrib import messages
from pirateWarApp.models import Ship, Player, User, Category, Activity
from datetime import datetime
import random
import math


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

    @staticmethod
    def get_player(user):
        """Return the player associated with the user or create one if it doesn't exist."""
        if Player.objects.filter(user=user).count() < 1:
            Player.objects.create(user=user, money=10, wood=10, iron=10, crew=3, cannons=1)
        return Player.objects.filter(user=user).first()

    def get(self, request, *args, **kwargs):
        user = request.user
        player = self.get_player(user)
        ships = Ship.objects.filter(player=player, currentActivity=None).all()
        ships_activity = Ship.objects.filter(player=player).exclude(currentActivity=None).all()
        nbships = len(ships)
        return render(request, self.template_name,
                      {'player': player, 'nbships': nbships, 'ships': ships, 'ships_activity': ships_activity})


class ShipDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Ship
    success_url = reverse_lazy('play')
    template_name = 'ship_confirm_delete.html'

    def test_func(self):
        self.object = self.get_object()
        cond = self.object.player.user.username == self.request.user.username
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
        return cond


class ActivityListView(generic.ListView):
    model = Activity
    template_name = "activity.html"

    def get_queryset(self):
        return self.model.objects.order_by('level')


class SelectShipView(generic.ListView):
    model = Ship
    template_name = "select_ship.html"

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        player = PlayView.get_player(user)
        ships = Ship.objects.filter(player=player, currentActivity=None).all()
        nbships = len(ships)
        if nbships == 0:
            messages.add_message(self.request, messages.ERROR, 'No ship available')
        pkactivity = pk
        return render(request, self.template_name,
                      {'nbships': nbships, 'ships': ships, 'pkactivity': pkactivity})


class AddActivityView(generic.TemplateView):
    template_name = 'play.html'
    model = Ship

    def get(self, request, pk, pk2, *args, **kwargs):
        user = request.user
        activity = Activity.objects.get(pk=pk)
        ship = Ship.objects.get(pk=pk2)
        if ship.player.user == user:
            ship.currentActivity = activity
            ship.endActivity = datetime.utcnow() + activity.duration
            ship.save()
        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
        return redirect('play')


class ResultView(generic.TemplateView):
    template_name = 'result.html'

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        player = PlayView.get_player(user=user)
        ship = Ship.objects.get(pk=pk)
        activity = ship.currentActivity
        if user != ship.player.user:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
            return redirect('play')
        if activity == None or ship.endActivity.timestamp() > datetime.now().timestamp():
            return redirect('play')
        else:
            deltaLevel = ship.level - activity.level
            dict = {'Shipping': 1, 'Defense': 1.2, 'Attack': 1.5}
            damage = 100 - (4 * ship.cannon + 2 * ship.crew + deltaLevel * 10 + random.randint(-20, 20))
            if damage < 0:
                damage = 0
            damage = damage * dict[activity.category.name]
            life = math.ceil(ship.life - damage)
            levelUp = False
            if life <= 0:
                life = 0
                ship.life = 0
                ship.delete()
            else:
                player.money = player.money + activity.rewardGold
                player.wood = player.wood + activity.rewardWood
                player.iron = player.iron + activity.rewardIron
                player.save()
                ship.xp = ship.xp + activity.level * 10
                if ship.xp >= 100 and ship.level < 10:
                    levelUp = True
                    ship.xp = 0
                    ship.level = ship.level + 1
                ship.life = life
                ship.currentActivity = None
                ship.endActivity = None
                ship.save()
            return render(request, self.template_name,
                          {'ship': ship, 'activity': activity, 'succes': life > 0, 'levelup': levelUp})


class ShipCreateView(generic.CreateView):
    template_name = 'play.html'
    model = Ship
    fields = ['name']

    def post(self, request, *args, **kwargs):
        name = request.POST.get('shipname', 'my ship')
        user = request.user
        player = PlayView.get_player(user=user)
        if player.wood >= 10:
            Ship.objects.create(player=player, name=name)
            player.wood = player.wood - 10
            player.save()

        else:
            messages.add_message(request, messages.ERROR, 'Not enough wood')

        return redirect('play')


class ShipUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Ship
    success_url = reverse_lazy('play')
    template_name = 'edit_ship.html'
    fields = ['name', 'crew', 'cannon', 'life']

    def test_func(self):
        self.object = self.get_object()
        cond = self.object.player.user == self.request.user
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
        return cond


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        logged = request.user.is_authenticated
        username = ''
        if logged:
            username = request.user.username
        return render(request, self.template_name, {'logged': logged, 'username': username})
