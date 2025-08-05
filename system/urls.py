from django.urls import re_path, path
from django.contrib import admin
from .import views

urlpatterns = [
    # Original URLs
    re_path(r'^$', views.home, name='home'),
    re_path(r'^carlist/$', views.car_list, name="car_list"),
    re_path(r'^createOrder/$', views.order_created, name="order_create"),
    re_path(r'^listOrder/$', views.order_list, name="order_list"),
    re_path(r'^(?P<id>\d+)/edit/$', views.car_update, name="car_edit"),
    re_path(r'^(?P<id>\d+)/$', views.car_detail, name="car_detail"),
    re_path(r'^detail/(?P<id>\d+)/$', views.order_detail, name="order_detail"),
    re_path(r'^(?P<id>\d+)/delete/$', views.car_delete, name="car_delete"),
    re_path(r'^(?P<id>\d+)/deleteOrder/$', views.order_delete, name="order_delete"),
    re_path(r'^contact/$', views.contact, name="contact"),
    re_path(r'^messages/$', views.user_messages, name="user_messages"),
    re_path(r'^newcar/$', views.newcar, name="newcar"),
    re_path(r'^(?P<id>\d+)/like/$', views.like_update, name="like"),
    re_path(r'^popularcar/$', views.popular_car, name="popularcar"),
    
    # NEW ADVANCED DBMS URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nearest-cars/', views.nearest_cars, name='nearest_cars'),
    path('clients/', views.client_list, name='client_list'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('bulk-salary-update/', views.bulk_salary_update, name='bulk_salary_update'),
    path('driver-applications/', views.driver_applications, name='driver_applications'),
    path('approve-application/<int:application_id>/', views.approve_driver_application, name='approve_application'),
    path('reject-application/<int:application_id>/', views.reject_driver_application, name='reject_application'),
    path('enhanced-cars/', views.enhanced_car_list, name='enhanced_car_list'),
    path('enhanced-orders/', views.enhanced_order_list, name='enhanced_order_list'),
    path('locations/', views.location_list, name='location_list'),
    path('maintenance/', views.car_maintenance_log, name='car_maintenance'),
    path('analytics/', views.analytics, name='analytics'),
    
    # Admin URLs for backwards compatibility
    re_path(r'^admin/$', views.admin_car_list, name='admin_index'),
    re_path(r'^message/delete/(?P<id>\d+)/$', views.msg_delete, name='msg_delete'),
]
