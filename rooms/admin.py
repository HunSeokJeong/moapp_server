from django.contrib import admin
from .models import Group, Room, History, Statics

admin.site.register(Group)
admin.site.register(Room)
admin.site.register(History)
admin.site.register(Statics)
# Register your models here.
