
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('get_all/', views.get_all, name='get_all'),
    path('person/', views.person, name='person'),
    path('person/<int:person_id>/', views.person, name='person'),
    path('create_relation/', views.create_relation, name='create_relation'),
    path('get_relatives/', views.get_relatives, name='get_relatives'),
    
]
