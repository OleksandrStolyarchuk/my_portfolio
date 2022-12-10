from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.author_list_view, name='index_author'),
    path('<int:id>', views.author_detail_view, name='detail'),
    path('delete/<int:id>/', views.author_delete_view, name='delete'),
    path('create/', views.author_create_view, name='create'),
]