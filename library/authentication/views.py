from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .forms import SignUpForm
from .models import CustomUser
from .serializers import UserSerializer

from rest_framework import generics, viewsets


class UserViewSet(viewsets.ModelViewSet):
    """
    User API
    """
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer


def users_list_view(request):
    context = {'users': CustomUser.objects.all()}

    return render(request, 'users_list.html', context)


def user_detail_view(request, id=None):
    user_object = None

    if id:
        user_object = CustomUser.objects.get(pk=id)
    context = {'user': user_object}

    return render(request, 'user_detail.html', context=context)


def register_view(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/users/login')

    context = {'form': form}

    return render(request, 'register.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm(request)

    context = {'form': form}

    return render(request, 'login.html', context=context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'logout.html', {})
