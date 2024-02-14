import os
from dotenv import load_dotenv
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Subscription
from django.contrib.auth.models import User
from datetime import date, timedelta

load_dotenv()


@shared_task
def email_send(self, post, form):
    html_content = render_to_string('news/send_mail.html', {'post': post})
    category_ids = form.cleaned_data.get('category')
    for categoryi in category_ids:
        category = Subscription(category_id=categoryi.id, user_id=self.request.user.pk)
        category.save()
    for category_id in category_ids:
        for user in User.objects.filter(subscription__category_id=category_id):
            msg = EmailMultiAlternatives(
                subject=f'''Приветствуем, {user}! В твоей любимой категории вышла новость:{post.title}''',
                from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                body=f'{post.text[:50]}..',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def weekly_delivery_cel():
    today = date.today()

    while today.weekday() != 0:
        today = today - timedelta(1)

    post_orm = Post.objects.filter(creation_time_post__date__gte=today)
    html_content = render_to_string('sender_email.html', {'post_orm': post_orm, 'post_c': post_orm.count()})

    for user_sub in Subscription.objects.all():
        for user in User.objects.all():
            if user_sub.user == user:
                msg = EmailMultiAlternatives(subject=f'Количество новостей - {post_orm.count()}',
                                             from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                                             to=[user.email])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
