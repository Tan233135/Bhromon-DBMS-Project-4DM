from django import forms
from .models import Car, Order, Message, Location, Client, Driver, DriverApplication, CarMaintenance

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "image",
            "car_name",
            "company_name",
            "model_year",
            "num_of_seats",
            "cost_par_day",
            "content",
            "status",
            "transmission",
            "fuel_type",
            "mileage",
            "location",
            "license_plate",
        ]
        widgets = {
            'model_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1980', 'max': '2024'}),
            'cost_par_day': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DHK-1234'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "car",
            "client",
            "driver",
            "start_date",
            "end_date",
            "pickup_location",
            "dropoff_location",
            "total_amount",
            "special_requirements",
        ]
        labels = {
            'car': 'Car Model',
            'client': 'Client',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'total_amount': 'Total Amount (Tk)',
            'special_requirements': 'Special Requirements',
        }
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'id': 'id_start_date',
                }
            ),
            'end_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'id': 'id_end_date',
                }
            ),
            'total_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'id_total_amount',
                    'step': '0.01',
                }
            ),
            'special_requirements': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            ),
        }
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "sender_name",
            "sender_email",
            "subject",
            "message_type",
            "message",
        ]
        labels = {
            'sender_name': 'Your Name',
            'sender_email': 'Your Email',
            'subject': 'Subject',
            'message_type': 'Message Type',
            'message': 'Your Message',
        }
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your message',
                'required': True
            }),
            'message_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please describe your inquiry, complaint, feedback, or support request in detail...',
                'required': True
            }),
        }
    
    def clean_sender_email(self):
        email = self.cleaned_data.get('sender_email')
        if email:
            # Basic email validation (Django handles most of this)
            if '@' not in email or '.' not in email:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.strip()) < 10:
            raise forms.ValidationError('Please provide a more detailed message (at least 10 characters).')
        return message

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'state', 'country', 'latitude', 'longitude', 'zip_code']
        widgets = {
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'date_of_birth', 'license_number', 'location'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DriverApplicationForm(forms.ModelForm):
    class Meta:
        model = DriverApplication
        fields = [
            'name', 'email', 'license_no', 'contact_number', 
            'address', 'experience_years', 'location'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class CarMaintenanceForm(forms.ModelForm):
    class Meta:
        model = CarMaintenance
        fields = [
            'car', 'maintenance_type', 'description', 'cost', 
            'maintenance_date', 'next_maintenance_date', 'performed_by'
        ]
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
