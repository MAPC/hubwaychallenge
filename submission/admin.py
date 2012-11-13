from django.contrib import admin
from models import Entry, JudgeNote, Award

class EntryAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'overall_judgerating', 'overall_publicrating']

class AwardAdmin(admin.ModelAdmin):

	list_display = ['id', 'category', 'entry']
	list_editable = ['category', 'entry']

admin.site.register(Entry, EntryAdmin)
admin.site.register(JudgeNote, admin.ModelAdmin)
admin.site.register(Award, AwardAdmin)
