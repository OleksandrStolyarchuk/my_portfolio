from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .form import OrderForm, OrderEndAtForm
from .models import Order
from .serializers import OrderSerializer


def order_list_view(request):
    if request.user.role == 1:
        context = {'orders': Order.objects.all()}
    else:
        context = {'orders': Order.objects.filter(user=request.user)}

    return render(request, 'order_list.html', context)


def order_create_view(request, id=0):
    # context = {}
    #
    # if request.method == 'POST':
    #     user = CustomUser.POST.get('user')
    #     book = request.POST.get('book')
    #     plated_end_at = request.POST.get('plated_end_at')
    #     order_object = Order.objects.create(user=user, book=book, plated_end_at=plated_end_at)
    #     context['object'] = order_object
    #     context['created'] = True
    #
    # # return render(request, 'create_order.html', context=context)
    if request.method == "GET":
        if id == 0:
            form = OrderForm()
        else:
            order = Order.objects.get(pk=id)
            form = OrderForm(instance=order)
        submit = "Add"
        context = {'form': form,
                   'submit': submit}
        return render(request, 'create_order.html', context)
    else:
        if id == 0:
            form = OrderForm(request.POST)
        else:
            order = Order.objects.get(pk=id)
            form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            # set current user
            form.instance.user = request.user
            form.save()
        return redirect('/orders')


def order_detail_view(request, id=None):
    order_object = None

    if id:
        order_object = Order.objects.get(pk=id)
    context = {'order': order_object}

    return render(request, 'order_detail.html', context=context)


def order_close_view(request, id=None):
    context = {}
    if id:
        try:
            order_object = Order.objects.get(pk=id)

            if order_object.end_at:
                order_object.delete()
                context['description'] = "The order was closed successful"
            else:
                context['description'] = f"The order can't be deleted, " \
                                         f"the user didn't return book yet"
        except Order.DoesNotExist:
            context['description'] = "The order doesn't exists in database"

    # return render(request, 'close_order.html', context=context)
    # return render(request, 'order_list.html', context=context)
    return redirect('/orders')


def set_end_at_view(request, id):
    order_object = Order.objects.get(pk=id)

    if request.method == 'POST':
        form = OrderEndAtForm(request.POST, instance=order_object)
        if form.is_valid():
            form.save()
            return redirect('detail_order', order_object.id)
    else:
        form = OrderEndAtForm(instance=order_object)

    return render(request, 'set_end_at.html', {'form': form})


class OrderAPIView(APIView):
    queryset = Order.objects.all().values()

    def get(self, request, id=None):
        if id:
            order = Order.get_by_id(id)
            return Response({'one order from GET':OrderSerializer(order).data})
        else:
            lst = Order.objects.all()
            return Response({'all orders from GET':OrderSerializer(lst, many=True).data})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self,request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method PUT not allowed here, no ID"})
        try:
            order_to_update = Order.get_by_id(id)
        except:
            return Response({'error': "method PUT, Order not Found"})
        serializer = OrderSerializer(data=request.data, instance=order_to_update)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"post":serializer.data})

    def delete(self,request,*args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            return Response({'error': "method DELETE not allowed here, no ID"})
        try:
            order_to_delete = Order.get_by_id(id)
        except:
            return Response({'error': "method DELETE, Order not Found"})
        order_to_delete.delete()
        return Response({"post": "Delete order id = " + str(id)})


class UserOrderViewSet(viewsets.ModelViewSet):
    """
    for user.id + order.id
    """
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user=user_id)
        return queryset
