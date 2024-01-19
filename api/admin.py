from django.contrib import admin
from .models import JduUser

# Register your models here.
@admin.register(JduUser)
class JduUserAdmin(admin.ModelAdmin):
    list_display = ('jdu_id', 'name', 'surname', 'exam_score')
    list_filter = ('jdu_id', 'exam_score')
    search_fields = ['jdu_id', 'jdu_name', 'phone_num', 'address']