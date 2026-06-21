from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('plot', 'Plot'),
        ('commercial', 'Commercial'),
    ]
    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('for_rent', 'For Rent'),
        ('sold', 'Sold'),
    ]
    title         = models.CharField(max_length=200)
    description   = models.TextField(blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='house')
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale')
    price         = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms      = models.IntegerField(default=0)
    bathrooms     = models.IntegerField(default=0)
    area_sqft     = models.FloatField()
    address       = models.CharField(max_length=300)
    city          = models.CharField(max_length=100)
    location      = models.PointField(geography=True, null=True, blank=True)
    agent         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='properties')
    is_featured   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.city}"
    
   
class PropertyMedia(models.Model):

    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    property    = models.ForeignKey(
                    Property,
                    on_delete=models.CASCADE,
                    related_name='media'
                  )
    media_type  = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    file        = models.FileField(upload_to='properties/media/')
    is_cover    = models.BooleanField(default=False)
    order       = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"{self.property.title} - {self.media_type}"
    
    
     
     
class AgentProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    phone         = models.CharField(max_length=20)
    agency_name   = models.CharField(max_length=200, blank=True)
    bio           = models.TextField(blank=True)
    photo         = models.ImageField(upload_to='agents/photos/', null=True, blank=True)
    is_verified   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Agent"


class Lead(models.Model):

    STATUS_CHOICES = [
        ('new',         'New'),
        ('contacted',   'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed',      'Closed'),
    ]

    property      = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leads')
    agent         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    name          = models.CharField(max_length=100)
    email         = models.EmailField()
    phone         = models.CharField(max_length=20)
    message       = models.TextField(blank=True)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.property.title}"
    
    
class SavedSearch(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name        = models.CharField(max_length=100)
    city        = models.CharField(max_length=100, blank=True)
    price_min   = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_max   = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bedrooms    = models.IntegerField(null=True, blank=True)
    is_active   = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now_add=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    
    