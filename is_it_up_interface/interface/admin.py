from django.contrib import admin

from .models import Site, Error, Submission

admin.site.register(Submission)
admin.site.register(Site)
#Register your models here.
admin.site.register(Error)