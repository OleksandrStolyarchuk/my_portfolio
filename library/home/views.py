from django.shortcuts import render

from book.models import Book


def home_view(request):
    context = {'books': Book.objects.all()}
    return render(request, 'home.html', context)
