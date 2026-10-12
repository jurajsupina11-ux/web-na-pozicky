from django.urls import path

from . import views

app_name = 'designs'

urlpatterns = [
    path('', views.designs_index, name='index'),
    path('<slug:slug>/', views.design_home, name='home'),
    path('<slug:slug>/miestnosti/', views.design_rooms, name='rooms'),
    path('<slug:slug>/dashboard/', views.design_dashboard, name='dashboard'),
    path('<slug:slug>/pozicka/<int:loan_id>/', views.design_loan_detail, name='loan_detail'),
    path('<slug:slug>/ako-to-funguje/', views.design_how_it_works, name='how_it_works'),
    path('<slug:slug>/moje-pozicky/', views.design_my_loans, name='my_loans'),
    path('uvodna-stranka/v1/', views.landing_mockup_v1, name='landing_v1'),
    path('uvodna-stranka/v2/', views.landing_mockup_v2, name='landing_v2'),
    path('uvodna-stranka/v3/', views.landing_mockup_v3, name='landing_v3'),
]
