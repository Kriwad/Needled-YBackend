from django.contrib import admin
from .models import ToDoList , CustomUser
# Register your models here.
admin.site.register(ToDoList)
admin.site.register(CustomUser)

