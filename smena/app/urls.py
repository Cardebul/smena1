from django.urls import path
from .views import index, CreateTable, create_worker, create_graphic, choise, delete

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('show/<int:pk>/', index, name='show'),
    path('create/', CreateTable.as_view(), name='create'),
    path('createworkers/', create_worker, name='createworker'),
    path('creategraphic/<int:pk>/', create_graphic, name='creategraphic'),
    path('delete/', choise, name='choise'),
    path('delete/<int:pk>', delete, name='delete'),
    
    
]