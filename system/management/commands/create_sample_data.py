from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from system.models import Location, Car, Client, Driver, DriverApplication, Order, Message, Admin, CarMaintenance
from decimal import Decimal
import random
from datetime import datetime, timedelta, date
import uuid

class Command(BaseCommand):
    help = 'Create sample data for testing the car rental system'

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create 20 Locations across Bangladesh
        locations_data = [
            ("Dhaka", "Dhaka", "Bangladesh", Decimal("23.8103"), Decimal("90.4125"), "1000"),
            ("Chittagong", "Chittagong", "Bangladesh", Decimal("22.3569"), Decimal("91.7832"), "4000"),
            ("Sylhet", "Sylhet", "Bangladesh", Decimal("24.8949"), Decimal("91.8687"), "3100"),
            ("Cox's Bazar", "Chittagong", "Bangladesh", Decimal("21.4272"), Decimal("92.0058"), "4700"),
            ("Rangpur", "Rangpur", "Bangladesh", Decimal("25.7439"), Decimal("89.2752"), "5400"),
            ("Rajshahi", "Rajshahi", "Bangladesh", Decimal("24.3636"), Decimal("88.6241"), "6000"),
            ("Khulna", "Khulna", "Bangladesh", Decimal("22.8456"), Decimal("89.5403"), "9000"),
            ("Barisal", "Barisal", "Bangladesh", Decimal("22.7010"), Decimal("90.3535"), "8200"),
            ("Comilla", "Chittagong", "Bangladesh", Decimal("23.4607"), Decimal("91.1809"), "3500"),
            ("Mymensingh", "Mymensingh", "Bangladesh", Decimal("24.7471"), Decimal("90.4203"), "2200"),
            ("Jessore", "Khulna", "Bangladesh", Decimal("23.1667"), Decimal("89.2167"), "7400"),
            ("Narayanganj", "Dhaka", "Bangladesh", Decimal("23.6238"), Decimal("90.4993"), "1400"),
            ("Bogra", "Rajshahi", "Bangladesh", Decimal("24.8465"), Decimal("89.3773"), "5800"),
            ("Dinajpur", "Rangpur", "Bangladesh", Decimal("25.6217"), Decimal("88.6354"), "5200"),
            ("Tangail", "Dhaka", "Bangladesh", Decimal("24.2513"), Decimal("89.9167"), "1900"),
            ("Pabna", "Rajshahi", "Bangladesh", Decimal("24.0064"), Decimal("89.2372"), "6600"),
            ("Kushtia", "Khulna", "Bangladesh", Decimal("23.9013"), Decimal("89.1200"), "7000"),
            ("Faridpur", "Dhaka", "Bangladesh", Decimal("23.6070"), Decimal("89.8429"), "7800"),
            ("Gazipur", "Dhaka", "Bangladesh", Decimal("23.9999"), Decimal("90.4203"), "1700"),
            ("Brahmanbaria", "Chittagong", "Bangladesh", Decimal("23.9570"), Decimal("91.1119"), "3400"),
        ]

        locations = []
        for city, state, country, lat, lng, zip_code in locations_data:
            location, created = Location.objects.get_or_create(
                city=city,
                state=state,
                country=country,
                defaults={
                    'latitude': lat,
                    'longitude': lng,
                    'zip_code': zip_code
                }
            )
            locations.append(location)
            if created:
                self.stdout.write(f"Created location: {location}")

        # Create 20 Cars with realistic data
        cars_data = [
            ("Toyota", "Corolla", 2022, 5, Decimal("3500.00"), "petrol", "automatic", Decimal("15.5")),
            ("Honda", "Civic", 2021, 5, Decimal("4000.00"), "petrol", "manual", Decimal("14.8")),
            ("Nissan", "Sentra", 2023, 5, Decimal("3800.00"), "petrol", "automatic", Decimal("16.2")),
            ("Toyota", "Prius", 2022, 5, Decimal("4500.00"), "hybrid", "automatic", Decimal("25.0")),
            ("Tesla", "Model 3", 2023, 5, Decimal("8000.00"), "electric", "automatic", Decimal("0.0")),
            ("Hyundai", "Elantra", 2021, 5, Decimal("3200.00"), "petrol", "manual", Decimal("13.9")),
            ("Ford", "Focus", 2022, 5, Decimal("3600.00"), "petrol", "automatic", Decimal("14.5")),
            ("BMW", "3 Series", 2023, 5, Decimal("7500.00"), "petrol", "automatic", Decimal("12.0")),
            ("Mercedes", "C-Class", 2022, 5, Decimal("8500.00"), "petrol", "automatic", Decimal("11.5")),
            ("Audi", "A4", 2023, 5, Decimal("8000.00"), "petrol", "automatic", Decimal("12.5")),
            ("Mazda", "3", 2021, 5, Decimal("3400.00"), "petrol", "manual", Decimal("15.8")),
            ("Volkswagen", "Jetta", 2022, 5, Decimal("3700.00"), "petrol", "automatic", Decimal("14.2")),
            ("Kia", "Optima", 2021, 5, Decimal("3300.00"), "petrol", "manual", Decimal("14.6")),
            ("Mitsubishi", "Lancer", 2020, 5, Decimal("2800.00"), "petrol", "manual", Decimal("13.2")),
            ("Subaru", "Impreza", 2022, 5, Decimal("3900.00"), "petrol", "automatic", Decimal("13.8")),
            ("Lexus", "IS", 2023, 5, Decimal("9500.00"), "hybrid", "automatic", Decimal("22.3")),
            ("Infiniti", "Q50", 2021, 5, Decimal("6500.00"), "petrol", "automatic", Decimal("10.8")),
            ("Genesis", "G70", 2022, 5, Decimal("7000.00"), "petrol", "automatic", Decimal("11.2")),
            ("Acura", "TLX", 2021, 5, Decimal("5500.00"), "petrol", "automatic", Decimal("12.8")),
            ("Volvo", "S60", 2023, 5, Decimal("7800.00"), "hybrid", "automatic", Decimal("20.5")),
        ]

        cars = []
        for i, (company, model, year, seats, cost, fuel, transmission, mileage) in enumerate(cars_data):
            car, created = Car.objects.get_or_create(
                company_name=company,
                car_name=model,
                model_year=year,
                defaults={
                    'num_of_seats': seats,
                    'cost_par_day': cost,
                    'fuel_type': fuel,
                    'transmission': transmission,
                    'mileage': mileage,
                    'location': random.choice(locations),
                    'status': random.choice(['available', 'available', 'available', 'rented']),
                    'license_plate': f"DHK-{1000 + i}",
                    'content': f"Excellent {company} {model} in great condition. Perfect for city driving."
                }
            )
            cars.append(car)
            if created:
                self.stdout.write(f"Created car: {car}")

        # Create 20 Clients with realistic data
        clients_data = [
            ("John", "Doe", "john.doe@email.com", "+8801711111111", "123 Main St, Chittagong", "1990-01-15"),
            ("Jane", "Smith", "jane.smith@email.com", "+8801722222222", "456 Oak Ave, Dhaka", "1985-05-20"),
            ("Mike", "Johnson", "mike.johnson@email.com", "+8801733333333", "789 Pine Rd, Sylhet", "1992-09-10"),
            ("Sarah", "Wilson", "sarah.wilson@email.com", "+8801744444444", "321 Elm St, Cox's Bazar", "1988-12-03"),
            ("David", "Brown", "david.brown@email.com", "+8801755555555", "654 Maple Dr, Rangpur", "1995-07-25"),
            ("Emily", "Jones", "emily.jones@email.com", "+8801766666666", "987 Birch Ln, Rajshahi", "1998-03-12"),
            ("Chris", "Davis", "chris.davis@email.com", "+8801777777777", "159 Cedar Blvd, Khulna", "1989-11-30"),
            ("Jessica", "Miller", "jessica.miller@email.com", "+8801788888888", "753 Spruce Ct, Barisal", "1991-08-18"),
            ("Matthew", "Garcia", "matthew.garcia@email.com", "+8801799999999", "852 Aspen Way, Comilla", "1994-06-22"),
            ("Ashley", "Rodriguez", "ashley.rodriguez@email.com", "+8801811111111", "951 Holly Dr, Mymensingh", "1996-04-05"),
            ("Kevin", "Martinez", "kevin.martinez@email.com", "+8801822222222", "369 Redwood Pkwy, Jessore", "1987-02-14"),
            ("Amanda", "Hernandez", "amanda.hernandez@email.com", "+8801833333333", "147 Magnolia Ave, Narayanganj", "1993-10-08"),
            ("Jason", "Lopez", "jason.lopez@email.com", "+8801844444444", "258 Walnut St, Bogra", "1997-07-19"),
            ("Melissa", "Gonzalez", "melissa.gonzalez@email.com", "+8801855555555", "369 Chestnut Rd, Dinajpur", "1999-05-28"),
            ("Joshua", "Perez", "joshua.perez@email.com", "+8801866666666", "741 Dogwood Ln, Tangail", "1986-09-01"),
            ("Stephanie", "Sanchez", "stephanie.sanchez@email.com", "+8801877777777", "852 Cypress Ct, Pabna", "1990-12-24"),
            ("Brian", "Ramirez", "brian.ramirez@email.com", "+8801888888888", "963 Sequoia Dr, Kushtia", "1992-02-29"),
            ("Nicole", "Torres", "nicole.torres@email.com", "+8801899999999", "159 Poplar Way, Faridpur", "1995-11-11"),
            ("Ryan", "Flores", "ryan.flores@email.com", "+8801911111111", "753 Sycamore Blvd, Gazipur", "1998-08-08"),
            ("Elizabeth", "Rivera", "elizabeth.rivera@email.com", "+8801922222222", "852 Hemlock Rd, Brahmanbaria", "1991-03-03"),
        ]

        clients = []
        for i, (first, last, email, phone, address, dob) in enumerate(clients_data):
            client, created = Client.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'phone_number': phone,
                    'address': address,
                    'date_of_birth': datetime.strptime(dob, "%Y-%m-%d").date(),
                    'license_number': f"DL{10000 + i}",
                    'location': random.choice(locations),
                    'category': random.choice(['regular', 'premium', 'corporate']),
                    'total_bookings': random.randint(0, 15),
                    'credit_score': random.randint(650, 800)
                }
            )
            clients.append(client)
            if created:
                self.stdout.write(f"Created client: {client}")

        # Create 20 Drivers with realistic data
        drivers_data = [
            ("Ahmed Rahman", "DL001", "+8801611111111", "100 Driver St, Chittagong", Decimal("25000.00"), 5),
            ("Karim Hassan", "DL002", "+8801622222222", "200 Driver Ave, Dhaka", Decimal("28000.00"), 8),
            ("Rahim Ali", "DL003", "+8801633333333", "300 Driver Rd, Sylhet", Decimal("24000.00"), 3),
            ("Nasir Ahmed", "DL004", "+8801644444444", "400 Driver St, Cox's Bazar", Decimal("26000.00"), 6),
            ("Farhan Khan", "DL005", "+8801655555555", "500 Driver Dr, Rangpur", Decimal("27000.00"), 7),
            ("Mohammad Islam", "DL006", "+8801666666666", "600 Driver Way, Rajshahi", Decimal("29000.00"), 9),
            ("Abdul Latif", "DL007", "+8801677777777", "700 Driver Ln, Khulna", Decimal("23000.00"), 2),
            ("Rashid Khan", "DL008", "+8801688888888", "800 Driver Ave, Barisal", Decimal("25500.00"), 4),
            ("Shahid Alam", "DL009", "+8801699999999", "900 Driver Blvd, Comilla", Decimal("26500.00"), 6),
            ("Rafiq Uddin", "DL010", "+8801601111111", "101 Driver Ct, Mymensingh", Decimal("27500.00"), 8),
            ("Hafiz Rahman", "DL011", "+8801602222222", "102 Driver Rd, Jessore", Decimal("24500.00"), 3),
            ("Mizanur Islam", "DL012", "+8801603333333", "103 Driver St, Narayanganj", Decimal("28500.00"), 9),
            ("Shamsul Haque", "DL013", "+8801604444444", "104 Driver Ave, Bogra", Decimal("22000.00"), 1),
            ("Nurul Amin", "DL014", "+8801605555555", "105 Driver Way, Dinajpur", Decimal("30000.00"), 12),
            ("Gias Uddin", "DL015", "+8801606666666", "106 Driver Ln, Tangail", Decimal("23500.00"), 2),
            ("Jasim Uddin", "DL016", "+8801607777777", "107 Driver Blvd, Pabna", Decimal("26000.00"), 5),
            ("Anwar Hossain", "DL017", "+8801608888888", "108 Driver Ct, Kushtia", Decimal("27000.00"), 7),
            ("Rashed Mia", "DL018", "+8801609999999", "109 Driver Dr, Faridpur", Decimal("25000.00"), 4),
            ("Hakim Ali", "DL019", "+8801610101010", "110 Driver St, Gazipur", Decimal("24000.00"), 3),
            ("Salim Sheikh", "DL020", "+8801610202020", "111 Driver Ave, Brahmanbaria", Decimal("28000.00"), 10),
        ]

        drivers = []
        for name, license, phone, address, salary, experience in drivers_data:
            driver, created = Driver.objects.get_or_create(
                license_no=license,
                defaults={
                    'name': name,
                    'contact_number': phone,
                    'address': address,
                    'salary': salary,
                    'location': random.choice(locations),
                    'status': random.choice(['active', 'active', 'inactive']),
                    'experience_years': experience,
                    'rating': Decimal(str(random.uniform(4.0, 5.0))[:4]),
                    'total_trips': random.randint(10, 200)
                }
            )
            drivers.append(driver)
            if created:
                self.stdout.write(f"Created driver: {driver}")

        # Create 20 Driver Applications
        applications_data = [
            ("New Driver 1", "newdriver1@email.com", "DL100", "+8801777777777", "New Address 1", 2),
            ("New Driver 2", "newdriver2@email.com", "DL101", "+8801788888888", "New Address 2", 4),
            ("New Driver 3", "newdriver3@email.com", "DL102", "+8801799999999", "New Address 3", 1),
            ("New Driver 4", "newdriver4@email.com", "DL103", "+8801712345678", "New Address 4", 3),
            ("New Driver 5", "newdriver5@email.com", "DL104", "+8801723456789", "New Address 5", 5),
            ("New Driver 6", "newdriver6@email.com", "DL105", "+8801734567890", "New Address 6", 2),
            ("New Driver 7", "newdriver7@email.com", "DL106", "+8801745678901", "New Address 7", 6),
            ("New Driver 8", "newdriver8@email.com", "DL107", "+8801756789012", "New Address 8", 1),
            ("New Driver 9", "newdriver9@email.com", "DL108", "+8801767890123", "New Address 9", 4),
            ("New Driver 10", "newdriver10@email.com", "DL109", "+8801778901234", "New Address 10", 7),
            ("New Driver 11", "newdriver11@email.com", "DL110", "+8801789012345", "New Address 11", 3),
            ("New Driver 12", "newdriver12@email.com", "DL111", "+8801790123456", "New Address 12", 5),
            ("New Driver 13", "newdriver13@email.com", "DL112", "+8801701234567", "New Address 13", 2),
            ("New Driver 14", "newdriver14@email.com", "DL113", "+8801712345670", "New Address 14", 8),
            ("New Driver 15", "newdriver15@email.com", "DL114", "+8801723456701", "New Address 15", 1),
            ("New Driver 16", "newdriver16@email.com", "DL115", "+8801734567012", "New Address 16", 6),
            ("New Driver 17", "newdriver17@email.com", "DL116", "+8801745670123", "New Address 17", 2),
            ("New Driver 18", "newdriver18@email.com", "DL117", "+8801756701234", "New Address 18", 4),
            ("New Driver 19", "newdriver19@email.com", "DL118", "+8801767801234", "New Address 19", 9),
            ("New Driver 20", "newdriver20@email.com", "DL119", "+8801778912345", "New Address 20", 3),
        ]

        for name, email, license, phone, address, experience in applications_data:
            app, created = DriverApplication.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'license_no': license,
                    'contact_number': phone,
                    'address': address,
                    'experience_years': experience,
                    'location': random.choice(locations),
                    'status': random.choice(['pending', 'reviewing', 'pending'])
                }
            )
            if created:
                self.stdout.write(f"Created driver application: {app}")

        # Create Orders
        for i in range(10):
            if clients and cars:
                order, created = Order.objects.get_or_create(
                    order_id=f"BHR{str(i).zfill(8)}",
                    defaults={
                        'car': random.choice(cars),
                        'client': random.choice(clients),
                        'driver': random.choice(drivers) if random.choice([True, False]) else None,
                        'start_date': datetime.now() + timedelta(days=random.randint(1, 30)),
                        'end_date': datetime.now() + timedelta(days=random.randint(31, 60)),
                        'pickup_location': random.choice(locations),
                        'dropoff_location': random.choice(locations),
                        'total_amount': Decimal(str(random.uniform(5000, 15000))[:8]),
                        'status': random.choice(['pending', 'confirmed', 'ongoing', 'completed']),
                        'special_requirements': f"Special requirement for order {i+1}"
                    }
                )
                if created:
                    self.stdout.write(f"Created order: {order}")

        # Create Messages
        messages_data = [
            ("Customer 1", "customer1@email.com", "inquiry", "Car Availability", "I want to know about car availability."),
            ("Customer 2", "customer2@email.com", "complaint", "Service Issue", "I had an issue with my recent booking."),
            ("Customer 3", "customer3@email.com", "feedback", "Great Service", "Thank you for the excellent service!"),
        ]

        for name, email, msg_type, subject, message in messages_data:
            msg, created = Message.objects.get_or_create(
                sender_email=email,
                subject=subject,
                defaults={
                    'sender_name': name,
                    'message_type': msg_type,
                    'message': message,
                    'client': random.choice(clients) if random.choice([True, False]) else None,
                    'is_read': random.choice([True, False])
                }
            )
            if created:
                self.stdout.write(f"Created message: {msg}")

        # Create Admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@bhromon.com',
                password='admin123'
            )
            
            admin_profile, created = Admin.objects.get_or_create(
                user=admin_user,
                defaults={
                    'can_edit_salaries': True,
                    'can_manage_drivers': True,
                    'can_manage_cars': True,
                    'can_view_reports': True
                }
            )
            if created:
                self.stdout.write("Created admin user: admin/admin123")

        self.stdout.write(
            self.style.SUCCESS("Sample data created successfully!")
        )
        self.stdout.write(
            self.style.SUCCESS("You can now login as admin with username: admin, password: admin123")
        )
