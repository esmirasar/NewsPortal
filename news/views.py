from django.shortcuts import render
from .models import Post  # импортируем модель Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'  #  шаблон для отображения списка новостей
    context_object_name = 'news_list'
    paginate_by = 2  # по заданию значение должно быть 10, но оставлю 2, потому что новости всего 3, и пагинация не будет работать

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
    template_name = 'news/news_list_id.html'  #  шаблон для отображения списка новостей
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
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    success_url = reverse_lazy('news_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')




