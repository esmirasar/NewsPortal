from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_comments_rating = 0
        posts = Post.objects.filter(author=self)
        for i in posts:
            posts_rating += i.rating
        comments = Comment.objects.filter(user=self.user)
        for h in comments:
            comments_rating += h.rating
        posts_comments = Comment.objects.filter(post__author=self)
        for t in posts_comments:
            posts_comments_rating += t.rating

        self.rating = (posts_rating * 3) + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscription', )

    def __str__(self):
        return self.name


class Post(models.Model):
    news = 'NW'  # значение такого вида будет записано в БД
    articles = 'AR'  # значение такого вида будет записано в БД
    POST_TYPES = [
        (news, "Новость"),
        (articles, "Статья")
    ]  # значения, которые будут переданы на пользовательский интерфейс

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    # в случае, если пользователю нравится, рейтинг прибавляется на 1
    def like(self):
        self.rating += 1
        self.save()

    # в случае, если пользователю не нравится, рейтинг убавляется на 1
    def dislike(self):
        self.rating -= 1
        self.save()

    # метод, возвращает начало статьи (предварительный просмотр) длиной 124 символа и добавляет многоточие в конце.
    def preview(self):

        if len(self.articles) > 124:
            return self.articles[:124] + '...'
        else:
            return self.articles

    # метод для обрезки текста в шаблон send_mail
    def get_short_text(self):
        return self.text[:50]

    @classmethod
    def get_absolute_url(self):
        post_url = reverse('post_detail', kwargs={'pk': self.objects.pk})
        return post_url


class PostCategory(models.Model):  # промежуточная модель для category
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"
