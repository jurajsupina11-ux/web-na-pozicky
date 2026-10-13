from django.urls import path

from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('ziadosti/', views.applications_list, name='applications_list'),
    path('ziadosti/<int:pk>/', views.application_detail, name='application_detail'),
    path('ziadosti/<int:pk>/schvalit/', views.application_approve, name='application_approve'),
    path('ziadosti/<int:pk>/zamietnut/', views.application_reject, name='application_reject'),
    path('ziadosti/<int:pk>/protiponuka/', views.application_counter_offer, name='application_counter_offer'),

    path('penazenka/', views.wallet_list, name='wallet_list'),
    path('penazenka/<int:pk>/potvrdit/', views.wallet_confirm, name='wallet_confirm'),
    path('penazenka/<int:pk>/zamietnut/', views.wallet_reject, name='wallet_reject'),

    path('pozicky/', views.loans_list, name='loans_list'),

    path('pouzivatelia/', views.users_list, name='users_list'),
    path('pouzivatelia/<int:pk>/', views.user_detail, name='user_detail'),
    path('pouzivatelia/<int:pk>/blokovat/', views.user_toggle_block, name='user_toggle_block'),

    path('trh/', views.marketplace_list, name='marketplace_list'),
    path('audit/', views.audit_log, name='audit_log'),
    path('zmluvy/', views.contracts_list, name='contracts_list'),
    path('nastavenia/', views.settings_view, name='settings'),
]
