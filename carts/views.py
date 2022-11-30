# from http.client import HTTPResponse
from turtle import color
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart,Cartitem
from store.models import Product,Variation
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from coupon.models import Coupon, ReviewCoupon
from datetime import date
from .models import  wishlist
# from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# def add_cart(request, product_id):
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                    print("varation= ",variation)
                except:
                    pass


        is_cart_item_exists = Cartitem.objects.filter(product=product, user=current_user).exists()
        print(is_cart_item_exists)
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cartitem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Cartitem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
           
            cart_item = Cartitem.objects.create(product = product,quantity = 1,user = current_user)
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
                cart_item.save()
        return redirect('cart')
    # If the user is not authenticated
    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = Cartitem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.filter(product=product, cart=cart)
            # existing_variations -> database
            # current variation -> product_variation
            # item_id -> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = Cartitem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = Cartitem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = Cartitem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')


# 
def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass 
    return redirect('cart')    

def remove_cart_item(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user,is_activate=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart,is_activate=True)
        for cart_item in cart_items:
            total += (cart_item.product.offer * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        
        grand_total =  total + tax
        
        
        grand_total = total + tax
    
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': cart_items,
            'tax'       : tax,
            'grand_total': grand_total,
        }
    except ObjectDoesNotExist:
        pass #just ignore
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
   
    }
    
    # tax = 0
    # grand_total = 0
    # try:

    #     if "buy_now" in request.session:
    #         del request.session["buy_now"]

    #     if request.user.is_authenticated:
    #         cart_items = Cartitem.objects.filter(
    #             user=request.user, is_activate=True
    #         )
        # else:
        #     cart = Cart.objects.get(cart_id=_cart_id(request))
        #     cart_items = Cartitem.objects.filter(cart=cart, is_activate=True)
        # for cart_item in cart_items:
        #     if cart_item.product.Offer_Price():
        #         offer_price = Product.Offer_Price(cart_item.product)
        #         print(offer_price["new_price"])
        #         total = total + (
        #             offer_price["new_price"] * cart_item.quantity
        #         )
        #         print(total)
    #         else:
    #             total = total + (cart_item.product.price * cart_item.quantity)

    #         quantity = quantity + cart_item.quantity
    #     tax = (2 * total) / 100
    #     grand_total = total + tax
    # except ObjectDoesNotExist:
    #     pass  # just ignore

    # context = {
    #     "total": total,
    #     "quantity": quantity,
    #     "cart_items": cart_items,
    #     "tax": tax,
    #     "grand_total": grand_total,
    # }
    
    
    return render(request,'store/cart.html', context)


# def cart(request):
#     return render(request,'store/cart.html')
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = Cartitem.objects.filter(user=request.user, is_activate=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cartitem.objects.filter(cart=cart, is_activate=True)
        for cart_item in cart_items:
            total += (cart_item.product.offer * cart_item.quantity)
            quantity += cart_item.quantity
              
              
              
        tax = (2 * total)/100
          
        grand_total = total+ tax
          
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        
    }
    
    
    
    
    
    # tax = 0
    # grand_total = 0
    # try:
    #     if request.user.is_authenticated:
    #         if "buy_now" in request.session:
    #             product_id = request.session["buy_now"]
    #             item = Product.objects.get(id=product_id)
                # addresses = Address.objects.filter(user=request.user)
            # else:
                # item = False
                # cart_items = Cartitem.objects.filter(
                #     user=request.user, is_active=True
                # )
                # addresses = Address.objects.filter(user=request.user)
        # else:
        #     cart = Cart.objects.get(cart_id=_cart_id(request))
        #     cart_items = Cartitem.objects.filter(cart=cart, is_active=True)

        # if "buy_now" in request.session:
        #     product_id = request.session["buy_now"]
        #     item = Product.objects.get(id=product_id)
        #     if item.Offer_Price():
            #     offer_price = Product.Offer_Price(item)
            #     print(offer_price["new_price"])
            #     total = total + (offer_price["new_price"] * 1)
            #     print(total)
            # else:
            #     total = item.price * 1
            # quantity = 1
            # tax = (2 * total) / 100
            # grand_total = total + tax

        # else:
        #     for cart_item in cart_items:
        #         if cart_item.product.Offer_Price():
        #             offer_price = Product.Offer_Price(cart_item.product)
        #             print(offer_price["new_price"])
        #             total = total + (
        #                 offer_price["new_price"] * cart_item.quantity
        #             )
        #             print(total)
        #         else:
        #             total = total + (
        #                 cart_item.product.price * cart_item.quantity
        #             )
    #         tax = (2 * total) / 100
    #         grand_total = total + tax
    #     if "discount_price" in request.session:
    #         grand_total = request.session["discount_price"]
    # except ObjectDoesNotExist:
    #     pass  # just ignore

    # context = {
    #     "total": total,
    #     "quantity": quantity,
    #     "cart_items": cart_items,
    #     "tax": tax,
    #     "grand_total": grand_total,
    #     # "addresses": addresses,
    #     "item": item,
    # }
    
    return render(request, 'store/checkout.html', context)


@login_required(login_url="userlogin")
def Check_coupon(request):

    if "coupon_code" in request.session:
        del request.session["coupon_code"]
        del request.session["amount_pay"]
        del request.session["discount_price"]

    flag = 0
    discount_price = 0
    amount_pay = 0
    coupon_code = request.POST.get("coupon_code")
    grand_total = float(request.POST.get("grand_total"))

    if Coupon.objects.filter(code=coupon_code, coupon_limit__gte=1).exists():
        coupon = Coupon.objects.get(code=coupon_code)
        print(coupon)
        if coupon.active == True:
            flag = 1
            if not ReviewCoupon.objects.filter(
                user=request.user, coupon=coupon
            ):
                today = date.today()

                if coupon.valid_from <= today and coupon.valid_to >= today:
                    discount_price = grand_total - coupon.discount

                    print(discount_price)
                    amount_pay = grand_total - discount_price
                    print(amount_pay)
                    flag = 2
                    request.session["amount_pay"] = amount_pay
                    request.session["coupon_code"] = coupon_code
                    request.session["discount_price"] = discount_price

                    print("asfghjsftsfT333333")

    context = {
        "amount_pay": amount_pay,
        "flag": flag,
        "discount_price": discount_price,
        "coupon_code": coupon_code,
    }

    return JsonResponse(context)
def wish_list(request,id):
    flag=0
    id= request.GET["id"]
    product=Product.objects.get(id=id)
    if wishlist.objects.filter(Product=product,user=request.user).exists():
        flag=1
    else:
        wishlist.objects.create(Product=product,user=request.user)
        flag=2

    context={
        "flag":flag
    }
    return JsonResponse(context)

def viewwish_list(request):
    Wishlist = wishlist.objects.filter(user=request.user)
    context={
        'wishlist':Wishlist
    }
    return render(request,'store/wish_list.html',context)