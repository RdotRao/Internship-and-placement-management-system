from django.contrib import admin
from .models import details,placed,position,completeddetails,applied
# Register your models here.


admin.site.register(details)
admin.site.register(position)
admin.site.register(placed)
admin.site.register(applied)
admin.site.register(completeddetails)