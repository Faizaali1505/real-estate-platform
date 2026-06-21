from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Property


@registry.register_document
class PropertyDocument(Document):

    city = fields.TextField(
        fields={'keyword': fields.KeywordField()}
    )
    property_type = fields.KeywordField()   # ← yeh add karo

    class Index:
        name = 'properties'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Property
        fields = [
            'title',
            'description',
            'status',
            'price',
            'bedrooms',
            'bathrooms',
            'area_sqft',
            'address',
            'is_featured',
            'created_at',
        ]