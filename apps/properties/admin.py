from django.contrib.gis import admin
from .models import Property, PropertyMedia, AgentProfile, Lead, SavedSearch

# Register your models here.
class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1
    
    
@admin.register(Property)
class PropertyAdmin(admin.GISModelAdmin):
    list_display = ['title', 'city', 'price', 'bedrooms', 'status']
    list_filter = ['status', 'property_type', 'city']
    search_fields = ['title', 'city', 'address']
    inlines = [PropertyMediaInline]
    
    
@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'agency_name', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['user__username', 'agency_name']
    
    
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'property', 'phone', 'status', 'created_at']
    list_filter = ['status','created_at']
    search_fields = ['name', 'email', 'phone']
    

@admin.register(SavedSearch)
class SavedSearchAdmin(admin.ModelAdmin):
    list_display = ['name','user','city','bedrooms','is_active']
    list_filter = ['is_active','city']
    search_fields = ['name','user__username']
    
    