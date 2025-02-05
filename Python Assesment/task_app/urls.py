from django.urls import path, include
from .views import *

urlpatterns = [

    path('task', TaskAPI.as_view())
]