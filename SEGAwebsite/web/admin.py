from django.contrib import admin
from .models import User, PerguruanTinggi
from import_export.admin import ImportExportModelAdmin

@admin.register(User,PerguruanTinggi)
class ViewAdmin(ImportExportModelAdmin):
	pass

