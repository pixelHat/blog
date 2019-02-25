from django.contrib import admin
from . import models

admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Reply)
admin.site.register(models.User)
