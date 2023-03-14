from django.contrib import admin
from django.urls import path
from core import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    path('', views.Index.as_view(), name='index'),
    path('fetch', views.Index.fetch, name='fetch-name'),

    path('counter/<str:pk>/', views.Counter.getCounter, name='counter'),
    path('collection/<str:pk>/', views.CollectionView.getCollection, name='collection'),

]
