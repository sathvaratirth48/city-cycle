from django.db import models

# Create your models here.

# City  
class City(models.Model):
    city_name = models.CharField(max_length=255)
    created_at = models.DateField()
    city_image = models.ImageField(upload_to='city_image/',null=True,blank=True)
    
#Vehicle Type
class Vehicle_type(models.Model):
    type_name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    
#Category 
class Category(models.Model):
    Vehicle_type = models.ForeignKey(Vehicle_type, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField()
    
#Vehicle 
class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=255)
    vehicle_type = models.ForeignKey(Vehicle_type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price_per_hour =models.IntegerField()
    description = models.TextField()
    is_available = models.CharField(max_length=255)
    created_at = models.DateField()
    vehicle_img = models.ImageField(upload_to='vehicle_image/',null=True,blank=True)


#Rental Location
class RentalLocation(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateField()