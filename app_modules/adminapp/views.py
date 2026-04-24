from django.shortcuts import render,redirect
from app_modules.adminapp import forms
from app_modules.adminapp import models
from app_modules.adminapp.models import Vehicle

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from app_modules.userapp.models import Booking



# Create your views here.

def index(request):
    return render(request, 'adminapp/index.html')

def analytics(request):
    return render(request, 'adminapp/analytics.html')

#Login Start

def auth_reset_creative(request):
    return render(request, 'adminapp/auth-reset-creative.html')

def auth_resetting_creative(request):
    return render(request, 'adminapp/auth-resetting-creative.html')



def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        role = request.POST.get('role')

        if password != password1:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists! Try another.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, role=role)

        if role == "Admin":
            user.is_approved = True
        else:
            user.is_approved = False

        user.save()
        messages.success(request, "Registration successful! Wait for admin approval before login.")
        return redirect('login')
    return render(request, 'adminapp/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'Admin' or user.is_approved:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                if user.role == 'Admin':
                    return redirect('admin_dashboard')
                elif user.role == 'Parent':
                    return redirect('parent_dashboard')
                else:
                    return redirect('index')
            else:
                messages.warning(request, "Your account is not yet approved by admin.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'adminapp/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')


@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')

    all_users = User.objects.exclude(role='Admin')
    approved_users = User.objects.filter(is_approved=True, role__in=['Parent', 'User'])
    rejected_users = User.objects.filter(is_approved=False, role__in=['Parent', 'User'])

    return render(request, 'adminapp/dashboard_admin.html', {
        'all_users': all_users,
        'approved_users': approved_users,
        'rejected_users': rejected_users,
    })


def parent_dashboard(request):
    return render(request, 'adminapp/dashboard_parent.html')

def user_dashboard(request):
    return render(request, 'adminapp/dashboard_user.html')

User = get_user_model()

@login_required
def approve_user(request, user_id):    
    if request.user.role != 'Admin':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('login')
    user = get_object_or_404(User, id=user_id)

    if user.role == 'Admin':
        messages.warning(request, "You cannot approve another Admin account.")
        return redirect('admin_dashboard')

    user.is_approved = True
    user.save()
    messages.success(request, f"{user.username} has been approved successfully!")
    return redirect('admin_dashboard')


@login_required
def reject_user(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if user.role == 'Admin':
        messages.warning(request, "You cannot reject another Admin account.")
        return redirect('admin_dashboard')

    user.is_approved = False
    user.save()
    messages.error(request, f"{user.username} has been rejected.")
    return redirect('admin_dashboard')

#Login End

#City Start 
def create_City(request):
    if request.method == 'POST':
        form = forms.city_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_city)
        else:
            print(form.errors)
    return render(request, 'adminapp/create_City.html') 

def list_city(request):
    city = models.City.objects.all()
    context = {'city':city}
    return render(request, 'adminapp/list_city.html',context) 

def delete_city(request,id):
    cit1 = models.City.objects.get(id=id)
    cit1.delete()
    return redirect(list_city)

def update_City(request,id):
    cit2 = models.City.objects.get(id=id)
    if request.method == 'POST':
        form = forms.city_form(request.POST, request.FILES, instance=cit2)
        if form.is_valid():
            form.save()
            return redirect(list_city)
        else:
            print(form.errors)
    context = {'cit2': cit2}
    return render(request,'adminapp/update_City.html',context)

#City End   


#vehicle Type Start
def create_Vehicletype(request):
    if request.method == 'POST':
        form = forms.vehicletype_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_vehicletype)
        else:
            print(form.errors)
    return render(request, 'adminapp/create_Vehicletype.html') 

def list_vehicletype(request):
    vehitype = models.Vehicle_type.objects.all()
    context = {'vehitype':vehitype}
    return render(request, 'adminapp/list_vehicletype.html',context) 

def delete_vehicletype(request,id):
    vehicletype1 = models.Vehicle_type.objects.get(id=id)
    vehicletype1.delete()
    return redirect(list_vehicletype)

def update_Vehicletype(request,id):
    vehicletype2 = models.Vehicle_type.objects.get(id=id)
    if request.method == 'POST':
        form = forms.vehicletype_form(request.POST, request.FILES, instance=vehicletype2)
        if form.is_valid():
            form.save()
            return redirect(list_vehicletype)
        else:
            print(form.errors)
    context = {'vehicletype2': vehicletype2}
    return render(request,'adminapp/update_Vehicletype.html',context)

#vehicle Type End 


#Category Start
def create_Category(request):
    vtype = models.Vehicle_type.objects.all() 
    if request.method == 'POST':
        form = forms.category_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_category)
        else:
            print(form.errors)
    context = {'vtype': vtype} 
    return render(request, 'adminapp/create_Category.html', context)

def list_category(request):
    category = models.Category.objects.all()
    context = {'category':category}
    return render(request, 'adminapp/list_category.html',context)

def delete_category(request,id):
    cate = models.Category.objects.get(id=id)
    cate.delete()
    return redirect(list_category)

def update_Category(request,id):
    categ = models.Category.objects.get(id=id)
    vtype = models.Vehicle_type.objects.all()
    if request.method == 'POST':
        form = forms.category_form(request.POST, request.FILES, instance=categ)
        if form.is_valid():
            form.save()
            return redirect(list_category)
        else:
            print(form.errors)
    context = {'categ':categ, 'vtype': vtype}
    return render(request,'adminapp/update_Category.html',context)

#Category End 

#Vehicle Start    
def create_Vehicle(request):
    vtype = models.Vehicle_type.objects.all() 
    cat = models.Category.objects.all()         
    city = models.City.objects.all()
    vehicles = models.Vehicle.objects.all()        
    if request.method == 'POST':
        form = forms.vehicle_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_vehicle)
        else:
            print(form.errors)
    context = {'vtype': vtype, 'cat': cat, 'city': city, 'vehicles': vehicles}
    return render(request, 'adminapp/create_Vehicle.html', context)

def list_vehicle(request):
    vehicle = models.Vehicle.objects.all()
    context = {'vehicle': vehicle}
    return render(request, 'adminapp/list_vehicle.html', context)

def delete_vehicle(request,id):
    vehi = models.Vehicle.objects.get(id=id) 
    vehi.delete()
    return redirect(list_vehicle)

def update_Vehicle(request,id):
    vehi1 = models.Vehicle.objects.get(id=id)
    vtype = models.Vehicle_type.objects.all()
    cat = models.Category.objects.all()
    city = models.City.objects.all()
    if request.method == 'POST':
        form = forms.vehicle_form(request.POST, request.FILES, instance=vehi1)
        if form.is_valid():
            form.save()
            return redirect(list_vehicle)
        else:
            print(form.errors)
    context = {'vehi1': vehi1, 'vtype': vtype, 'cat': cat,'city': city}
    return render(request,'adminapp/update_Vehicle.html',context)

#Vehicle End     

# Rental Location Start 
def create_RentalLocation(request):
    city = models.City.objects.all() 
    if request.method == 'POST':
        form = forms.rentallocation_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(list_rentallocation)
        else:
            print(form.errors)
    context = {'city': city}
    return render(request, 'adminapp/create_RentalLocation.html', context)

def list_rentallocation(request):
    rentallocation = models.RentalLocation.objects.all()
    context = {'rentallocation': rentallocation}
    return render(request, 'adminapp/list_rentallocation.html', context)

def delete_rentallocation(request,id):
    rentallo = models.RentalLocation.objects.get(id=id)
    rentallo.delete()
    return redirect(list_rentallocation)

def update_RentalLocation(request,id):
    rentallo1 = models.RentalLocation.objects.get(id=id)
    city = models.City.objects.all() 
    if request.method == 'POST':
        form = forms.rentallocation_form(request.POST, request.FILES, instance=rentallo1)
        if form.is_valid():
            form.save()
            return redirect(list_rentallocation)
        else:
            print(form.errors)
    context = {'rentallo1': rentallo1, 'city': city}
    return render(request,'adminapp/update_RentalLocation.html',context)

# Rental Location End 

#List Bookings For Admin

@login_required
def list_Booking(request):
    if request.user.role != 'Admin':
        return redirect('login')

    booking = Booking.objects.all().order_by('-booking_date')  # ✅ models.Booking → Booking
    return render(request, 'adminapp/list_Booking.html', {'booking': booking})

# ── Accept  Booking ─────────────────────────────────────────────
def accept_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.booking_status = 'Confirmed'
    booking.save()
    return redirect('admin_list_booking')

# ── Reject  Booking ─────────────────────────────────────────────
def reject_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.booking_status = 'Cancelled'
    booking.save()
    return redirect('admin_list_booking')
