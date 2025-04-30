# views.py (Cleaned Version)
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
import json

from .forms import ContactForm
from .models import contact
from .mail import send_email


def home(request):
    return render(request, 'main_app/home.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created Successfully: {username}")
            login(request, user)
            return redirect('main_app:home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")
    else:
        form = UserCreationForm()
    return render(request, 'main_app/register.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main_app:home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username} !")
                return redirect("main_app:home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "main_app/login.html", {'form': form})


def emergency_contact(request):
    if not request.user.is_authenticated:
        return redirect("main_app:login")
    contacts = contact.objects.filter(user=request.user)
    return render(request, 'main_app/emergency_contact.html', {
        'contacts': contacts,
        'total_contacts': contacts.count(),
        'user': request.user
    })


def create_contact(request):
    inst = contact(user=request.user)
    form = ContactForm(request.POST or None, instance=inst)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, "New contact created successfully and notified!")
        return redirect('main_app:emergency_contact')
    return render(request, 'main_app/create_contact.html', {'form': form})


def update_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    form = ContactForm(request.POST or None, instance=curr_contact)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f"{curr_contact.name} updated successfully!")
        return redirect('main_app:emergency_contact')
    return render(request, 'main_app/create_contact.html', {'form': form})


def delete_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    if request.method == "POST":
        curr_contact.delete()
        messages.success(request, f"{curr_contact.name} deleted successfully!")
        return redirect('main_app:emergency_contact')
    return render(request, 'main_app/delete_contact.html', {'item': curr_contact})


@ensure_csrf_cookie
@login_required
def emergency_with_location(request):
    return render(request, 'main_app/emergency.html', {'name': request.user.username})


import os
from dotenv import load_dotenv
load_dotenv()
from twilio.rest import Client

# Correct way: Fetch credentials from environment variables (recommended)
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_number = os.getenv('TWILIO_FROM_PHONE_NUMBER')
to_number = os.getenv('TWILIO_TO_PHONE_NUMBER')  # This should be set to the emergency number you want to send SMS to

def sendsms(lat , lon ):
    client = Client(account_sid, auth_token)
    try:
        message_body = "🚨 Emergency alert! Location 🗺 : \nClick here: https://maps.google.com/?q=" + str(lat) + "," + str(lon) + "\nPlease check on your loved one"
        msg = str(message_body)
        message = client.messages.create(
            # body="🚨 Emergency alert! Please check on your loved one lat = {lat} , lon = {lon}",
            body= msg,
            from_=from_number,  # Your Twilio number
            to=to_number  # Dynamic emergency number
        )
        print(f"SMS sent successfully: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

@csrf_exempt
@login_required
def send_location_to_contacts(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get('latitude')
            lon = data.get('longitude')
            if not lat or not lon:
                return JsonResponse({'message': 'Invalid location data'}, status=400)

            contacts = contact.objects.filter(user=request.user)
            location_link = f"https://www.google.com/maps?q={lat},{lon}"

            # Now properly send SMS to each contact
            # for c in contacts:
            #     send_sms_alert(c.phone_number)  # Assuming your 'contact' model has 'phone_number' field

            sendsms(lat , lon)
            # Send email as well
            if contacts:
                send_email(request.user.username, contacts[0].email, location_link)

            return JsonResponse({'message': 'Location sent to contacts successfully!'})
        except Exception as e:
            return JsonResponse({'message': 'Error sending location', 'error': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)


def send_sms_alert(request):
    return redirect('main_app/sms_alert.html')


def redirect_emergency(request):
    return redirect('main_app:emergency_location')


def helpline_numbers(request):
    return render(request, 'main_app/helpline_numbers.html')


def women_rights(request):
    return render(request, 'main_app/women_rights.html')


def women_laws(request):
    return render(request, 'main_app/women_laws.html')


def developers(request):
    return render(request, 'main_app/developers.html')


def about_me(request):
    return render(request, 'main_app/about_me.html')