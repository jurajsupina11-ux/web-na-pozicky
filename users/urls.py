from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('login/investor/', views.InvestorLoginView.as_view(), name='login_investor'),
    path('login/dlznik/', views.BorrowerLoginView.as_view(), name='login_borrower'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('kyc/', views.kyc_form, name='kyc'),
    path('ziadost-o-uver/', views.loan_application, name='loan_application'),
    path('moje-ziadosti/', views.my_applications, name='my_applications'),
    path('moje-pozicky/', views.my_loans, name='my_loans'),
    path('ponuky/', views.my_offers, name='my_offers'),
    path('moje-pozicky/<int:loan_id>/podpisat-zmluvu/', views.sign_loan_contract, name='sign_loan_contract'),
    path('moje-pozicky/<int:loan_id>/odklad/', views.request_postponement, name='request_postponement'),
    path('moje-pozicky/<int:loan_id>/nahlasit-uhradu/', views.report_payment, name='report_payment'),
    path('moje-udaje/', views.my_profile, name='my_profile'),
    path('moje-zmluvy/', views.my_contracts, name='my_contracts'),
    path('moje-zmluvy/<int:loan_id>/zmluva.pdf', views.contract_loan_agreement_pdf, name='contract_loan_agreement'),
    path('moje-zmluvy/<int:loan_id>/predpis.pdf', views.contract_payment_notice_pdf, name='contract_payment_notice'),
    path(
        'moje-zmluvy/<int:loan_id>/potvrdenie-o-zaniku-dlhu.pdf',
        views.contract_debt_discharge_pdf, name='contract_debt_discharge',
    ),
    path('nastavenia/', views.account_settings, name='account_settings'),
    path('nastavenia/zmena-hesla/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('nastavenia/zmena-hesla/hotovo/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('pozvi-priatela/', views.referral, name='referral'),
    path('admin-nahlad/', views.impersonate_list, name='impersonate_list'),
    path('admin-nahlad/<int:user_id>/', views.impersonate_start, name='impersonate_start'),
    path('admin-nahlad/stop/', views.impersonate_stop, name='impersonate_stop'),
]
