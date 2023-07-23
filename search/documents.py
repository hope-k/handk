from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from inventory import models


@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.ObjectField(
        properties={
            'name': fields.TextField(),
        }
    )

    class Index:
        name = 'productinventory'

    class Django:
        model = models.ProductInventory

        fields = [
            'id',
            'sku',
            'store_price',
            'is_default',

        ]
