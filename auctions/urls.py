from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionListView.as_view(), name='list'),
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('new/', views.AuctionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='detail'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
]
