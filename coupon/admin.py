from django.contrib import admin

# Register your models here.
# from django.contrib import admin

from coupon.models import Coupon, ReviewCoupon

# Register your models here.


class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "valid_from", "valid_to", "discount", "active"]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]


admin.site.register(Coupon,CouponAdmin)
admin.site.register(ReviewCoupon)