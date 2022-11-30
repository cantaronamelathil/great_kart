from django.urls import path
from . import views


urlpatterns = [
    # User block
# path('',views.active_users,name='active_users'),
path('active_users/',views.active_users,name='active_users'),
path("blockuser/<user_id>", views.block_user, name="blockuser"),
path("unblockuser/<user_id>", views.unblock_user, name="unblockuser"),
path('adminsignin/',views.adminsignin,name='adminsignin'),
path('adminlogout/',views.adminlogout,name='adminlogout'),
path('product_man/',views.product_man,name= 'product_man'),
path('edit_products/<int:id>', views.editProduct, name="editProduct"),
path('delete_products/<int:id>', views.deleteProduct, name="deleteProduct"),
path('add_products/', views.addProduct, name="addProduct"),
path('categorylists/', views.categorylists, name="categorylists"),
path('addcategory/', views.addcategory, name="addcategory"),
path('editcategory/<int:id>', views.editcategory, name="editcategory"),
path('deletecategory/<int:id>', views.deletecategory, name="deletecategory"),
path('active_order/', views.active_order, name="active_order"),
path('order_history/', views.order_history, name="order_history"),
path('varientlists/', views.varientlists, name="varientlists"),
path('addvarient/', views.addvarient, name="addvarient"),
path('editvarient/<int:id>', views.editvarient, name="editvarient"),
path('deletevarient/<int:id>', views.deletevarient, name="deletevarient"),
path('coupon_lists/', views.coupon_lists, name="coupon_lists"),
path('add_coupon/', views.add_coupon, name="add_coupon"),
path('editcoupon/<int:id>', views.editcoupon, name="editcoupon"),
path('deletecoupon/<int:id>', views.deletecoupon, name="deletecoupon"),
path('dashboard/', views.dashboard, name="dashboard"),
path('sales_report/', views.sales_report, name="sales_report"),
# path('dashboard/', views.dashboard, name="dashboard"),
# path('editvarient/', views.editvarient, name="editvarient"),
# path(' order_status_change/<int:id>', views. order_status_change, name=" order_status_change"),
# path("deleteuser/<user_id>", views.delete_user, name="deleteuser"),
]
    