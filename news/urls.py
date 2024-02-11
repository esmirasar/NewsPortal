from django.urls import path
from .views import NewsListView, NewsListDetail, PostCreate, PostUpdate, PostDelete, ToSendMail, after_subscription, NewsListSearch

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>', NewsListDetail.as_view()),
    path('search/', NewsListSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscribe/', ToSendMail.as_view(), name='subscribe'),
    path('after_subscription/', after_subscription, name='after_subscription')
]

