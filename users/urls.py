from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('kyc/', views.kyc_form, name='kyc'),
    path('ziadost-o-uver/', views.loan_application, name='loan_application'),
    path('moje-ziadosti/', views.my_applications, name='my_applications'),
    path('moje-pozicky/', views.my_loans, name='my_loans'),
    path('moje-udaje/', views.my_profile, name='my_profile'),
    path('moje-zmluvy/', views.my_contracts, name='my_contracts'),
    path('nastavenia/', views.account_settings, name='account_settings'),
    path('admin-nahlad/', views.impersonate_list, name='impersonate_list'),
    path('admin-nahlad/<int:user_id>/', views.impersonate_start, name='impersonate_start'),
    path('admin-nahlad/stop/', views.impersonate_stop, name='impersonate_stop'),
]
