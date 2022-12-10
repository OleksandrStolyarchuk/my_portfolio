from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AuthorForm
from .models import Author
from .serializers import AuthorSerializer


def author_list_view(request):
    context = {'authors': Author.objects.all()}

    return render(request, 'authors_list.html', context)


def author_create_view(request):
    form = AuthorForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        author_object = form.save()
        return redirect('index_author')

    return render(request, 'create_author.html', context=context)


def author_detail_view(request, id=None):
    author_object = None

    if id:
        author_object = Author.objects.get(pk=id)
    context = {'author': author_object}

    return render(request, 'author_detail.html', context=context)


def author_delete_view(request, id=None):
    context = {}
    if id:
        try:
            author_object = Author.objects.get(pk=id)
            books_count = author_object.books.all().count()

            if books_count == 0:
                author_object.delete()
                context['description'] = "The author was deleted successful"
            else:
                context['description'] = f"The author can't be deleted, " \
                                         f"he has {books_count} books attached"
        except Author.DoesNotExist:
            context['description'] = "The author doesn't exists in database"

    return render(request, 'delete_author.html', context=context)

class AuthorAPIView(APIView):

    queryset = Author.objects.all().values()

    def get(self, request, id=None):
        if id:
            author= Author.get_by_id(id)
            return Response({'one author from GET': AuthorSerializer(author).data})
        else:
            lst = Author.objects.all()
            return Response({'all authors from GET': AuthorSerializer(lst, many=True).data})

    # def post(self, request):
    #     serializer = AuthorSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response({'post': serializer.data})

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_new = Author.objects.create(
            name=request.data['name'],
            surname=request.data['surname'],
            patronymic=request.data['patronymic'],
            id=request.data['id'],
            # books = request.data['books']
        )
        for book_id in request.data['books']:
            post_new.add(book_id)
        return Response({'post': AuthorSerializer(post_new).data})


    def put(self,request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method PUT not allowed here, no ID"})
        try:
            author_to_update = Author.get_by_id(id)
        except:
            return Response({'error': "method PUT, Author not Found"})
        serializer = AuthorSerializer(data=request.data, instance=author_to_update)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"post":serializer.data})

    def delete(self,request,*args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method DELETE not allowed here, no ID"})
        try:
            author_to_delete = Author.get_by_id(id)
        except:
            return Response({'error': "method DELETE, Author not Found"})
        author_to_delete.delete()
        return Response({"post":"Delete author id = " +str(id)})