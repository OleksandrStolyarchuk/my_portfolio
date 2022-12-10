"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views import UserViewSet

from author.views import AuthorAPIView
from book.views import BookAPIView
from order.views import OrderAPIView, UserOrderViewSet


router_user = DefaultRouter()
router_user.register(r'api/v1/user', UserViewSet)

router_order = DefaultRouter()
router_order.register(r'api/v1/user/(?P<user_id>\d+)/order',
                      UserOrderViewSet, basename='order_plus_user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('book/', include('book.urls')),
    path('author/', include('author.urls')),
    path('users/', include('authentication.urls')),
    path('orders/', include('order.urls')),

    path('api/v1/book/', BookAPIView.as_view()),
    path('api/v1/book/<int:id>/', BookAPIView.as_view()),

    path('api/v1/author/', AuthorAPIView.as_view()),
    path('api/v1/author/<int:id>/', AuthorAPIView.as_view()),

    path('api/v1/order/', OrderAPIView.as_view()),
    path('api/v1/order/<int:id>/', OrderAPIView.as_view()),
]

urlpatterns += router_user.urls
urlpatterns += router_order.urls

