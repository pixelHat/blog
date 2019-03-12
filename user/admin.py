from django.contrib import admin
from . import models

admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.User)
admin.site.register(models.Contact)
admin.site.register(models.Notify)
