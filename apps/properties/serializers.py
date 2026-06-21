from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import Property, PropertyMedia, Lead, SavedSearch



class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PropertyMedia
        fields = ['id', 'media_type', 'file', 'is_cover', 'order']
        
        
        
class PropertySerializer(serializers.ModelSerializer):
    latitude  = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    media     = PropertyMediaSerializer(many=True, read_only=True)   
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Property
        fields = [
          'id', 'title', 'description', 'property_type', 'status','price', 'bedrooms', 'bathrooms', 'area_sqft',
            'address', 'city','latitude', 'longitude','lat', 'lng','media','is_featured', 'created_at',  
        ]
        read_only_fields = ['id', 'created_at']
        
    def get_latitude(self, obj):
        return obj.location.y if obj.location else None
    
    def get_longitude(self, obj):
        return obj.location.x if obj.location else None
    
    def create(self, validated_data):
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)
        if lat and lng:
            validated_data['location'] = Point(lng, lat, srid=4326)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        lat = validated_data.pop('lat', None)
        lng = validated_data.pop('lng', None)
        if lat and lng:
            validated_data['location'] = Point(lng, lat, srid=4326)
        return super().update(instance, validated_data)
    

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Lead
        fields = ['id', 'property', 'name', 'email', 'phone', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
        
        

class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedSearch
        fields = ['id','name','city','price_min','price_max','bedrooms','is_active','created_at']
        read_only_fields = ['id','created_at']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    
    