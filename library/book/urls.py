from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('<int:id>', views.book_detail_view, name='book_detail'),
    # path('delete/<int:id>/', views.book_delete_view, name='delete_book'),
    path('create/', views.book_create_view, name='create_book'),
]