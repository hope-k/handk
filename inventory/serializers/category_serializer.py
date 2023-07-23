from rest_framework import serializers
from inventory import models


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = [
            'id',
            'name',
            'slug',
            'is_active',
            'children'
        ]
        depth = 1

    def get_children(self, obj):
        children = obj.get_children()
        serializer = CategorySerializer(children, many=True)
        return serializer.data
