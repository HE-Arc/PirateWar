import hashlib
import math
import random
from datetime import datetime

from pirateWarApp.forms import ProfileUpdateForm, ShipUpdateForm
from pirateWarApp.models import Activity, Category, Player, Ship, User

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import ModelForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import utc
from django.views import generic
from django.views.generic import TemplateView

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        hash = hashlib.md5()
        hash.update(request.user.email.encode())
        hash = hash.hexdigest()
        url = 'https://secure.gravatar.com/avatar/' + hash
        url += '?s=180&d=' + request.build_absolute_uri('/')
        url += static('img/pirate.png').lstrip('/')
        return render(request, self.template_name, {'hash': hash, 'url': url})


class PasswordChangeView(generic.TemplateView):
    model = User
    template_name = 'edit_password.html'

    def get(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        instance.password = ""
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwars):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class UpdateProfileView(generic.TemplateView):
    form_class = ProfileUpdateForm
    model = User
    template_name = 'edit_password.html'

    def get(self, request, *args, **kwargs):
        instance = User.objects.get(id=request.user.id)
        form = ProfileUpdateForm(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwars):
        user_to_update = User.objects.get(id=request.user.id)
        form = ProfileUpdateForm(request.POST, instance=user_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class PlayView(generic.TemplateView):
    template_name = 'home.html'

    @staticmethod
    def get_player(user):
        """Return the player associated with the user or create one if it doesn't exist."""
        if Player.objects.filter(user=user).count() < 1:
            Player.objects.create(user=user, money=100,
                                  wood=100, iron=100, crew=5, cannons=2)
        return Player.objects.filter(user=user).first()

    def get(self, request, *args, **kwargs):
        user = request.user
        player = self.get_player(user)
        ships = Ship.objects.filter(player=player, currentActivity=None).all()
        ships_activity = Ship.objects.filter(
            player=player).exclude(currentActivity=None).all()
        nbships = len(ships)
        users = User.objects.all()
        return render(request, self.template_name,
                      {'player': player, 'nbships': nbships, 'ships': ships, 'ships_activity': ships_activity, 'users': users})


class ShipDeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Ship
    success_url = reverse_lazy('home')
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

    def get(self, request, *args, **kwargs):
        if "fight" in request.path:
            activities = self.model.objects.filter(
                category__name__contains="Attack").order_by('level')
        else:
            activities = self.model.objects.order_by('level')
        return render(request, self.template_name, {'activities': activities})


class SelectShipView(generic.ListView):
    model = Ship
    template_name = "select_ship.html"

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        player = PlayView.get_player(user)
        ships = Ship.objects.filter(player=player, currentActivity=None).all()
        nbships = len(ships)
        if nbships == 0:
            messages.add_message(
                self.request, messages.ERROR, 'No ship available')
        pkactivity = pk
        return render(request, self.template_name,
                      {'nbships': nbships, 'ships': ships, 'pkactivity': pkactivity})


class AddActivityView(generic.TemplateView):
    model = Ship

    def post(self, request, *args, **kwargs):
        user = request.user
        activity = Activity.objects.get(pk=request.POST.get('activitypk'))
        ship = Ship.objects.get(pk=request.POST.get('shippk'))
        if ship.player.user == user:
            ship.currentActivity = activity
            ship.endActivity = datetime.utcnow().replace(tzinfo=utc) + activity.duration
            ship.save()
        else:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
        return redirect('home')


class ResultView(generic.TemplateView):
    template_name = 'result.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        player = PlayView.get_player(user=user)
        ship = Ship.objects.get(pk=request.POST.get('shippk'))
        activity = ship.currentActivity
        if user != ship.player.user:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
            return redirect('home')
        if activity is None or ship.endActivity.timestamp() > datetime.utcnow().replace(tzinfo=utc).timestamp():
            return redirect('home')

        delta_level = ship.level - activity.level
        factor_by_type = {'Shipping': 1, 'Defense': 1.2, 'Attack': 1.5}
        damage = 100 - (4 * ship.cannon + 2 * ship.crew +
                        delta_level * 10 + random.randint(-20, 20))
        if damage < 0:
            damage = 0
        damage = damage * factor_by_type[activity.category.name]
        life = math.ceil(ship.life - damage)
        level_up = False
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
                level_up = True
                ship.xp = 0
                ship.level = ship.level + 1
            ship.life = life
            ship.currentActivity = None
            ship.endActivity = None
            ship.save()
        return render(request, self.template_name,
                      {'ship': ship, 'activity': activity, 'succes': life > 0, 'levelup': level_up})


class ShipCreateView(generic.CreateView):
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

        return redirect('home')


class ShipUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Ship
    success_url = reverse_lazy('home')
    template_name = 'edit_ship.html'
    form_class = ShipUpdateForm

    def post(self, request, *args, **kwargs):
        ship_to_update = Ship.objects.get(pk=self.get_object().pk)
        player = ship_to_update.player

        old_crew = ship_to_update.crew
        old_cannon = ship_to_update.cannon
        old_life = ship_to_update.life

        form = ShipUpdateForm(request.POST, instance=ship_to_update)

        if form.is_valid():
            new_crew = form.cleaned_data['crew']
            new_cannon = form.cleaned_data['cannon']
            new_life = form.cleaned_data['life']

            cond_crew = player.crew + (old_crew - new_crew) >= 0
            cond_cannon = player.cannons + (old_cannon - new_cannon) >= 0
            cond_wood = player.wood + (old_life - new_life) >= 0

            if not cond_crew:
                # form.fields['crew'].error_messages['max_value'] = 'Not enough crew available'
                messages.add_message(
                    self.request, messages.ERROR, 'Not enough crew available')
            if not cond_wood:
                # form.fields['life'].error_messages['max_value'] = 'Not enough wood available'
                messages.add_message(
                    self.request, messages.ERROR, 'Not enough wood available')
            if not cond_cannon:
                # form.fields['cannon'].error_messages['max_value'] = 'Not enough cannon available'
                messages.add_message(
                    self.request, messages.ERROR, 'Not enough cannon available')

            if cond_crew and cond_cannon and cond_wood:
                player.crew = player.crew + (old_crew - new_crew)
                player.wood = player.wood + (old_life - new_life)
                player.cannons = player.cannons + (old_cannon - new_cannon)
                player.save()
                form.save()
                return HttpResponseRedirect(self.get_success_url())

        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def test_func(self):
        self.object = self.get_object()
        cond = self.object.player.user == self.request.user
        if not cond:
            messages.add_message(self.request, messages.ERROR, 'Wrong user')
        return cond

    def get_context_data(self, **kwargs):
        context = super(ShipUpdateView, self).get_context_data(**kwargs)
        context['player'] = self.object.player
        return context


class BuyCannonView(generic.TemplateView):

    def post(self, request, *args, **kwargs):
        player = PlayView.get_player(request.user)
        player = Player.objects.select_for_update().get(pk=player.pk)
        if player.iron >= 10:
            player.cannons += 1
            player.iron -= 10
            player.save()
            return redirect('home')

        messages.add_message(self.request, messages.ERROR, 'Not enough iron')
        return redirect('home')


class RecruitCrewManView(generic.TemplateView):

    def post(self, request, *args, **kwargs):
        player = PlayView.get_player(request.user)
        player = Player.objects.select_for_update().get(pk=player.pk)
        if player.money >= 10:
            player.crew += 1
            player.money -= 10
            player.save()
            return redirect('home')

        messages.add_message(self.request, messages.ERROR, 'Not enough money')
        return redirect('home')
