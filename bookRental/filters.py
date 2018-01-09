from django_filters import FilterSet
from . import models
import rest_framework_filters as filters


class BookFilter(FilterSet):

    class Meta:
        model = models.Book
        fields = ['name']
