import random
import os
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from django.shortcuts import render,redirect
from django.utils.timezone import now

from app_modules.adminapp.views import list_city

from app_modules.userapp import forms
from app_modules.adminapp.models import Vehicle
from app_modules.userapp import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import ProfileForm, RegisterForm
from app_modules.adminapp import models as admin_models
# Create your views here.     

def home_page(request):
    vehicles = Vehicle.objects.all()[:6]  
    context = {'vehicles': vehicles}
    return render(request, 'userapp/index.html', context)

def about_page(request):
    return render(request,'userapp/about.html')

#Booking Start  

# ── Booking ──────────────────────────────────────────────────────────────────
@login_required
def booking_page(request, id):
    vehicle = Vehicle.objects.get(id=id)
    rental_locations = admin_models.RentalLocation.objects.all()

    if request.method == 'POST':
        form = forms.BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.vehicle = vehicle
            booking.user = request.user
            booking.booking_status = "Pending"
            # total_hours POST se manually lo (JS calculate karta hai)
            booking.total_hours = int(float(form.cleaned_data.get('total_hours') or 0))
            booking.save()
            messages.success(request, "Booking created successfully!")
            return redirect('list_Booking_user')
        else:
            messages.error(request, "Please fix the errors below.")
            print(form.errors)  # ← terminal mein exact error dekho
    else:
        form = forms.BookingForm()

    return render(request, 'userapp/booking.html', {
        'form': form,
        'vehicle': vehicle,
        'rental_locations': rental_locations,
    })

# ── List Bookings ───────────────────────────────────────────────────────────── 
    
@login_required 
def list_Booking_user(request):
    """User: all bookings"""
    booking = models.Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'userapp/list_Booking_user.html', {'booking': booking})


# ── Update Booking For User ────────────────────────────────────────────────────────────

def update_Booking(request, id):
    booking1 = get_object_or_404(models.Booking, id=id)
    vehicles = Vehicle.objects.all()
    rental_locations = admin_models.RentalLocation.objects.all()
    status_choices = models.Booking.BOOKING_STATUS_CHOICES

    # ✅ POST pe priority
    next_url = request.POST.get('next') or request.GET.get('next') or 'list_Booking_user'

    if request.method == 'POST':
        form = forms.BookingForm(request.POST, instance=booking1)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = booking1.user
            booking.total_hours = int(float(form.cleaned_data.get('total_hours') or 0))
            booking.total_amount = booking1.total_amount 
            booking.vehicle = booking1.vehicle  
            booking.save()
            messages.success(request, f"Booking #{id} updated successfully!")
            return redirect(next_url)   # ✅ ab correct redirect
        else:
            messages.error(request, "Please fix the errors below.")
            print(form.errors)  # 👈 debug ke liye

    else:
        form = forms.BookingForm(instance=booking1)

    return render(request, 'userapp/update_Booking.html', {
        'form': form,
        'booking1': booking1,
        'vehicles': vehicles,
        'rental_locations': rental_locations,
        'status_choices': status_choices,
        'next': next_url,
    })


# ── Delete Booking ──────────────────────────────────────────────────────────── 

def delete_booking(request, id):
    booking = get_object_or_404(models.Booking, id=id)
    booking.delete()
    messages.success(request, f"Booking #{id} deleted successfully!")
    return redirect('list_Booking_user')


# ── Cancel Booking (Rapido Style) ─────────────────────────────────────────────

def cancel_booking(request, id):
    booking = get_object_or_404(models.Booking, id=id)

    # ── Block if not cancellable ─────────────────────────────────────
    if not booking.can_cancel():
        messages.error(
            request,
            f"Booking #{id} cannot be cancelled. "
            f"Current status: {booking.booking_status}"
        )
        return redirect('list_Booking_user')

    form = forms.CancelBookingForm()

    if request.method == 'POST':
        form = forms.CancelBookingForm(request.POST)
        if form.is_valid():
            reason       = form.cleaned_data['cancel_reason']
            other_reason = form.cleaned_data.get('cancel_reason_other', '')
            refund       = booking.get_refund_amount()   # calculate BEFORE status change

            # ── Apply cancellation ───────────────────────────────────
            booking.booking_status      = 'Cancelled'
            booking.cancel_reason       = reason
            booking.cancel_reason_other = other_reason if reason == 'other' else ''
            booking.cancelled_at        = timezone.now()
            booking.refund_amount       = refund
            booking.refund_status       = 'Pending' if refund > 0 else 'None'
            booking.save()

            if refund > 0:
                messages.success(
                    request,
                    f"Booking #{id} cancelled. "
                    f"₹{refund} refund will be processed shortly."
                )
            else:
                messages.success(
                    request,
                    f"Booking #{id} cancelled. No refund applicable."
                )
            return redirect('list_Booking_user')

    context = {
        'booking':        booking,
        'form':           form,
        'refund_preview': booking.get_refund_amount(),
    }
    return render(request, 'userapp/cancel_booking.html', context)



#Booking End      

def car_page(request):
    vehicles = Vehicle.objects.all()
    context = {'vehicles': vehicles}
    return render(request, 'userapp/car.html', context)


def contact_page(request):
    return render(request,'userapp/contact.html')

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    related_vehicles = Vehicle.objects.filter(
        category=vehicle.category
    ).exclude(id=vehicle.id)[:4]
    
    context = {
        'vehicle': vehicle,
        'related_vehicles': related_vehicles,
    }
    return render(request, 'userapp/vehicle_detail.html', context)

def service_page(request):
    return render(request,'userapp/service.html')

def why_choose_page(request):
    return render(request,'userapp/why_choose.html')

def testimonial_page(request):
    return render(request,'userapp/testimonial.html')


#Login Start

User = get_user_model()

# ================= REGISTER =================

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'User'
            user.is_approved = False
            user.save()

            messages.success(request, "Registration successful! Wait for admin approval.")
            return redirect('user_login')
        else:
            messages.error(request, "Please correct the errors below!")

    else:
        form = RegisterForm()

    return render(request, 'userapp/register.html', {'form': form})


# ================= LOGIN =================  
def login_view(request):
    if request.user.is_authenticated:
        logout(request)   # old user remove first

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.role == 'Admin':
                login(request, user)
                return redirect('index')

            elif user.role == 'User' and user.is_approved:
                login(request, user)
                return redirect('home_page')

            else:
                messages.warning(request, "Wait for admin approval!")

        else:
            messages.error(request, "Invalid Username or Password!")

    return render(request, 'userapp/login.html')

# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    request.session.flush()   # old session clear
    messages.info(request, "Logged out successfully!")
    return redirect('user_login')   # correct login page

# ================= ADMIN DASHBOARD =================
@login_required
def admin_dashboard(request):
    if request.user.role != 'Admin':
        messages.error(request, "Unauthorized access!")
        return redirect('login')

    all_users = User.objects.exclude(role='Admin')
    approved_users = User.objects.filter(is_approved=True, role='User')
    rejected_users = User.objects.filter(is_approved=False, role='User')

    return render(request, 'userapp/dashboard_admin.html', {
        'all_users': all_users,
        'approved_users': approved_users,
        'rejected_users': rejected_users,
    })


# ================= USER DASHBOARD =================
@login_required
def user_dashboard(request):
    return render(request, 'userapp/dashboard_user.html')


# ================= APPROVE USER =================
@login_required
def approve_user(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, "Unauthorized action!")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if user.role == 'Admin':
        messages.warning(request, "Cannot approve Admin!")
        return redirect('admin_dashboard')

    user.is_approved = True
    user.save()

    messages.success(request, f"{user.username} approved!")
    return redirect('admin_dashboard')


# ================= REJECT USER =================
@login_required
def reject_user(request, user_id):
    if request.user.role != 'Admin':
        messages.error(request, "Unauthorized action!")
        return redirect('login')

    user = get_object_or_404(User, id=user_id)

    if user.role == 'Admin':
        messages.warning(request, "Cannot reject Admin!")
        return redirect('admin_dashboard')

    user.is_approved = False
    user.save()

    messages.error(request, f"{user.username} rejected!")
    return redirect('admin_dashboard')

# Login End 


# User Profile Start  

# ================= VIEW PROFILE =================
@login_required
def profile_view(request):
    return render(request, 'userapp/profile.html', {'user': request.user})


# ================= EDIT PROFILE =================
User = get_user_model()

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Use User instead of CustomUser
            old_image = User.objects.get(pk=request.user.pk).profile_image
            new_image = form.cleaned_data.get('profile_image')

            if new_image and old_image and old_image != new_image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'userapp/profile.html', {'form': form, 'edit_mode': True})


# ================= DELETE PROFILE IMAGE =================
@login_required
def delete_profile_image(request):
    if request.method == 'POST':
        user = request.user
        if user.profile_image:
            # Delete file from disk
            image_path = user.profile_image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
            # Clear from DB
            user.profile_image = None
            user.save(update_fields=['profile_image'])
            messages.success(request, "Profile photo removed.")
        else:
            messages.info(request, "No profile image to remove.")
    return redirect('profile_edit')

# User Profile End

# ── Start Booking (Random Vehicle) ─────────────────────────────────────────────
def start_booking(request):
    vehicles = Vehicle.objects.all()

    if vehicles.exists():
        vehicle = random.choice(vehicles)  # ya .first()
        return redirect('booking_page', id=vehicle.id)
    else:
        return redirect('home')  # agar koi vehicle nahi hai
