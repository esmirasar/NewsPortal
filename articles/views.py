from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import sys
sys.path.append('..')
from news.models import Post, User, Category, Author, PostCategory, Comment
from .forms import ArticleForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('articles.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = '/news/post_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'AR'
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')
