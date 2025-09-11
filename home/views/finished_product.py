
from django.shortcuts import render, redirect
from home.models import Final_Product,Finish_Product_Category
from home.forms import Finish_ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required

@login_required
@permission_required('home.view_product', login_url='/login/')
def products(request):
    category_selected=False
    categoryID=(request.GET.get('category'))
    if categoryID:
        categories=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
        category_selected=True
        products=Final_Product.objects.filter(category=categoryID,is_deleted=False)
        # products=Product.objects.filter(is_deleted=False)
        print(products)
    else:
        categories=Finish_Product_Category.objects.filter(is_deleted=False)
        products=Final_Product.objects.filter(is_deleted=False).order_by('category')
    data={'products':products,'categories':categories,'category_selected':category_selected}
    return render(request,"stock_finished_product/products_home.html",data)   

@login_required
# @permission_required('home.add_sales_product', login_url='/login/')
def add_product(request,id=''):
  if id:
    categories=Finish_Product_Category.objects.filter(is_deleted=False,id=id)
  else:
    categoryID=int((request.GET.get('category')))
    categories=Finish_Product_Category.objects.filter(is_deleted=False,id=categoryID)
  if request.method == 'POST':
      mydata=Final_Product.objects.filter(is_deleted=False)
      form = Finish_ProductForm(request.POST,request.FILES)
      if form.is_valid():
        form.save()
        messages.success(request,"Product Added successfully !!")
        if id:
          return redirect('addfinishedproduct1',id)
        else:
          return redirect('addfinishedproduct1',categoryID)
  else:
      
      if id:
        cat=Finish_Product_Category.objects.get(is_deleted=False,id=id)
      else:
        cat=Finish_Product_Category.objects.get(is_deleted=False,id=categoryID)
      mydata=Final_Product.objects.filter(is_deleted=False,category=cat).order_by("-id")
      form = Finish_ProductForm(initial={'category': cat})
  data={'form': form, 'mydata':mydata,'categories':categories,'prod':True}
  return render(request, 'stock_finished_product/add_Product.html', data)

@login_required
@permission_required('home.change_sales_product', login_url='/login/')
def edit_product(request,id):
  data={}
  if request.method == 'POST':
    mydata=Final_Product.objects.get(id=id)
    categoryID=mydata.category.id
    form = Finish_ProductForm(request.POST,request.FILES,instance=mydata)
    if form.is_valid():
      form.save()
      messages.success(request,"Product Updated successfully !!")
      return redirect('addfinishedproduct1',categoryID)
  else:
    mydata=Final_Product.objects.get(id=id) 
    form = Finish_ProductForm(instance=mydata)
  data={'form': form, 'mydata':mydata,'update':True,}
  return render(request, 'stock_finished_product/add_Product.html', data)

@login_required
@permission_required('home.delete_product', login_url='/login/')
def delete_product(request,id):
  
  mydata=Final_Product.objects.get(id=id)
  categoryID=mydata.category.id
  mydata.is_deleted=True
  mydata.save()
  messages.success(request,"Product Deleted successfully !!")
  return redirect('addfinishedproduct1',categoryID)

def delete_product1(request,id):
  
  mydata=Final_Product.objects.get(id=id)
  categoryID=mydata.category.id
  mydata.is_deleted=True
  mydata.save()
  messages.success(request,"Product Deleted successfully !!")
  return redirect('finishedproduct')


from ..models import Inventory

def inventory(request):

  inventory = Inventory.objects.all()
  # print(f"Product: {inventory.product.productname}, Stock: {inventory.quantity} units")
  print(inventory)
  data={ 'mydata':inventory}
  return render(request, 'stock_finished_product/inventory.html', data)
