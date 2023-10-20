from rest_framework import serializers
from inventory import models


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = '__all__'

    def save(self, **kwargs):
        try:
            user_pk = self.context['user_pk']
            product_slug = self.context['product_slug']
            review = models.Review.objects.get(user=user_pk, product__slug=product_slug)
            review.comment = self.validated_data['comment']
            self.instance = review.save()

        except models.Review.DoesNotExist:
            self.instance = models.Review.objects.create(**self.validated_data)
        return self.instance
