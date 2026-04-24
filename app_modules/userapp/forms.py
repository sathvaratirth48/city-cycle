from django.forms.widgets import FileInput
from django import forms
from app_modules.userapp import models
from .models import CustomUser

#Login Start

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone_number',
            'address',
            'date_of_birth',
            'profile_image'
        ]

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password1')

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        
#Login End

#User Profile Start
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone_number',
            'address',
            'date_of_birth',
            'profile_image',
        ]
        widgets = {
            'profile_image': FileInput(),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image and hasattr(image, 'size'):
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Image size must be under 5MB.")
        return image


#User Profile End

#Booking Start  
class BookingForm(forms.ModelForm):
    start_time = forms.TimeField(
        input_formats=['%I:%M %p', '%H:%M'] 
    )
    end_time = forms.TimeField(
        input_formats=['%I:%M %p', '%H:%M']
    )
    booking_date = forms.DateField(
        input_formats=['%d-%m-%Y', '%Y-%m-%d']
    )
    total_hours = forms.FloatField(required=False)
    
    class Meta:
        model = models.Booking
        fields = [
        'pickup_location',
        'dropoff_location',
        'adult',
        'child',
        'start_time',
        'end_time',
        'total_hours',
        'total_amount',
        'booking_date',
        'special_requests',
        ]


# ── Cancel Booking Form ───────────────────────────────────────
class CancelBookingForm(forms.Form):
    cancel_reason = forms.ChoiceField(
        choices=models.Booking.CANCEL_REASON_CHOICES,
        widget=forms.RadioSelect(),
        label="Reason for Cancellation"
    )
    cancel_reason_other = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class':       'form-control',
            'rows':        3,
            'placeholder': 'Please describe your reason...'
        }),
        label="Other Reason"
    )

    def clean(self):
        cleaned_data = super().clean()
        reason       = cleaned_data.get('cancel_reason')
        other_reason = cleaned_data.get('cancel_reason_other')

        if reason == 'other' and not other_reason.strip():
            raise forms.ValidationError("Please describe your reason for cancellation.")
        return cleaned_data
    
#Booking End 