from django.urls import path
from .views import NewsListView, NewsListDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>', NewsListDetail.as_view()),
    path('search/', NewsListView.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete')
]

