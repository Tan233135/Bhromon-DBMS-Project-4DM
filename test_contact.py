#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental_app.settings')
django.setup()

from system.forms import MessageForm
from system.models import Message
from django.test import Client

def test_contact_form():
    print("Testing Contact Form...")
    
    # Test 1: Form creation
    form = MessageForm()
    print("✓ Form creation successful")
    
    # Test 2: Form validation with valid data
    form_data = {
        'sender_name': 'Test User',
        'sender_email': 'test@example.com',
        'subject': 'Test Subject',
        'message_type': 'inquiry',
        'message': 'This is a test message with more than 10 characters.'
    }
    form = MessageForm(form_data)
    if form.is_valid():
        print("✓ Form validation successful")
        
        # Test 3: Save message
        try:
            message = form.save()
            print(f"✓ Message saved successfully with ID: {message.id}")
        except Exception as e:
            print(f"✗ Error saving message: {e}")
    else:
        print("✗ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  - {field}: {errors}")
    
    # Test 4: Check total messages
    total_messages = Message.objects.count()
    print(f"✓ Total messages in database: {total_messages}")
    
    # Test 5: Test contact page view
    client = Client()
    try:
        response = client.get('/car/contact/')
        print(f"✓ Contact page accessible - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ Contact page loads successfully")
        else:
            print(f"✗ Contact page returned status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error accessing contact page: {e}")

if __name__ == "__main__":
    test_contact_form()
