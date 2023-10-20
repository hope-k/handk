from . import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple


class ProductInventoryModelForm(forms.ModelForm):
    attribute_values = forms.ModelMultipleChoiceField(
        queryset=models.ProductAttributeValue.objects.all(),
        widget=FilteredSelectMultiple('Inventory Features', False),
        required=True
    )

    class Meta:
        model = models.ProductInventory
        fields = '__all__'


class ProductModelForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=models.ProductFeature.objects.all(),
        widget=FilteredSelectMultiple('Product Features', False),
        required=False
    )
