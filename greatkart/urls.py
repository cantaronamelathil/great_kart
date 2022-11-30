from .import views
from django.urls import path



urlpatterns = [
    path('',views.home,name='home'),
    # path('<slung:category_slug>/',views., name='home')
]

