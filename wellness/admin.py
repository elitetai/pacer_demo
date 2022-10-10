from django.contrib import admin
from wellness.models import DailyRecord

class DailyRecordAdmin(admin.ModelAdmin):
    model = DailyRecord
    list_display = ['id', 'user', 'date']
    search_fields = ['user__email', 'user__username', 'date']
    list_filter = ['date']

admin.site.register(DailyRecord, DailyRecordAdmin)