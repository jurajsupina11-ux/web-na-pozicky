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
    path('statistiky/', views.public_stats, name='public_stats'),
    path('notifikacie/', views.notifications_list, name='notifications'),
    path('notifikacie/precitat/<int:pk>/', views.notification_mark_read, name='notification_mark_read'),
    path('notifikacie/precitat-vsetky/', views.notifications_mark_all_read, name='notifications_mark_all_read'),
]
