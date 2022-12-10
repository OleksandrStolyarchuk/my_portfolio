from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
]