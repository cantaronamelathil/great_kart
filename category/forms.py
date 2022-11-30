from django.db.models import fields
from django.forms import ModelForm
from .models import category

class CategoryForm(ModelForm):
    class Meta:
        model = category
        fields = ["category_name", "slug", "cat_image"]