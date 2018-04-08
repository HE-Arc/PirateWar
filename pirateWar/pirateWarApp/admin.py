from django.contrib import admin

from .models import Activity, Category, Player, Ship, User

# Register your models here.

admin.site.register(Player)
admin.site.register(Category)
admin.site.register(Activity)
admin.site.register(Ship)
