from django.shortcuts import render, redirect,get_object_or_404
from home.models import Price_List,Final_Product_Price
from home.forms import Price_ListForm,Final_Product_PriceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required

@login_required
@permission_required('home.add_project', login_url='/login/')
def pricelist_detail(request,id):
  mydata=None
  if request.user.is_authenticated:
    price_list=Price_List.objects.get(is_deleted=False,id=id)
    print(price_list.id)
    if price_list:
        mydata=Final_Product_Price.objects.filter(is_deleted=False,price_list_id=price_list.id)

    data={'mydata':mydata, 'price_list':price_list ,'form':Final_Product_PriceForm()}
    return render(request, 'price_list/add_price_list.html', data )
  else:
    return redirect('signin')

@login_required
@permission_required('home.add_project', login_url='/login/')
def add_pricelist(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
       
        mydata=Price_List.objects.filter(is_deleted=False)
        form = Price_ListForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Region Added successfully !!")
          return redirect('pricelist')
    else:
        mydata=Price_List.objects.filter(is_deleted=False)
        
        form = Price_ListForm()
    data={'form': form, 'mydata':mydata,}
    return render(request, 'price_list/add_price_list.html', data)
  else:
    return redirect('signin')

@login_required
@permission_required('home.change_project', login_url='/login/')
def edit_pricelist(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Price_List.objects.get(id=id)
      form = Price_ListForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Region Updated successfully !!")
        return redirect('region')
    else:
      mydata=Price_List.objects.get(id=id)
      form = Price_ListForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True }
  return render(request, 'price_list/add_price_list.html', data)


from django.db.models.deletion import ProtectedError

@login_required
@permission_required('home.view_delete', login_url='/login/')
def delete_pricelist(request, id):
    try:
        mydata = get_object_or_404(Price_List, id=id)
        mydata.delete()
        messages.success(request, "Region Deleted successfully !!")
    except ProtectedError as e:
        related_objects = e.protected_objects  # Get the related objects that are blocking the delete
        messages.error(
            request, 
            f"Cannot delete '{mydata.name}' because it is referenced by: "
            f"{', '.join([str(obj) for obj in related_objects])}. Please delete the related objects first."
        )
    return redirect('pricelist')