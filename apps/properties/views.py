from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from .models import Property, Lead, SavedSearch
from .serializers import PropertySerializer, LeadSerializer, SavedSearchSerializer
from .documents import PropertyDocument
from elasticsearch_dsl import Q as ESQ
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title','city', 'address']
    ordering_fields = ['price', 'created_at', 'area_sqft']
    
    def get_queryset(self):
        qs = Property.objects.all()

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        bedrooms  = self.request.query_params.get('bedrooms')
        city      = self.request.query_params.get('city')

        if price_min:
            qs = qs.filter(price__gte=price_min)
        if price_max:
            qs = qs.filter(price__lte=price_max)
        if bedrooms:
            qs = qs.filter(bedrooms=bedrooms)
        if city:
            qs = qs.filter(city__icontains=city)

        return qs

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat    = request.query_params.get('lat')
        lng    = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 5))

        if not lat or not lng:
            return Response({'error': 'lat aur lng dono do'}, status=400)

        point = Point(float(lng), float(lat), srid=4326)
        props = Property.objects.filter(
            location__distance_lte=(point, D(km=radius))
        ).annotate(
            distance=Distance('location', point)
        ).order_by('distance')

        return Response(PropertySerializer(props, many=True).data)
    
    

    @action(detail=False, methods=['get'])
    def in_bounds(self, request):
    
        north = request.query_params.get('north')
        south = request.query_params.get('south')
        east  = request.query_params.get('east')
        west  = request.query_params.get('west')

        if not all([north, south, east, west]):
            return Response(
                {'error': 'north, south, east, west — yeh chaaron parameters zaroori hain'},
                status=400
            )

        from django.contrib.gis.geos import Polygon

        bbox = Polygon.from_bbox((
            float(west),    # min longitude
            float(south),   # min latitude
            float(east),    # max longitude
            float(north),   # max latitude
        ))
        bbox.srid = 4326

        properties = Property.objects.filter(location__within=bbox)

        return Response(PropertySerializer(properties, many=True).data)
    
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        city = request.query_params.get('city')
        price_min = request.query_params.get('price_min')
        price_max = request.query_params.get('price_max')
        bedrooms = request.query_params.get('bedrooms')

        search = PropertyDocument.search()

        if query:
            search = search.query(
                ESQ('multi_match', query=query, fields=['title', 'description', 'city', 'address'])
            )

        if city:
            search = search.filter('match', city=city)

        if bedrooms:
            search = search.filter('term', bedrooms=int(bedrooms))

        if price_min or price_max:
            price_range = {}
            if price_min:
                price_range['gte'] = float(price_min)
            if price_max:
                price_range['lte'] = float(price_max)
            search = search.filter('range', price=price_range)
        
        search.aggs.bucket('by_city', 'terms', field='city.keyword', size=10)
        search.aggs.bucket('by_property_type', 'terms', field='property_type', size=10)
        search.aggs.bucket('by_bedrooms', 'terms', field='bedrooms', size=10)
        
        response = search.execute()

        results = []
        for hit in response:
            results.append({
                'id': hit.meta.id,
                'title': hit.title,
                'price': hit.price,
                'city': hit.city,
                'bedrooms': hit.bedrooms,
                'area_sqft': hit.area_sqft,
            })
        facets = {
            'cities': [
                {'name': bucket.key, 'count': bucket.doc_count}
                for bucket in response.aggregations.by_city.buckets
            ],
            'property_types': [
                {'name': bucket.key, 'count': bucket.doc_count}
                for bucket in response.aggregations.by_property_type.buckets
            ],
            'bedrooms': [
                {'name': bucket.key, 'count': bucket.doc_count}
                for bucket in response.aggregations.by_bedrooms.buckets
            ],
        }
        
        return Response({
            'count': response.hits.total.value,
            'results': results,
            'facets': facets,
        })
        


class LeadViewSet(viewsets.ModelViewSet):
    queryset         = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_queryset(self):
        # Agent sirf apne property ke leads dekhe
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return Lead.objects.filter(property__agent=self.request.user)
        return Lead.objects.all()
    
    

class SavedSearchViewSet(viewsets.ModelViewSet):
    serializer_class = SavedSearchSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedSearch.objects.filter(user=self.request.user)
    
    
    