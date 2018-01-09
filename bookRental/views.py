from django.shortcuts import render
from django_filters import rest_framework as django_filters_set
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework import filters as drf_filters
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from . import models, serializers, filters
from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import operator


class Login(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        username = request.data.get("username")
        print(username)
        password = request.data.get("password")
        print(password)
        user = authenticate(username=username, password=password)
        if not user:
            print('not user')
            return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)
        else:
            user_id = user.id
            print(user_id)
            token, _ = Token.objects.get_or_create(user=user)
            print(token)
            return Response({"token": token.key, 'user_id': user_id})


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    filter_backends = (drf_filters.SearchFilter, drf_filters.OrderingFilter, django_filters_set.DjangoFilterBackend,)
    ordering_fields = ('price',)
    search_fields = ('author__first_name', 'author__last_name')
    filter_class = filters.BookFilter


class RentedBook(generics.ListAPIView):

    serializer_class = serializers.RentalSerializer

    def get_queryset(self):
        user = getUser(self.request)
        obj_list = models.Lease.objects.filter(user=user)
        sorted_obj_list = sorted(obj_list, key=operator.attrgetter('balance'))
        return [item for item in sorted_obj_list if item.active]


class RentABookView(APIView):

    def get(self, request, id, format=None):
        return Response({'sdf': 4234})

    def post(self, request, id, format=None):
        user = getUser(request)
        term = int(request.data.get('term'))
        book = models.Book.objects.get(pk=id)

        value = book.price * term
        if (user.balance - value) >= 0:
            user.balance -= value
            user.save()
            date_start = timezone.now()
            date_finish = date_start + relativedelta(months=term)
            new_lease = models.Lease(user=user, book=book, value=value, date_start=date_start, date_finish=date_finish)
            new_lease.save()
            content = {'lease': new_lease.pk}
            return Response(content)
        else:
            raise APIException('not enough money')


def getUser(request):
    token_text = str(request.META.get('HTTP_AUTHORIZATION'))
    token = token_text.split(' ')[1]
    user = Token.objects.get(key=token).user
    return user


def index(request):
    return render(request, 'bookRental/api.html')


