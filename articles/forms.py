from django import forms
from django.forms import ValidationError

import sys
sys.path.append('..')
from news.models import Post


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title == text:
            raise ValidationError('Описание и заголовок не должны быть одинаковыми')
        return cleaned_data
