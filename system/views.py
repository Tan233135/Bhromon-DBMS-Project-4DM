from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Q, Count, Avg
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime, timedelta

from .models import Car, Order, Message, Location, Client, Driver, DriverApplication, CarMaintenance, Admin
from .forms import CarForm, OrderForm, MessageForm



def home(request):
    context = {
        "title" : "Car Rental"
    }
    return render(request,'home.html', context)

def car_list(request):
    car = Car.objects.all().order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
                     Q(car_name__icontains=query) |
                     Q(company_name__icontains = query) |
                     Q(num_of_seats__icontains=query) |
                     Q(cost_par_day__icontains=query)
                            )

    paginator = Paginator(car, 12)  
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        car = paginator.page(1)
    except EmptyPage:
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'car_list.html', context)

def car_detail(request, id=None):
    detail = get_object_or_404(Car,id=id)
    context = {
        "detail": detail
    }
    return render(request, 'car_detail.html', context)

def car_created(request):
    form = CarForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/")
    context = {
        "form" : form,
        "title": "Create Car"
    }
    return render(request, 'car_create.html', context)

def car_update(request, id=None):
    detail = get_object_or_404(Car, id=id)
    form = CarForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Car"
    }
    return render(request, 'car_create.html', context)

def car_delete(request,id=None):
    query = get_object_or_404(Car,id = id)
    query.delete()

    car = Car.objects.all()
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)


def order_list(request):
    order = Order.objects.all().order_by('-id')

    query = request.GET.get('q')
    if query:
        order = order.filter(
            Q(car__car_name__icontains=query)|
            Q(client__first_name__icontains=query)|
            Q(client__last_name__icontains=query)|
            Q(order_id__icontains=query)
        )

    paginator = Paginator(order, 4) 
    page = request.GET.get('page')
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        order = paginator.page(1)
    except EmptyPage:
        order = paginator.page(paginator.num_pages)
    context = {
        'order': order,
    }
    return render(request, 'order_list.html', context)

def order_detail(request, id=None):
    detail = get_object_or_404(Order,id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'order_detail.html', context)

def order_created(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    
                    # Check car availability
                    car = order.car
                    if car.status != 'available':
                        messages.error(request, 'This car is not available for rent.')
                        return HttpResponseRedirect(reverse('order_create'))

                    # Update car status to 'rented'
                    car.status = 'rented'
                    car.save()
                    
                    # Save the order
                    order.save()
                    
                    # Update client's total bookings
                    client = order.client
                    client.total_bookings += 1
                    client.update_category()
                    
                    messages.success(request, f'Order {order.order_id} has been created successfully!')
                    return HttpResponseRedirect(reverse('order_list'))
            except Exception as e:
                messages.error(request, f'An error occurred while creating the order: {str(e)}')
    else:
        form = OrderForm()

    # Get all cars for the dropdown and JavaScript calculation
    cars = Car.objects.filter(status='available')
    context = {
        "form": form,
        "title": "Create Order",
        "cars": cars
    }
    return render(request, 'order_create.html', context)

def order_update(request, id=None):
    detail = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Order"
    }
    return render(request, 'order_create.html', context)

def order_delete(request,id=None):
    query = get_object_or_404(Order,id = id)
    query.delete()
    return HttpResponseRedirect("/listOrder/")

def newcar(request):
    new = Car.objects.order_by('-id')
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )


    paginator = Paginator(new, 12) 
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        new = paginator.page(1)
    except EmptyPage:
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)

def like_update(request, id=None):
    new = Car.objects.order_by('-id')
    like_count = get_object_or_404(Car, id=id)
    like_count.like+=1
    like_count.save()
    context = {
        'car': new,
    }
    return render(request,'new_car.html',context)

def popular_car(request):
    new = Car.objects.order_by('-like')
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    paginator = Paginator(new, 12)
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        new = paginator.page(1)
    except EmptyPage:
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)

def contact(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.save()
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return HttpResponseRedirect(reverse('contact'))
            except Exception as e:
                messages.error(request, f'An error occurred while sending your message: {str(e)}')
    else:
        form = MessageForm()
    
    context = {
        "form": form,
        "title": "Contact With Us",
    }
    return render(request,'contact.html', context)


def admin_car_list(request):
    car = Car.objects.order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query)
        )

    paginator = Paginator(car, 12)
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        car = paginator.page(1)
    except EmptyPage:
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)

def admin_msg(request):
    msg = Message.objects.order_by('-id')
    context={
        "car": msg,
    }
    return render(request, 'admin_msg.html', context)

def user_messages(request):
    """Display messages for regular users"""
    # Get all messages, ordered by most recent first
    messages_list = Message.objects.all().order_by('-created_at')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        messages_list = messages_list.filter(
            Q(sender_name__icontains=query) |
            Q(sender_email__icontains=query) |
            Q(subject__icontains=query)
        )
    
    # Filter by message type
    message_type = request.GET.get('type')
    if message_type:
        messages_list = messages_list.filter(message_type=message_type)
    
    paginator = Paginator(messages_list, 10)
    page = request.GET.get('page')
    try:
        messages_list = paginator.page(page)
    except PageNotAnInteger:
        messages_list = paginator.page(1)
    except EmptyPage:
        messages_list = paginator.page(paginator.num_pages)
    
    context = {
        'messages_list': messages_list,
        'message_types': Message.MESSAGE_TYPES,
        'selected_type': message_type,
        'query': query,
    }
    return render(request, 'user_messages.html', context)

def msg_delete(request,id=None):
    query = get_object_or_404(Message, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")

# NEW ADVANCED DBMS VIEWS

def dashboard(request):
    """Main dashboard with statistics"""
    context = {
        'total_cars': Car.objects.count(),
        'available_cars': Car.objects.filter(status='available').count(),
        'total_drivers': Driver.objects.count(),
        'active_drivers': Driver.objects.filter(status='active').count(),
        'total_clients': Client.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'locations': Location.objects.count(),
        'pending_applications': DriverApplication.objects.filter(status='pending').count(),
    }
    return render(request, 'dashboard.html', context)

def nearest_cars(request):
    """Find nearest available cars based on client location"""
    locations = Location.objects.all()
    cars = []
    selected_location = None
    
    if request.GET.get('location_id'):
        try:
            selected_location = Location.objects.get(id=request.GET.get('location_id'))
            radius = int(request.GET.get('radius', 50))
            nearby_cars = Car.get_nearest_available_cars(selected_location, radius)
            cars = nearby_cars
        except (Location.DoesNotExist, ValueError):
            pass
    
    context = {
        'locations': locations,
        'cars': cars,
        'selected_location': selected_location,
        'radius': request.GET.get('radius', 50)
    }
    return render(request, 'nearest_cars.html', context)

def client_list(request):
    """List all clients with categories"""
    clients = Client.objects.all().order_by('-created_on')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        clients = clients.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        clients = clients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    
    paginator = Paginator(clients, 15)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)
    
    # Statistics
    client_stats = Client.objects.values('category').annotate(count=Count('id'))
    
    context = {
        'clients': clients,
        'client_stats': client_stats,
        'categories': Client.CLIENT_CATEGORIES,
        'selected_category': category
    }
    return render(request, 'client_list.html', context)

def driver_list(request):
    """List all drivers with management options"""
    drivers = Driver.objects.all().order_by('-hired_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        drivers = drivers.filter(status=status)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        drivers = drivers.filter(
            Q(name__icontains=query) |
            Q(license_no__icontains=query) |
            Q(contact_number__icontains=query)
        )
    
    paginator = Paginator(drivers, 15)
    page = request.GET.get('page')
    try:
        drivers = paginator.page(page)
    except PageNotAnInteger:
        drivers = paginator.page(1)
    except EmptyPage:
        drivers = paginator.page(paginator.num_pages)
    
    # Statistics
    driver_stats = {
        'total': Driver.objects.count(),
        'active': Driver.objects.filter(status='active').count(),
        'inactive': Driver.objects.filter(status='inactive').count(),
        'on_trip': Driver.objects.filter(status='on_trip').count(),
        'average_salary': Driver.objects.aggregate(avg_salary=Avg('salary'))['avg_salary'] or 0
    }
    
    context = {
        'drivers': drivers,
        'driver_stats': driver_stats,
        'statuses': Driver.DRIVER_STATUS_CHOICES,
        'selected_status': status
    }
    return render(request, 'driver_list.html', context)

@require_http_methods(["POST"])
def bulk_salary_update(request):
    """Bulk update driver salaries - ATOMICITY demonstration"""
    try:
        percentage = float(request.POST.get('percentage', 0))
        driver_ids = request.POST.getlist('driver_ids')
        
        if percentage and driver_ids:
            with transaction.atomic():
                from decimal import Decimal
                drivers = Driver.objects.filter(id__in=driver_ids)
                for driver in drivers:
                    driver.salary = driver.salary * (Decimal('1') + Decimal(str(percentage)) / Decimal('100'))
                    driver.save()
                
                messages.success(request, f"Successfully updated salaries for {len(driver_ids)} drivers by {percentage}%")
        else:
            messages.error(request, "Please provide percentage and select drivers")
    except ValueError:
        messages.error(request, "Invalid percentage value")
    except Exception as e:
        messages.error(request, f"Error updating salaries: {str(e)}")
    
    return HttpResponseRedirect(reverse('driver_list'))

def driver_applications(request):
    """Driver application system"""
    applications = DriverApplication.objects.all().order_by('-applied_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    paginator = Paginator(applications, 15)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    
    context = {
        'applications': applications,
        'statuses': DriverApplication.APPLICATION_STATUS_CHOICES,
        'selected_status': status
    }
    return render(request, 'driver_applications.html', context)

def approve_driver_application(request, application_id):
    """Approve a driver application"""
    application = get_object_or_404(DriverApplication, id=application_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Create new driver
                driver = Driver.objects.create(
                    name=application.name,
                    license_no=application.license_no,
                    contact_number=application.contact_number,
                    address=application.address,
                    salary=25000.00,  # Default salary
                    location=application.location,
                    experience_years=application.experience_years
                )
                
                # Update application status
                application.status = 'approved'
                application.reviewed_at = datetime.now()
                application.save()
                
                messages.success(request, f"Driver application approved! {driver.name} has been added as a driver.")
        except Exception as e:
            messages.error(request, f"Error approving application: {str(e)}")
    
    return HttpResponseRedirect(reverse('driver_applications'))

def reject_driver_application(request, application_id):
    """Reject a driver application"""
    application = get_object_or_404(DriverApplication, id=application_id)
    
    if request.method == 'POST':
        application.status = 'rejected'
        application.reviewed_at = datetime.now()
        application.notes = request.POST.get('notes', '')
        application.save()
        
        messages.success(request, f"Driver application rejected.")
    
    return HttpResponseRedirect(reverse('driver_applications'))

def enhanced_car_list(request):
    """Enhanced car list with advanced filtering"""
    cars = Car.objects.all().select_related('location').order_by('-created_at')
    
    # Advanced filtering
    status = request.GET.get('status')
    if status:
        cars = cars.filter(status=status)
    
    fuel_type = request.GET.get('fuel_type')
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    transmission = request.GET.get('transmission')
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    location_id = request.GET.get('location_id')
    if location_id:
        cars = cars.filter(location_id=location_id)
    
    # Price range filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        cars = cars.filter(cost_par_day__gte=min_price)
    if max_price:
        cars = cars.filter(cost_par_day__lte=max_price)
    
    # Search
    query = request.GET.get('q')
    if query:
        cars = cars.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(license_plate__icontains=query)
        )
    
    paginator = Paginator(cars, 12)
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    
    context = {
        'cars': cars,
        'locations': Location.objects.all(),
        'statuses': Car.CAR_STATUS_CHOICES,
        'fuel_types': Car.FUEL_CHOICES,
        'transmissions': Car.TRANSMISSION_CHOICES,
        'filters': {
            'status': status,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'location_id': location_id,
            'min_price': min_price,
            'max_price': max_price,
            'query': query,
        }
    }
    return render(request, 'enhanced_car_list.html', context)

def enhanced_order_list(request):
    """Enhanced order list with relationships"""
    orders = Order.objects.all().select_related('car', 'client', 'driver', 'pickup_location', 'dropoff_location').order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Filter by client category
    client_category = request.GET.get('client_category')
    if client_category:
        orders = orders.filter(client__category=client_category)
    
    paginator = Paginator(orders, 15)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    
    # Statistics
    order_stats = {
        'total': Order.objects.count(),
        'pending': Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'ongoing': Order.objects.filter(status='ongoing').count(),
        'completed': Order.objects.filter(status='completed').count(),
    }
    
    context = {
        'orders': orders,
        'order_stats': order_stats,
        'statuses': Order.ORDER_STATUS_CHOICES,
        'client_categories': Client.CLIENT_CATEGORIES,
        'filters': {
            'status': status,
            'client_category': client_category,
        }
    }
    return render(request, 'enhanced_order_list.html', context)

def location_list(request):
    """List and manage locations"""
    locations = Location.objects.all().order_by('country', 'state', 'city')
    
    # Add car and client counts for each location
    for location in locations:
        location.car_count = Car.objects.filter(location=location).count()
        location.client_count = Client.objects.filter(location=location).count()
        location.driver_count = Driver.objects.filter(location=location).count()
    
    context = {
        'locations': locations,
    }
    return render(request, 'location_list.html', context)

def car_maintenance_log(request):
    """Car maintenance tracking"""
    maintenance_logs = CarMaintenance.objects.all().select_related('car').order_by('-maintenance_date')
    
    # Filter by car if specified
    car_id = request.GET.get('car_id')
    if car_id:
        maintenance_logs = maintenance_logs.filter(car_id=car_id)
    
    paginator = Paginator(maintenance_logs, 20)
    page = request.GET.get('page')
    try:
        maintenance_logs = paginator.page(page)
    except PageNotAnInteger:
        maintenance_logs = paginator.page(1)
    except EmptyPage:
        maintenance_logs = paginator.page(paginator.num_pages)
    
    context = {
        'maintenance_logs': maintenance_logs,
        'cars': Car.objects.all(),
        'selected_car_id': car_id,
    }
    return render(request, 'car_maintenance.html', context)

def analytics(request):
    """Analytics dashboard"""
    # Car analytics
    car_by_status = Car.objects.values('status').annotate(count=Count('id'))
    car_by_company = Car.objects.values('company_name').annotate(count=Count('id')).order_by('-count')[:5]
    
    # Client analytics
    client_by_category = Client.objects.values('category').annotate(count=Count('id'))
    
    # Order analytics  
    order_by_status = Order.objects.values('status').annotate(count=Count('id'))
    
    # Driver analytics
    driver_by_status = Driver.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'car_by_status': list(car_by_status),
        'car_by_company': list(car_by_company),
        'client_by_category': list(client_by_category),
        'order_by_status': list(order_by_status),
        'driver_by_status': list(driver_by_status),
    }
    return render(request, 'analytics.html', context)
