from django.urls import path, include
from . import views

app_name = 'restaurant'

urlpatterns = [
	path('home', views.home_page, name='restaurant_homepage'),
	path('nutritionalinfo/list', views.NutritionalInfoListView.as_view(), name='nutritional_info_list'),
	path('nutritionalinfo/create', views.NutritionalInfoCreateView.as_view(), name='nutritional_info_create'),
	#path('nutritionalinfo/detail/<int:pk>', views.NutritionalInfoDetailView.as_view(), name='nutritional_info_detail'),
	path('nutritionalinfo/update/<int:pk>', views.NutritionalInfoUpdateView.as_view(), name='nutritional_info_update'),
	path('nutritionalinfo/delete/<int:pk>', views.NutritionalInfoDeleteView.as_view(), name='nutritional_info_delete'),
	path('product/list', views.ProductListView.as_view(), name='product_list'),
	path('product/create', views.create_product, name='product_create'),
	#path('product/detail/<int:pk>', views.NutritionalInfoDetailView.as_view(), name='nutritional_info_detail'),
	path('product/update/<int:pk>', views.update_product, name='product_update'),
	path('product/delete/<int:pk>', views.ProductDeleteView.as_view(), name='product_delete'),
]

