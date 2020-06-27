from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory, inlineformset_factory
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from .models import NutritionalInfo, Product, NutritionalInfoValues
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views

# VIEWS for Nutritional Info
@method_decorator([login_required], name='dispatch')
class NutritionalInfoListView(ListView):
	queryset = NutritionalInfo.objects.all()
	context_object_name = 'nutritional_infos'
	template_name = 'restaurant/nutritional_info/list.html'

@method_decorator([login_required], name='dispatch')	
class NutritionalInfoCreateView(CreateView):
	model = NutritionalInfo
	template_name = 'restaurant/nutritional_info/create.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:nutritional_info_list')
	
@method_decorator([login_required], name='dispatch')
class NutritionalInfoDetailView(DetailView):
	model = NutritionalInfo	
	
@method_decorator([login_required], name='dispatch')	
class NutritionalInfoUpdateView(UpdateView):
	model = NutritionalInfo
	template_name = 'restaurant/nutritional_info/update.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:nutritional_info_list')
	
@method_decorator([login_required], name='dispatch')	
class NutritionalInfoDeleteView(DeleteView):
	model = NutritionalInfo
	template_name = 'restaurant/nutritional_info/delete.html'
	permission_required = 'NutritionalInfos.delete_NutritionalInfo'
	success_url = reverse_lazy('restaurant:nutritional_info_list')
	
# Views for Product
@method_decorator([login_required], name='dispatch')
class ProductListView(ListView):
	model  = Product
	context_object_name = 'products'
	template_name = 'restaurant/product/list.html'
	
@method_decorator([login_required], name='dispatch')	
class ProductUpdateView(UpdateView):
	model = Product
	template_name = 'restaurant/product/update.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
	
@method_decorator([login_required], name='dispatch')	
class ProductUpdateView2(UpdateView):
	model = Product
	template_name = 'restaurant/product/update2.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
@method_decorator([login_required], name='dispatch')	
class ProductUpdateView3(UpdateView):
	model = Product
	template_name = 'restaurant/product/update3.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
@method_decorator([login_required], name='dispatch')	
class ProductUpdateView4(UpdateView):
	model = Product
	template_name = 'restaurant/product/update4.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
@method_decorator([login_required], name='dispatch')	
class ProductDeleteView(DeleteView):
	model = Product
	template_name = 'restaurant/product/delete.html'
	success_url = reverse_lazy('restaurant:product_list')

from restaurant.forms import NutritionalInfoValuesForm, NutritionalInfoValuesFormFormSet, ProductForm, MyFormSimple

formset2 = NutritionalInfoValuesFormFormSet(initial=[
			{'nutritional_info': '1',
			 'product': "2",
			 "values": "200.00"}
		])
@method_decorator([login_required], name='dispatch')	
class ProductCreateView(CreateView):
	model = Product
	template_name = 'restaurant/product/create.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
	def get(self, request, *args, **kwargs):
		context = {'form': MyFormSimple(),
				   #'form_set': NutritionalInfoValuesFormFormSet()
				   }
		return render(request, 'restaurant/product/create.html', context)
		
@method_decorator([login_required], name='dispatch')	
class ProductCreateView2(CreateView):
	model = Product
	template_name = 'restaurant/product/create2.html'
	fields = "__all__"
	success_url = reverse_lazy('restaurant:product_list')
	
	def get(self, request, *args, **kwargs):
		context = {'form': MyFormSimple(),
				   #'form_set': NutritionalInfoValuesFormFormSet()
				   }
		return render(request, 'restaurant/product/create2.html', context)

@login_required		
def create_product(request):
	if request.method == 'POST':
		form = MyFormSimple(request.POST)
		keys_inlineforms = [el for el in request.POST.keys() if ("nutritional_info" in el or "values" in el) and request.POST[el] !=['']]
		data_inlineforms = [request.POST[key] for key in keys_inlineforms]
		form_set = NutritionalInfoValuesFormFormSet(request.POST)
		if form.is_valid() and form_set.is_valid():
			cd = form.cleaned_data
			ASSOCIATED_DATA = form_set.cleaned_data
			DATA_DICT = { ky: request.POST.dict()[ky] for ky in ["nombre", "description", "status"]}
			DATA_DICT["name"] = DATA_DICT["nombre"]
			del DATA_DICT["nombre"]
			new_product = Product.objects.create(**DATA_DICT)
			for el in ASSOCIATED_DATA:
				if el:
					NutritionalInfoValues.objects.create(product=new_product, 
														 nutritional_info=el["nutritional_info"],
														 values=el["values"])
			return HttpResponseRedirect(reverse('restaurant:product_list'))
	else:
		form = MyFormSimple()
		form_set = NutritionalInfoValuesFormFormSet()
		return render(request, 'restaurant/product/create3.html', {'form': form, 'formset': form_set})
		

from django.shortcuts import render, get_object_or_404, redirect		
def post_update(request, pk=None):
	#if not request.user.is_staff or not request.user.is_superuser:
	#	raise Http404
	instance = get_object_or_404(Product, pk=pk)
	print(instance)
	data = {"name": instance.name, 
			"description": instance.description, 
			"status": instance.status}
	data_rel = []
	for el in instance.nutritionalinfovalues_set.all():
		data_rel.append({"product": el.product.name, 
					 "nutritional_info": el.nutritional_info.name, 
					 "values": el.values})
	print(data)
	print(data_rel)
	form = ProductForm(data)
	form2 = MyFormSimple(data)
	for el in data_rel:
		formset = NutritionalInfoValuesFormFormSet(data_rel)
	print(form2)
	print("***")
	print(formset)
	print("=================")
	print(request.POST)
	if form2.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
	return render(request, "post_form.html", context)
	
def post_update2(request, pk=None):
	#if not request.user.is_staff or not request.user.is_superuser:
	#	raise Http404
	instance = get_object_or_404(Product, pk=pk)
	print(instance)
	data = {"nombre": instance.name, 
			"description": instance.description, 
			"status": instance.status}
	#		
	form = MyFormSimple(data)					
	
	
	data_rel = []
	for el in instance.nutritionalinfovalues_set.all():
		data_rel.append({"product": el.product.name, 
					     "nutritional_info": el.nutritional_info.name, 
					     "values": el.values})
						 
	num_forms = len(instance.nutritionalinfovalues_set.all())
	NutritionalInfoValuesFormFormSet = formset_factory(NutritionalInfoValuesForm, extra=num_forms, max_num=num_forms)
	import pdb; pdb.set_trace()
	for el in data_rel:
		formset = NutritionalInfoValuesFormFormSet(data_rel)
		
	print(data_rel)
	print("=================")
	
	
	if request.method == 'POST':
		import pdb; pdb.set_trace()	
	
	if form.is_valid():
		import pdb; pdb.set_trace()
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"instance": instance,
		"form":form,
	}
	return render(request, "restaurant/product/update2.html", context)