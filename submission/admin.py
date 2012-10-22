from django.contrib import admin
from models import Entry, JudgeNote

admin.site.register(Entry,admin.ModelAdmin)
admin.site.register(JudgeNote, admin.ModelAdmin)
