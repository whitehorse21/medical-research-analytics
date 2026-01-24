from django.contrib import admin

from .models import LiteratureArticle, Participant, Study, Token

admin.site.register(Study)
admin.site.register(Participant)
admin.site.register(LiteratureArticle)
admin.site.register(Token)