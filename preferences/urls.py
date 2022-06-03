from django.urls import re_path, include
from django.urls import path
from django.views.static import serve

from preferences import views
from pbrlwebapp import settings

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('queries/', views.query_list),
    path('query/<uuid:query_id>', views.query_detail),
    path('', views.QueryListView.as_view(), name='index'),
    path('<uuid:query_id>', views.query, name='query'),
    path('next', views.next_query, name='next'),
    re_path(r'^(?P<path>.*)$', serve,
        {'document_root': settings.BASE_DIR / 'videofiles'})
]
