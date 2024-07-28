from django.contrib import admin
from .models import MaintenanceRequest, Assignament

class Assignament_InLine(admin.TabularInline):
    model = Assignament
    extra = 1

class MaintenanceRequest_Admin(admin.ModelAdmin):
    list_display = ('date_required', 'description', 'state')
    inlines = [Assignament_InLine]

class Assignament_Admin(admin.ModelAdmin):
    list_display = ('request_id', 'user_id', 'date_assigned')

admin.site.register(MaintenanceRequest, MaintenanceRequest_Admin)
admin.site.register(Assignament, Assignament_Admin)
