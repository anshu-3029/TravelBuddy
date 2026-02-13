from urllib import request
from django.contrib import messages
from django.shortcuts import render

from main.forms import PackageForm
from .models import Package

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import ContactMessage

from .models import Booking
from .forms import BookingForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from datetime import date

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def packages(request):
    packages = Package.objects.all()
    return render(request, 'packages.html', {'packages': packages})

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "admin/admin_login.html")


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    packages = Package.objects.all()
    bookings = Booking.objects.all().order_by("-booked_at")
    messages_list = ContactMessage.objects.all().order_by("-created_at")

    return render(request, "admin/admin_dashboard.html", {
        "packages": packages,
        "bookings": bookings,
        "messages_list": messages_list
    })


@login_required
def admin_add_package(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    form = PackageForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Package added successfully!")
        return redirect('admin_dashboard')
    
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control form-control-lg' 
        
    return render(request, 'admin/package_form.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered! Please login.")
            return redirect('login')

        else:
            messages.error(request, "Registration failed. Please correct the errors below.")

    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not registered.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid password.")
            return redirect('login')

    form = AuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def book_now(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        travel_date_str = request.POST.get("travel_date")
        persons = request.POST.get("persons")

        # Date validation
        try:
            travel_date = datetime.strptime(travel_date_str, "%Y-%m-%d").date()
        except:
            messages.error(request, "Invalid date.")
            return render(request, "book_now.html", {"package": package})

        if travel_date <= date.today():
            messages.error(request, "Travel date must be in the future.")
            return render(request, "book_now.html", {"package": package})

        # ✅ SAVE TO DATABASE
        Booking.objects.create(
            user=request.user,
            package=package,
            full_name=full_name,
            email=email,
            phone=phone,
            travel_date=travel_date,
            persons=persons
        )

        messages.success(request, "Booking successful!")
        return redirect("home")

    return render(request, "book_now.html", {"package": package})

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )

        messages.success(request, "Message sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")

def admin_logout(request):
    logout(request)
    return redirect('admin_login')