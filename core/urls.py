from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('investori/', views.landing_investor, name='investor'),
    path('pre-ziadatelov/', views.landing_borrower, name='borrower'),
    path('kontakt/', views.contact, name='contact'),
    path('caste-otazky/', views.faq, name='faq'),
    path('obchodne-podmienky/', views.terms, name='terms'),
    path('ochrana-osobnych-udajov/', views.privacy, name='privacy'),
]
