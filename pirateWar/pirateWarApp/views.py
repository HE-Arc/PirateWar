from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
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


class ShipDeleteView(generic.DeleteView):
    model = Ship
    success_url = reverse_lazy('play')
    template_name = 'ship_confirm_delete.html'

    def check_user(self, user1, user2):
        return user1 == user2

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (self.check_user(request.user, self.object.player.user)):
            self.object.delete()
            return redirect('/play')
        else:
            return HttpResponse('401 - Unauthorized', status=401)


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

        # TODO Error message
        return redirect('play')


class ShipUpdateView(generic.UpdateView):
    model = Ship
    success_url = reverse_lazy('play')
    template_name = 'edit_ship.html'


class ShipListView(generic.ListView):
    model = Ship


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        logged = request.user.is_authenticated
        username = ''
        if logged:
            username = request.user.username
        return render(request, self.template_name, {'logged': logged, 'username': username})
