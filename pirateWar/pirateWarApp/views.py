from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.contrib import messages
from pirateWarApp.models import Ship, Player, User, Category, Activity


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
        ships = Ship.objects.filter(player=player).all()
        nbships = len(ships)
        return render(request, self.template_name,
                      {'player': player, 'nbships': nbships, 'ships': ships})


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

class SelectQuestView(generic.ListView):
    model = Activity
    template_name = "select_quest.html"


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
