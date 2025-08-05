from django.urls import path, include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from system.views import admin_car_list, admin_msg, order_list, car_created, order_update, order_delete, msg_delete
from accounts.views import (login_view, register_view, logout_view)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    # Admin routes
    path('car/admin/', admin_car_list, name='admin_car_list'),
    path('message/', admin_msg, name='admin_message'),
    path('listOrder/', order_list, name='list_order'),
    path('create/', car_created, name='car_create'),
    path('order/', include('system.urls')),
    path('car/', include('system.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
