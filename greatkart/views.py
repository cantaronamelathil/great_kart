from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

# Create your views here.


def home(request):
    #  <h1> hai </h1>
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'greatkart/home.html', context)
