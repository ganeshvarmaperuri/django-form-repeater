from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('create', GrandParentCreate.as_view(), name="grandparent_create"),
]
