# from unicodedata import category
# from http.client import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Product
from category.models import Category
from django.core.paginator import Paginator
from carts.views import _cart_id
# from django.http import HttpResponse
from carts.models import Cartitem,wishlist

from django.http import HttpResponse,JsonResponse
# Create your views here.
from django.db.models import Q
from django.contrib import messages

def store(request, category_slug=None):
    print(1)
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)

        in_cart = Cartitem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product).exists()

        # return HttpResponse(in_cart)

        # exit()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            #   products = Product.objects.order_by('-created_date').filter(Q(description_icontions=keyword|Q(product_name__icontains=))
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            print(products)
            context = {
                'products': products,
                'product_count': product_count,
            }
    #  return render(request, 'store/store.html', context)
    return render(request, 'store/store.html',context)



def wishlists(request):
    id = request.GET['id']
    
    
    if wishlist.objects.filter(user=request.user).filter(Product_id = id).exists():
        flag = 1
    else:
        flag = 0
        wishlist.objects.create(user = request.user,Product_id = id).save()

    return JsonResponse({'flag':flag})



def buy_now(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        request.session["buy_now"] = product.id
        return redirect("checkout")

    else:
        messages.error(request, "Login Required!")
        return redirect("store")