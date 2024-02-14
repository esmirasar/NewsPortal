from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Post, Category, PostCategory, User, Subscription  # импортируем модель
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .filters import PostFilter
from django.urls import reverse_lazy
from .forms import PostForm, SubscriptionForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
import os
from dotenv import load_dotenv
from .tasks import email_send

load_dotenv()


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'  # шаблон для отображения списка новостей
    context_object_name = 'news_list'
    paginate_by = 5  # по заданию значение должно быть 10, но оставлю 2, потому что новости всего 3, и пагинация не будет работать


class NewsListSearch(ListView):
    model = Post
    template_name = 'news/news_list_search.html'  # шаблон для отображения списка новостей
    context_object_name = 'news_list_search'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsListDetail(DetailView):
    model = Post
    template_name = 'news/news_list_id.html'  # шаблон для отображения списка новостей
    context_object_name = 'news_list_id'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NW'
        post.save()

        email_send(self, post, form)

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('news_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


class ToSendMail(CreateView):
    form_class = SubscriptionForm
    model = Subscription
    template_name = 'news/Subscription.html'
    success_url = reverse_lazy('after_subscription')

    def form_valid(self, form):
        sub = form.save(commit=False)
        sub.user_id = self.request.user.pk
        return super().form_valid(form)


# отображение шаблона после отправки формы подписки


def after_subscription(request):
    return render(request, 'news/after_subscription.html')
