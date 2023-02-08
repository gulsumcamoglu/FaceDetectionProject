from django.contrib import admin
from facedetection.models import reportModel,detectionModel

admin.site.register(reportModel)
class detectionAdmin(admin.ModelAdmin):
    search_fields= ('name','date')
    list_display = (
        'name','date','time'
    )
admin.site.register(detectionModel , detectionAdmin)
# Register your models here.
