from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
import math

# Existing function
def uploaded_location(instance, filename):
    return ("%s/%s") % (instance.car_name, filename)

# Location Model - For nearest car matching
class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Bangladesh')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['city', 'state', 'country']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['city', 'state']),
        ]
    
    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"
    
    def distance_to(self, other_location):
        """Calculate distance between two locations using Haversine formula"""
        if not all([self.latitude, self.longitude, other_location.latitude, other_location.longitude]):
            return float('inf')
        
        R = 6371  
        lat1, lon1 = math.radians(float(self.latitude)), math.radians(float(self.longitude))
        lat2, lon2 = math.radians(float(other_location.latitude)), math.radians(float(other_location.longitude))
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c

# Enhanced Car Model
class Car(models.Model):
    CAR_STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('inactive', 'Inactive'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    image = models.ImageField(upload_to=uploaded_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    car_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    model_year = models.IntegerField(null=True, blank=True)
    num_of_seats = models.IntegerField()
    cost_par_day = models.DecimalField(max_digits=10, decimal_places=2)
    content = models.TextField()
    like = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=CAR_STATUS_CHOICES, default='available')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='manual')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='petrol')
    mileage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    license_plate = models.CharField(max_length=20, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'location']),
            models.Index(fields=['cost_par_day']),
            models.Index(fields=['company_name']),
        ]
    
    def __str__(self):
        return f"{self.company_name} {self.car_name}"
    
    def get_absolute_url(self):
        return "/car/%s/" % (self.id)
    
    @classmethod
    def get_nearest_available_cars(cls, client_location, radius_km=50):
        """Get available cars within specified radius of client location"""
        available_cars = cls.objects.filter(status='available').select_related('location')
        nearby_cars = []
        
        for car in available_cars:
            if car.location:
                distance = client_location.distance_to(car.location)
                if distance <= radius_km:
                    nearby_cars.append({'car': car, 'distance': distance})
        
        # Sort by distance
        nearby_cars.sort(key=lambda x: x['distance'])
        return nearby_cars

# Client Model (Enhanced Customer)
class Client(models.Model):
    CLIENT_CATEGORIES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('corporate', 'Corporate'),
        ('vip', 'VIP'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CLIENT_CATEGORIES, default='regular')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    credit_score = models.IntegerField(default=700)
    total_bookings = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['location']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def update_category(self):
        """Auto-update client category based on bookings"""
        if self.total_bookings >= 50:
            self.category = 'vip'
        elif self.total_bookings >= 20:
            self.category = 'premium'
        elif self.total_bookings >= 5:
            self.category = 'corporate'
        else:
            self.category = 'regular'
        self.save()

# Driver Model with Location
class Driver(models.Model):
    DRIVER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_trip', 'On Trip'),
        ('suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    license_no = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    hired_date = models.DateField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=DRIVER_STATUS_CHOICES, default='active')
    experience_years = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_trips = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'location']),
            models.Index(fields=['salary']),
        ]
    
    def __str__(self):
        try:
            return self.name or f"Driver #{self.id}"
        except:
            return f"Driver #{self.id if self.id else 'Unknown'}"
    
    @classmethod
    def bulk_update_salaries(cls, percentage_increase):
        """Bulk update all driver salaries - ATOMICITY"""
        from decimal import Decimal
        with transaction.atomic():
            drivers = cls.objects.all()
            for driver in drivers:
                driver.salary = driver.salary * (Decimal('1') + Decimal(str(percentage_increase)) / Decimal('100'))
                driver.save()

# Enhanced Order Model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=20, unique=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='pickup_orders')
    dropoff_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='dropoff_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    special_requirements = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['client', 'status']),
            models.Index(fields=['order_id']),
        ]
    
    def __str__(self):
        return f"Order {self.order_id} - {self.car.car_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            import uuid
            self.order_id = f"BHR{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return "/order/detail/%s/" % (self.id)

# Message System
class Message(models.Model):
    MESSAGE_TYPES = [
        ('inquiry', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('feedback', 'Feedback'),
        ('support', 'Support Request'),
    ]
    
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='inquiry')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', 'created_at']),
            models.Index(fields=['message_type']),
        ]
    
    def __str__(self):
        return f"{self.subject} - {self.sender_name}"

# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_edit_salaries = models.BooleanField(default=True)
    can_manage_drivers = models.BooleanField(default=True)
    can_manage_cars = models.BooleanField(default=True)
    can_view_reports = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"Admin - {self.user.username}"

# Driver Application System
class DriverApplication(models.Model):
    APPLICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    license_no = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    experience_years = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['status', 'applied_at']),
            models.Index(fields=['location']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.status}"

# Car Maintenance Log
class CarMaintenance(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_type = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance_date = models.DateField()
    next_maintenance_date = models.DateField(null=True, blank=True)
    performed_by = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-maintenance_date']
    
    def __str__(self):
        return f"{self.car.car_name} - {self.maintenance_type}"

