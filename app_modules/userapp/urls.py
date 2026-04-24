from django.contrib import admin
from django.urls import path,include
from app_modules.userapp import views



urlpatterns = [
    path('', views.home_page, name='home_page'),
    
    #Login Start  
    path('register/', views.register_view, name='user_register'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject/<int:user_id>/', views.reject_user, name='reject_user'),
    #Login End 
    
    #User Profile Start
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/delete-image/', views.delete_profile_image, name='delete_profile_image'),
    
    #User Profile End
    
    #Booking Start
    path('booking/<int:id>/', views.booking_page, name='booking_page'),
    path('start-booking/', views.start_booking, name='start_booking'),
    
    path('user/bookings/', views.list_Booking_user, name='list_Booking_user'),
    path('booking/update/<int:id>/', views.update_Booking, name='update_Booking'),
    path('booking/delete/<int:id>/', views.delete_booking, name='delete_booking'),
    path('booking/cancel/<int:id>/', views.cancel_booking, name='cancel_booking'),
    
    #Booking End   
    
    path('car/', views.car_page, name='car_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('service/', views.service_page, name='service_page'),
    path('why_choose/', views.why_choose_page, name='why_choose_page'),
    path('testimonial/',views.testimonial_page, name='testimonial_page'),
    path('about/', views.about_page, name='about_page'),
   
    
    
]
