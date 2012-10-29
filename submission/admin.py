from django.contrib import admin
from models import Entry, JudgeNote

class EntryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'overall_judgerating', 'overall_publicrating']

admin.site.register(Entry, EntryAdmin)
admin.site.register(JudgeNote, admin.ModelAdmin)
