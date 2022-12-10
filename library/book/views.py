from django.shortcuts import render, redirect

from .form import BookForm
from .models import Book
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BookSerializer


# def book_list_view(request):
#     context = {'books': Book.objects.all()}
#     return render(request, 'home.html', context)


def book_create_view(request, id=0):
    # context = {}
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     description = request.POST.get('description')
    #     count = request.POST.get('count')
    #
    #     book_object = Book.objects.create(name=name, description=description, count=count)
    #     context['object'] = book_object
    #     context['created'] = True
    #
    # return render(request, 'create_book.html', context=context)
    if request.method == "GET":
        if id == 0:
            form = BookForm()
            submit = "Add"
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(instance=book)
            submit = "Update"
        context = {'form': form,
                   'submit': submit}
        # return render(request, 'book/create_book.html', context)
        return render(request, 'create_book.html', context)
    else:
        if id == 0:
            form = BookForm(request.POST)
        else:
            book = Book.objects.get(pk=id)
            form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        return redirect('home')


def book_detail_view(request, id=None):
    book_object = None

    if id:
        book_object = Book.objects.get(pk=id)
    context = {'book': book_object}

    return render(request, 'book_detail.html', context=context)


def add_authors_to_book_view(request, id=None):
    book_object = None

    if id:
        book_object = Book.objects.get(pk=id)
    context = {'book': book_object}

    return render(request, 'book_detail.html', context=context)

class BookAPIView(APIView):

    queryset = Book.objects.all().values()
    def get(self, request, id = None):
        if id:
            book= Book.get_by_id(id)
            return Response({'one book from GET':BookSerializer(book).data})
        else:
            lst = Book.objects.all()
            return Response({'all books from GET':BookSerializer(lst, many=True).data})

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self,request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method PUT not allowed here, no ID"})
        try:
            book_to_update = Book.get_by_id(id)
        except:
            return Response({'error': "method PUT, Book not Found"})
        serializer = BookSerializer(data=request.data, instance=book_to_update)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"post":serializer.data})

    def delete(self,request,*args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method DELETE not allowed here, no ID"})
        try:
            book_to_delete = Book.get_by_id(id)
        except:
            return Response({'error': "method DELETE, Book not Found"})
        book_to_delete.delete()
        return Response({"post":"Delete book id = " +str(id)})