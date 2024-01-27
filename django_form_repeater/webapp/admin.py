from django.contrib import admin
from .models import *


admin.site.register(GrandParent)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(GrandChild)
