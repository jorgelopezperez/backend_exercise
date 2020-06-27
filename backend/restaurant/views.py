from django.http import HttpResponse, HttpResponseRedirect
from django.forms import formset_factory, inlineformset_factory
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, DetailView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect		
from .models import NutritionalInfo, Product, NutritionalInfoValues
from .forms import NutritionalInfoValuesForm, NutritionalInfoValuesFormFormSet, ProductForm, MyFormSimple


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


@login_required		
def create_product(request):
	if request.method == 'POST':
		form = MyFormSimple(request.POST)
		keys_inlineforms = [el for el in request.POST.keys() if ("nutritional_info" in el or "values" in el) and request.POST[el] !=['']]
		data_inlineforms = [request.POST[key] for key in keys_inlineforms]
		form_set = NutritionalInfoValuesFormFormSet(request.POST)
		import pdb; pdb.set_trace()
		if form.is_valid() and form_set.is_valid():
			cd = form.cleaned_data
			ASSOCIATED_DATA = form_set.cleaned_data
			DATA_DICT = { ky: request.POST.dict()[ky] for ky in ["nombre", "description", "status"]}
			DATA_DICT["name"] = DATA_DICT["nombre"]
			del DATA_DICT["nombre"]
			new_product = Product.objects.create(**DATA_DICT)
			import pdb; pdb.set_trace()
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
		



@login_required	
def update_product(request, pk=None):
	instance = get_object_or_404(Product, pk=pk)
	print(instance)
	data = {"nombre": instance.name, 
			"description": instance.description, 
			"status": instance.status}
	#		
	form = MyFormSimple(data)					
	
	data_rel = []
	data_rel_ = []
	for el in instance.nutritionalinfovalues_set.all():
		data_rel.append({"product": el.product.name, 
					     "nutritional_info": el.nutritional_info.name, 
					     "values": el.values})
		data_rel_.append({"product": el.product.name, 
					     "nutritional_info": el.nutritional_info.pk, 
					     "values": el.values})
						 
	num_forms = len(instance.nutritionalinfovalues_set.all())
	NutritionalInfoValuesFormFormSet = formset_factory(NutritionalInfoValuesForm, extra=num_forms, max_num=num_forms)
	for el in data_rel:
		formset = NutritionalInfoValuesFormFormSet(el)
		
	data_inlineforms__ = [{"form-0-nutritional_info": "1", "form-0-values": "1111"},
	{"form-0-nutritional_info": "6", "form-0-values": "2222"}]
		
	DICT_HIDDEN = {'form-TOTAL_FORMS': num_forms, 
					'form-INITIAL_FORMS': '0', 
					'form-MIN_NUM_FORMS': '0',
					'form-MAX_NUM_FORMS': num_forms}	
			
	LIST_DICT_VISIBLE = []
	for id,data in enumerate(data_rel_):
		key1   = "form-" + str(id) + "-nutritional_info"
		value1 =  data_rel_[id]["nutritional_info"]
		key2   = "form-" + str(id) + "-values"
		value2 =  data_rel_[id]["values"]
		mydict = {key1: value1, key2: value2}
		LIST_DICT_VISIBLE.append(mydict)
		
	from collections import ChainMap
	DICT_VISIBLE = dict(ChainMap(*LIST_DICT_VISIBLE))
	LIST_DICT_TOTAL = [DICT_VISIBLE] + [DICT_HIDDEN]
	data_inlineforms = dict(ChainMap(*LIST_DICT_TOTAL))
	data_inlineforms__2 = {"nutritional_info": "1", "values": "1111"}
	
	form_set = NutritionalInfoValuesFormFormSet(data_inlineforms)
	#OLD_KEYS = list(set([list(el.keys()).pop(0) for el in form_set.cleaned_data]))
	OLD_NUTRITIONAL_INFO_LIST_DICTS = form_set.cleaned_data
	OLD_KEYS = list(set([list(el.keys()).pop(0) for el in form_set.cleaned_data]))
	OLD_NUTRITIONAL_INFO = [el["nutritional_info"].name for el in form_set.cleaned_data]
	print("OLD_NUTRITIONAL_INFO")
	print(OLD_NUTRITIONAL_INFO)
	if request.method == 'POST':
		form = MyFormSimple(request.POST)
		form_set = NutritionalInfoValuesFormFormSet(request.POST)
		#import pdb; pdb.set_trace()		
		if form.is_valid() and form_set.is_valid():
			cd = form.cleaned_data
			ASSOCIATED_DATA = form_set.cleaned_data
			print("ASSOCIATED_DATA")
			print(ASSOCIATED_DATA)
			NEW_ASSOCIATED_DATA_LIST = [el["nutritional_info"].name for el in ASSOCIATED_DATA]
			print("NEW_ASSOCIATED_DATA_LIST")
			print(NEW_ASSOCIATED_DATA_LIST)
			TO_DELETE_partial = list(set(OLD_NUTRITIONAL_INFO) - set(NEW_ASSOCIATED_DATA_LIST))
			TO_DELETE_BETTER  = [{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in OLD_NUTRITIONAL_INFO_LIST_DICTS if el["nutritional_info"].name in TO_DELETE_partial]
			TO_INSERT_partial = list(set(NEW_ASSOCIATED_DATA_LIST) - set(OLD_NUTRITIONAL_INFO))
			TO_INSERT_BETTER  = [{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in ASSOCIATED_DATA if el["nutritional_info"].name  in TO_INSERT_partial]
			TO_UPDATE_partial = list(set([el["values"] for el in ASSOCIATED_DATA]) - set([el["values"] for el in OLD_NUTRITIONAL_INFO_LIST_DICTS]))
			TO_UPDATE = [{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in ASSOCIATED_DATA if el["values"] in TO_UPDATE_partial]
			TO_UPDATE_BETTER = [{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in ASSOCIATED_DATA if el["values"] in TO_UPDATE_partial and el["nutritional_info"].name not in TO_INSERT_partial]
			#import pdb; pdb.set_trace()
			print([{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in ASSOCIATED_DATA if el["nutritional_info"].name in TO_INSERT_partial])
			print([{"nutritional_info": el["nutritional_info"].name, "values": el["values"]} for el in OLD_NUTRITIONAL_INFO_LIST_DICTS if el["nutritional_info"].name in TO_DELETE_partial])
			print([el for el in OLD_NUTRITIONAL_INFO_LIST_DICTS if el["nutritional_info"].name in TO_DELETE_partial])
			DATA_DICT = { ky: request.POST.dict()[ky] for ky in ["nombre", "description", "status"]}
			DATA_DICT["name"] = DATA_DICT["nombre"]
			del DATA_DICT["nombre"]
			
			if TO_UPDATE_BETTER != []:	
				for el in ASSOCIATED_DATA:
					to_update_nutr_instance = NutritionalInfoValues.objects.filter(product_id = instance.pk, nutritional_info__name = el["nutritional_info"].name).get()
					to_update_nutr_instance.values = el["values"]
					to_update_nutr_instance.save()
					
			if TO_DELETE_partial != [] and TO_INSERT_partial != []:	
				for el in TO_DELETE_BETTER:
					print("el-delete")
					print(el)
					import pdb; pdb.set_trace()
					NutritionalInfoValues.objects.filter(product=instance,  nutritional_info__name = el["nutritional_info"]).delete
				for el in TO_INSERT_BETTER:
					print("el-insert")
					print(el)
					#import pdb; pdb.set_trace()
					nutritional_instance = NutritionalInfo.objects.get(name=el["nutritional_info"])
					print(nutritional_instance)
					NutritionalInfoValues.objects.create(product=instance,  nutritional_info = nutritional_instance,values=el["values"])
					#instance.nutritionalinfovalues_set.create
				
				
			'''
			for el in ASSOCIATED_DATA:
				print("el")
				print(el)
				if el["nutritional_info"].name in OLD_NUTRITIONAL_INFO:
					print("UPDATING")
					to_update_nutr_instance = NutritionalInfoValues.objects.filter(product_id = instance.pk, nutritional_info__name = el["nutritional_info"].name).get()
					to_update_nutr_instance.values = el["values"]
					to_update_nutr_instance.save()
				else:
					print("DELETING")
					to_delete_nutr_instance = NutritionalInfoValues.objects.filter(product_id = instance.pk, nutritional_info__name = el["nutritional_info"].name).get()
					to_delete_nutr_instance.values = el["values"]
					to_delete_nutr_instance.save()
			'''
			#messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
			return HttpResponseRedirect(reverse('restaurant:product_list'))

	context = {
		"instance": instance,
		"form":form,
		"form_set":form_set,
	}
	return render(request, "restaurant/product/update.html", context)