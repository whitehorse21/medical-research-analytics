from django.contrib import admin

from .models import LiteratureArticle, Participant, Study

admin.site.register(Study)
admin.site.register(Participant)
admin.site.register(LiteratureArticle)
