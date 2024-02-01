from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
import django_filters
from django import forms

class PostFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains", label="Название")
    author_id__user_id__username = CharFilter(lookup_expr="icontains", label="Автор")
    date_of_creation = django_filters.DateTimeFilter(widget=forms.DateTimeInput(attrs={'type': 'date'}), lookup_expr="gte", label="Дата публикации")

