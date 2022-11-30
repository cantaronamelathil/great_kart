from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import  auth
from django.contrib.auth import authenticate

from django.http import  HttpResponse
from accounts.models import Accounts
from  store. models import Product,Variation
from  category. models import Category
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm,CategoryForm
from orders.models import Order,Payment,OrderProduct
from django.db.models import Q
from store.forms import   VarientForm
from .forms import EditVarient,EditCoupon,EditProductOffer
from coupon.models import Coupon
from datetime import date
from django.utils import timezone
import datetime
from django.db.models import Sum  
from coupon.forms import CouponForm
# from offer.forms import  ProductOfferForm
# from offer.models import ProductOffer
# from store. forms import  ProductForm
# Create your views here.
# @login_required(login_url='adminlogin')

def check_admin(user):
    return user.is_admin

def dashboard(request):
    New=0
    Accepted=0
    Completed=0
    Cancelled=0
    products=Product.objects.all().count()
    users=Accounts.objects.all().count()
    sales=OrderProduct.objects.all().count()
    revenue= Payment.objects.all()
    amount=0
    for i in revenue:
        amount+=float(i.amount_paid)
    amt=round(amount,2)
    labels=[]
    data=[]

    queryset= OrderProduct.objects.all().order_by('-created_at')
    for product in queryset:
        if product.status == 'New':
            New+=1
        elif product.status == 'Accepted':
            Accepted+=1
        elif product.status == 'Completed':
            Completed+=1
        else:
            Cancelled+=1

    print(New)
    print(Accepted)
    print(Completed)
    print(Cancelled)

    labels=["New","Accepted","Completed","Cancelled"]
    data=[New,Accepted,Completed,Cancelled]
         
    
    context={
        'product_count':products,
        'user_count' : users,
        'sales_count' : sales,
        'revenue' : amt,
        'data':data,
        'labels':labels
    }
    return render(request,'Admincust/admindash.html',context)

def active_users(request):
    if "key" in request.GET:
        search_key = request.GET.get('key') if request.GET.get('key') is not None else ''
        users = Accounts.objects.order_by("id").filter(is_admin=False).all() and Accounts.objects.filter(
            username__istartswith=search_key)
        context = {'users': users}
        return render(request, "admincust/activeusers.html", context)
    else:
        users = Accounts.objects.order_by("id").filter(is_admin=False).all()
        context = {'users': users}
    return render(request, "admincust/activeusers.html", context)




#  @login_required(login_url='adminlogin')
def block_user(request, user_id):
    user = Accounts.objects.get(pk=user_id)
    user.is_active = False
    user.save()
    print('success')
    return redirect("active_users")


# @login_required(login_url='adminlogin')
def unblock_user(request, user_id):
    user = Accounts.objects.get(pk=user_id)
    user.is_active = True
    user.save()
    return redirect("active_users")


# admin signin
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminsignin(request):
    if request.user.is_staff:
        return redirect('active_users')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST['password']
        print(email,password)
        user = authenticate(email=email,password=password)
        print(user)
        if user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('active_users')
        else: 
            messages.error(request, 'Invalid Credentials')
            return redirect('adminsignin')
    else:
        print(1)
        return render(request, 'admincust/adminsiginin.html')


def adminlogout(request):
    auth.logout(request)
    return redirect('adminsignin')

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')
def product_man(request):
    products =  Product.objects.all().order_by('-id')
    
    return render(request, 'admincust/product_man.html', {'products': products})
    

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')
def editProduct(request, id):
    edtproduct = Product.objects.get(pk= id)
    form = ProductForm(instance=edtproduct)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=edtproduct)
        if form.is_valid():
            form.save()
            return redirect("product_man")

    context = {"form": form}
    return render(request, "admincust/editproduct.html", context)

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')
def addProduct(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES,)
        if form.is_valid():
            form.save()
            return redirect("product_man")

    context = {"form": form}
    return render(request, "admincust/addproduct.html", context)

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')
def deleteProduct(request, id ):
    Product.objects.filter(id=id).delete()
    return redirect("product_man")

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')
def categorylists(request):
    Categories = Category.objects.all()
    return render(
        request, "admincust/categorylist.html", {"Categories": Categories}
    )
@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def addcategory(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("categorylists")
    context = {"form": form}
    return render(request, "admincust/addcategory.html", context) 
@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def editcategory(request,id):
    edtcategory = Category.objects.get(pk=id)
    form = CategoryForm(instance=edtcategory)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=edtcategory)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {"form": form}
                # messages.info(request,"A user with that email address already exists.")
                return render(request, "admincust/editcategory.html", context)
            return redirect("categorylists")

    context = {"form": form}
    return render(request, "admincust/editcategory.html", context) 


@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def deletecategory(request,id):
    dlt = Category.objects.get(pk=id)
    dlt.delete()
    messages.success(request, "Your Product Has been deleted")
    return redirect("categorylists")

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def active_order(request):
    # if request.session.get('login') == True:
        orders = Order.objects.all()
        orderproduct = OrderProduct.objects.filter(Q(status = 'Placed')|Q(status = 'Shipped')).order_by('-created_at')
        payment = Payment.objects.all()
        # for order in orders:
            # print(order.first_name,order.city)
        
        return render(request, 'admincust/active_orders.html', {'orders':orders, 'orderproducts': orderproduct, 'payments': payment})
    # else:
        # return redirect('')

@user_passes_test(check_admin, login_url='/admincust/adminsignin/')   
def order_history(request):
    # if request.session.get('login') == True:
        orders = Order.objects.all()
        orderproduct = OrderProduct.objects.filter(Q(status = 'Delivered')|Q(status = 'Returned')|Q(status = 'Cancelled')).order_by('-created_at')
        return render(request, 'admincust/order_history.html', {'orders':orders, 'orderproducts': orderproduct})
    # else:


 
        # return redirect('logincheck')
        
        
@user_passes_test(check_admin, login_url='/admincust/adminsignin/')                 
def varientlists(request):
    varients = Variation.objects.all()
    print(varients)
    context = {
            "varients": varients
    }
    return render(request, "admincust/product_variation.html", context)
        
@user_passes_test(check_admin, login_url='/admincust/adminsignin/')         
def addvarient(request):
    form = VarientForm()
    if request.method == "POST":
        form = VarientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("varientlists")
    context = {"form": form}
    return render(request, "admincust/add_varient.html", context)



@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def editvarient(request,id):
    edtvarient = Variation.objects.get(pk=id)
    form = EditVarient(instance=edtvarient)
    if request.method == "POST":
        form = EditVarient(request.POST, instance=edtvarient)
        if form.is_valid():
            try:
                form.save()
            except:
                context = {"form": form}
                # messages.info(request,"A user with that email address already exists.")
                return render(request, "admincust/editvarient.html", context)
        return redirect("varientlists")

    context = {"form": form}
    return render(request, "admincust/editvarient.html", context)
@user_passes_test(check_admin, login_url='/admincust/adminsignin/')    
def deletevarient(request,id):
    dlt = Variation.objects.get(pk=id)
    dlt.delete()
    messages.success(request, "Your Product Has been deleted")
    return redirect("varientlists")



def coupon_lists(request):
    today = date.today()
    coupon_form = CouponForm()
    coupons = Coupon.objects.all().order_by("-id")

    for coupon in coupons:
        if coupon.valid_from <= today and coupon.valid_to >= today:
            Coupon.objects.filter(id=coupon.id).update(active=True)
        else:
            Coupon.objects.filter(id=coupon.id).update(active=False)

    context = {
        "coupon_form": coupon_form,
        "coupons": coupons,
    }
    return render(request, "admincust/couponlist.html", context)


def add_coupon(request):
    form = CouponForm()
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("coupon_lists")
    context = {"form": form}
    return render(request, "admincust/add_coupon.html", context)



def editcoupon(request,id):
    edtcoupon = Coupon.objects.get(pk=id)
    form = EditCoupon(instance=edtcoupon)
    if request.method == "POST":
        form = EditCoupon(request.POST, instance=edtcoupon)
        if form.is_valid():
            try:
                form.save()

            except:
                context = {"form": form}
                # messages.info(request,"A user with that email address already exists.")
                return render(request, "admincust/editcoupon.html", context)
            return redirect("coupon_lists")

    context = {"form": form}
    return render(request, "admincust/editcoupon.html", context)


def deletecoupon(request,id):
    cpn = Coupon.objects.get(pk=id)
    cpn.delete()
    messages.success(request, "Your Coupon Has been deleted")
    return redirect("coupon_lists")




@user_passes_test(check_admin, login_url='/admincust/adminsignin/') 
def sales_report(request):
    product = Product.objects.all()
    context = {"product": product}
    return render(request, "admincust/salesreport.html",context)




# def productlists(request):
#     if request.session.has_key("key"):
#         datas = Product.objects.all()
#         print(datas)
#         return render(
#             request,
#             "admincust/productlist.html",
#             {
#                 "datas": datas,
#             },
#         )
#     else:
#         return redirect()
    
    
# def add_product_offer(request):
#     form = ProductForm()
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("existing_product_Offer")
#     context = {"form": form}
#     return render(request, "admincust/add_product_offer.html", context)

# def editProductOffer(request,id):
#     editProductOff = Product.objects.get(pk=id)
#     form = EditProductOffer(instance=editProductOff)
#     if request.method == "POST":
#         form = EditProductOffer(request.POST, instance=editProductOff)
#         if form.is_valid():
#             try:
#                 form.save()

#             except:
#                 context = {"form": form}
#                 # messages.info(request,"A user with that email address already exists.")
#                 return render(request, "admincust/editProductOffer.html", context)
#             return redirect("existing_product_Offer")

#     context = {"form": form}
#     return render(request, "admin/editProductOffer.html", context)


# def deleteProductOffer(request,id):
#     dlt = Product.objects.get(pk=id)
#     dlt.delete()
#     return redirect("existing_product_Offer")
# def activeorders(request):
#     exclude_list = ["Delivered", "Canceled"]
#     active_orders = OrderProduct.objects.all().exclude(
#         status__in=exclude_list
#     )[
#         ::-1
#     ]  # for reversing the order.
#     status = STATUS
#     context = {
#         "active_orders": active_orders,
#         "status": status,
#     }
#     return render(request, "admincust/active_orders.html", context)


# def order_history(request):
#     exclude_list = [
#         "New",
#         "Accepted",
#         "Placed",
#         "Shipped",
#     ]
#     active_orders = OrderProduct.objects.all().exclude(
#         status__in=exclude_list
#     )[::-1]
#     status = STATUS1
#     context = {
#         "active_orders": active_orders,
#         "status": status,
#     }
#     return render(request, "admincust/order-history.html", context)
# def order_status_change(request):
#     id = request.POST["id"]
#     status = request.POST["status"]
#     order_product = OrderProduct.objects.get(id=id)
#     order_product.status = status
#     order_product.save()
#     return JsonResponse({"success": True})

# def add_product(request):
#     if request.session.get('login') == True:
#         if request.method == 'POST':

#             form = ProductForm(request.POST, request.FILES)
#             print(request.FILES)
#             if form.is_valid():
#                 product = form.save()
#                 if product.offer is not None:
#                     product.actual_price = product.price
#                     product.price = int(product.actual_price-(product.actual_price*product.offer/100))
#                     print(product.price,'price')
#                     print(product.actual_price,'actual_price')

#                 else:
#                     product.price = int(product.price)
#                 form.save()
#                 return redirect('product_man')
#             else:
#                 return redirect('add_product')
#         else:

    #         form = ProductForm()
    #         products = Product.objects.all()
    #         return render(request, 'admin/add_product.html', {'products': products, 'form': form})
    # else:
    #     return redirect('logincheck')



# def delete_pro(request):
#     if request.session.get('login') == True:
#         id = request.POST['id']
#         Product.objects.filter(id=id).delete()
#         return HttpResponse({'success': True})
#     else:
#         return redirect('logincheck')


# def product_update(request, slug):
#     if request.session.get('login') == True:
#         product = Product.objects.get(slug=slug)
#         if request.method == 'POST':
#             form = ProductForm(request.POST, request.FILES, instance=product)

#             if form.is_valid():
#                 product = form.save()
#                 if product.offer is not None:
#                     product.actual_price = product.price
#                     product.price = int(product.actual_price-(product.actual_price*product.offer/100))
#                     print(product.price,'price')
#                     print(product.actual_price,'actual_price')

            #     else:
            #         product.price = int(product.price)
            #     form.save()
            #     return redirect('product_man')
            # else:
    #             return redirect('product_update' ,slug=slug)
    #     else:
    #         form = ProductForm(instance=product)
    #         return render(request, 'admin/product_update.html', {'product': product, 'form': form})
    # else:
    #     return redirect('logincheck') 

