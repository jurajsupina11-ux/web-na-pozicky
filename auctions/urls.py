from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionListView.as_view(), name='list'),
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('ziadosti/', views.open_auctions_view, name='open_auctions'),
    path('trh/', views.marketplace, name='marketplace'),
    path('trh/<int:bid_id>/kupit/', views.marketplace_buy, name='marketplace_buy'),
    path('penazenka/vklad/', views.wallet_deposit, name='wallet_deposit'),
    path('penazenka/vyber/', views.wallet_withdraw, name='wallet_withdraw'),
    path('investicia/<int:bid_id>/predaj/', views.bid_toggle_sale, name='bid_toggle_sale'),
    path('new/', views.AuctionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='detail'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
]
