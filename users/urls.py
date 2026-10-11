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
]
