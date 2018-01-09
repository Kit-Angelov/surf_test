from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^rent_a_book/(?P<id>[0-9]+)/$', views.RentABookView.as_view(), name='rent_a_book'),
    url(r'^rented_books/$', views.RentedBook.as_view(), name='rented_books'),
]

urlpatterns += router.urls
