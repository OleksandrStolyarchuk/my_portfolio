from django.urls import path

from . import views

urlpatterns = [
    path('', views.users_list_view, name='index_user'),
    path('<int:id>', views.user_detail_view, name='user_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
