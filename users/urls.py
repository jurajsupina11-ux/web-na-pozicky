from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('kyc/', views.kyc_form, name='kyc'),
    path('ziadost-o-uver/', views.loan_application, name='loan_application'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('moje-ziadosti/', views.my_applications, name='my_applications'),
    path('moje-pozicky/', views.my_loans, name='my_loans'),
    path('moje-pozicky/<int:loan_id>/odklad/', views.request_postponement, name='request_postponement'),
    path('moje-pozicky/<int:loan_id>/nahlasit-uhradu/', views.report_payment, name='report_payment'),
    path('moje-udaje/', views.my_profile, name='my_profile'),
    path('moje-zmluvy/', views.my_contracts, name='my_contracts'),
    path('nastavenia/', views.account_settings, name='account_settings'),
    path('admin-nahlad/', views.impersonate_list, name='impersonate_list'),
    path('admin-nahlad/<int:user_id>/', views.impersonate_start, name='impersonate_start'),
    path('admin-nahlad/stop/', views.impersonate_stop, name='impersonate_stop'),
]
