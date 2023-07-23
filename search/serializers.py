from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from inventory.serializers.product_serializer import ProductSerializer
from search.documents import ProductInventoryDocument


class ProductInventoryDocumentSerializer(DocumentSerializer):
    product = ProductSerializer()

    class Meta:
        document = ProductInventoryDocument
        fields = (
            'id',
            'product',
            'sku',
            'store_price',
            'is_default',
        )
