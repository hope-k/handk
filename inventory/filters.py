from django_filters import rest_framework as filters
from inventory import models
from django.db.models import Q, F, Count, Avg, Max, Min, Sum


# class ProductInventoryFilter(filters.FilterSet):
#     is_default = filters.BooleanFilter(
#         field_name='is_default', lookup_expr='exact')
#     product_slug = filters.CharFilter(
#         field_name='product__slug', lookup_expr='exact')
#     category_slug = filters.CharFilter(
#         field_name='product__category__slug')
#     price = filters.RangeFilter(field_name='store_price', lookup_expr='range')

#     class Meta:
#         model = models.ProductInventory
#         fields = ['is_default', 'product_slug', 'category_slug', 'store_price']


class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(
        method='filter_category_slug',
    )
    price = filters.RangeFilter(
        field_name='inventories__store_price', lookup_expr='range')
    brand = filters.CharFilter(
        field_name='brand__name',
        method='filter_brand',
        lookup_expr='exact'
    )
    # ! ORDERING: the first value is the field name, the second is the query param
    o = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('inventories__sale_price', 'sale_price'),
        )
    )

    def filter_brand(self, queryset, name, value):
        brand_names = value.split(',')
        return queryset.filter(Q(inventories__brand__name__in=brand_names))

    def filter_category_slug(self, queryset, name, value):
        category = models.Category.objects.get(slug=value)
        # ? include self
        # ? because if theres no descendants,
        # ? we want to include the parent and query the parent
        descendant_slugs = category.get_descendants(
            include_self=True).values_list('slug', flat=True)
        return queryset.filter(Q(category__slug__in=descendant_slugs))

    class Meta:
        model = models.Product
        fields = ['category', 'price', 'brand']
