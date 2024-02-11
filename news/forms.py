from django import forms
from django.forms import ValidationError
import sys
from .models import Category, Post, Subscription
sys.path.append('..')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author',
                  'category',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if title == text:
            raise ValidationError('Описание и заголовок не должны быть одинаковыми')
        return cleaned_data


#форма, которая позволит пользователям выбирать категории, на которые они хотят подписаться


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['category']
        widgets = {
            'category': forms.Select,
        }


