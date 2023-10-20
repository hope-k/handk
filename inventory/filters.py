from django_filters import rest_framework as filters
from inventory import models
from django.db.models import Q, F, Count, Avg, Max, Min, Sum



class ProductFilter(filters.FilterSet):
    class Meta:
        model = models.Product
        fields = ['category', 'price', 'brand', 'rating']

    category = filters.CharFilter(
        method='filter_category_slug',
    )
    price = filters.RangeFilter(
        field_name='min_price',
        lookup_expr='range'
        )

    brand = filters.CharFilter(
        field_name='brand__name',
        method='filter_brand',
        lookup_expr='exact'
    )
    rating = filters.CharFilter(
        field_name='reviews__rating',
        method='filter_rating'
    )
    # ! ORDERING: the first value is the field name, the second is the query param
    sort = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('min_price', 'price'),
        )
    )

    def filter_rating(self, queryset, name, value):
        return queryset.filter(Q(reviews__rating=value))

    def filter_brand(self, queryset, name, value):
        brand_names = value.split(',')
        return queryset.filter(Q(brand__name__in=brand_names))

    def filter_category_slug(self, queryset, name, value):
        category = models.Category.objects.get(slug=value)
        # ? include self
        # ? because if theres no descendants,
        # ? we want to include the parent and query the parent
        descendant_slugs = category.get_descendants(
            include_self=True).values_list('slug', flat=True)
        return queryset.filter(Q(category__slug__in=descendant_slugs))
