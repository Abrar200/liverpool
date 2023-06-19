from django.contrib import admin
from .models import Players, News, Profile, Comment


admin.site.register(Players)
admin.site.register(News)
admin.site.register(Profile)
admin.site.register(Comment)