from django.urls import path

from . import views

app_name = 'designs'

urlpatterns = [
    path('', views.designs_index, name='index'),
    path('<slug:slug>/', views.design_home, name='home'),
    path('<slug:slug>/miestnosti/', views.design_rooms, name='rooms'),
    path('<slug:slug>/dashboard/', views.design_dashboard, name='dashboard'),
]
