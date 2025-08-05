from django.contrib import admin
from .models import (
    Car, Order, Message, Location, Client, Driver, 
    Admin, DriverApplication, CarMaintenance
)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country', 'latitude', 'longitude')
    list_filter = ('country', 'state')
    search_fields = ('city', 'state')

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('car_name', 'company_name', 'status', 'cost_par_day', 'location')
    list_filter = ('status', 'company_name', 'fuel_type', 'transmission')
    search_fields = ('car_name', 'company_name', 'license_plate')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'category', 'total_bookings', 'location')
    list_filter = ('category', 'is_verified', 'location')
    search_fields = ('first_name', 'last_name', 'email', 'license_number')
    readonly_fields = ('created_on',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_no', 'salary', 'status', 'rating', 'location')
    list_filter = ('status', 'location')
    search_fields = ('name', 'license_no', 'contact_number')
    readonly_fields = ('hired_date',)
    list_per_page = 25
    ordering = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'car', 'client', 'driver', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'car__car_name', 'client__email')
    readonly_fields = ('order_id', 'created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender_name', 'sender_email', 'message_type', 'is_read', 'created_at')
    list_filter = ('message_type', 'is_read', 'created_at')
    search_fields = ('sender_name', 'sender_email', 'subject')
    readonly_fields = ('created_at',)

@admin.register(Admin)
class AdminModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_edit_salaries', 'can_manage_drivers', 'can_manage_cars')
    list_filter = ('can_edit_salaries', 'can_manage_drivers')

@admin.register(DriverApplication)
class DriverApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'experience_years', 'applied_at')
    list_filter = ('status', 'applied_at', 'location')
    search_fields = ('name', 'email', 'license_no')
    readonly_fields = ('applied_at',)

@admin.register(CarMaintenance)
class CarMaintenanceAdmin(admin.ModelAdmin):
    list_display = ('car', 'maintenance_type', 'cost', 'maintenance_date')
    list_filter = ('maintenance_type', 'maintenance_date')
    search_fields = ('car__car_name', 'maintenance_type')
