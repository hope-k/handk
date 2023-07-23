from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf import filter_backends
from search.documents import ProductInventoryDocument
from search.serializers import ProductInventoryDocumentSerializer


class ProductInventoryDocumentViewSet(DocumentViewSet):
    document = ProductInventoryDocument
    serializer_class = ProductInventoryDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        filter_backends.CompoundSearchFilterBackend,
    ]
    search_fields = (
        'product.name', 'sku', 'store_price', 'is_default',
    )
