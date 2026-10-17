from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.AuctionListView.as_view(), name='list'),
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('historia/', views.investor_history, name='investor_history'),
    path('historia/export.pdf', views.investor_history_pdf, name='investor_history_pdf'),
    path('moje-zmluvy/', views.investor_contracts, name='investor_contracts'),
    path('danovy-vykaz/', views.tax_statement, name='tax_statement'),
    path('danovy-vykaz/<int:year>/export.pdf', views.tax_statement_pdf, name='tax_statement_pdf'),
    path('investicia/<int:bid_id>/zmluva.pdf', views.contract_loan_agreement_pdf, name='contract_loan_agreement'),
    path(
        'investicia/<int:bid_id>/zmluva-o-postupeni.pdf',
        views.contract_assignment_agreement_pdf, name='contract_assignment_agreement',
    ),
    path(
        'investicia/<int:bid_id>/oznamenie-o-postupeni.pdf',
        views.contract_assignment_notice_pdf, name='contract_assignment_notice',
    ),
    path('ziadosti/', views.open_auctions_view, name='open_auctions'),
    path('trh/', views.marketplace, name='marketplace'),
    path('trh/<int:bid_id>/kupit/', views.marketplace_buy, name='marketplace_buy'),
    path('penazenka/vklad/', views.wallet_deposit, name='wallet_deposit'),
    path('penazenka/vklad/qr-platba.png', views.deposit_payment_qr, name='deposit_payment_qr'),
    path('penazenka/vyber/', views.wallet_withdraw, name='wallet_withdraw'),
    path('investicia/<int:bid_id>/predaj/', views.bid_toggle_sale, name='bid_toggle_sale'),
    path('new/', views.AuctionCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AuctionDetailView.as_view(), name='detail'),
    path('<int:pk>/bid/', views.place_bid, name='place_bid'),
]
