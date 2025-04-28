# urls.py (Cleaned Version)
from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home_redirect'),  # Optional /home/ URL
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    path('emergency_contact/', views.emergency_contact, name='emergency_contact'),
    path('contact/create/', views.create_contact, name='create_contact'),
    path('contact/update/<int:pk>/', views.update_contact, name='update_contact'),
    path('contact/delete/<int:pk>/', views.delete_contact, name='delete_contact'),

    path('emergency/send/', views.emergency_with_location, name='emergency_location'),
    path('emergency/send-location/', views.send_location_to_contacts, name='send_location'),
    path('emergency/', views.redirect_emergency),

    path('helpline_numbers/', views.helpline_numbers, name='helpline_numbers'),
    path('women_rights/', views.women_rights, name='women_rights'),
    path('women_laws/', views.women_laws, name='women_laws'),
    path('developers/', views.developers, name='developers'),
    path('about_me/', views.about_me, name='about_me'),
    
]
