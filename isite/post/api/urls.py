from django.urls import path

from post.api.views import (
    api_detail_post_view,
    api_update_post_view,
    api_create_post_view,
    api_delete_post_view,
    ApiPostIndexView,
)

app_name = 'post'

urlpatterns = [
    path('detail/<str:slug>', api_detail_post_view, name='detail'),
    path('update/<str:slug>', api_update_post_view, name='update'),
    path('create', api_create_post_view, name='create'),
    path('delete/<str:slug>', api_delete_post_view, name='delete'),
    path('', ApiPostIndexView.as_view(), name='index'),
]
