
from django.shortcuts import render, redirect
from home.models import Product_Price,Category
from home.forms import Product_PriceForm,search_Product_PriceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.add_product_price', login_url='/login/')
def add_product_price(request,id=''):
    if id:
        cat=Category.objects.filter(is_deleted=False,id=id)
        cat1=Category.objects.get(is_deleted=False,id=id)
    else:
        categoryID=int((request.GET.get('category')))
        cat=Category.objects.filter(is_deleted=False,id=categoryID)
        cat1=Category.objects.get(is_deleted=False,id=categoryID)
    if request.method == 'POST':
        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1)
        form = Product_PriceForm(request.POST,category=cat1)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Added successfully !!")
            return redirect('addproductprice', id if id else categoryID)
    else:
        
        if id:
            cat=Category.objects.filter(is_deleted=False,id=id)
            cat1=Category.objects.get(is_deleted=False,id=id)
        else:
            cat=Category.objects.filter(is_deleted=False,id=categoryID)
            cat1=Category.objects.get(is_deleted=False,id=categoryID)

        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1).order_by("-id")
        form = Product_PriceForm(category=cat1)
    data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
    return render(request, 'stock/add_product_prices.html', data)

@login_required
@permission_required('home.change_product_price', login_url='/login/')
def edit_product_price(request,id):
    data={}
    if request.method == 'POST':
        mydata=Product_Price.objects.get(id=id)
        categoryID=mydata.product.category.id
        form = Product_PriceForm(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request,"Product Updated successfully !!")
            return redirect('addproductprice',categoryID)
    else:
        mydata=Product_Price.objects.get(id=id) 
        form = Product_PriceForm(instance=mydata)
    data={'form': form, 'mydata':mydata,'update':True,}
    return render(request, 'stock/add_product_prices.html', data)

@login_required
@permission_required('home.delete_product_price', login_url='/login/')
def delete_product_price(request,id):

    mydata=Product_Price.objects.get(id=id)
    categoryID=mydata.product.category.id
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Product Deleted successfully !!")
    return redirect('addproductprice',categoryID)


@login_required
# @permission_required('home.add_product_price', login_url='/login/')
def search_product_price(request,id=''):
    if id:
        cat=Category.objects.filter(is_deleted=False,id=id)
        cat1=Category.objects.get(is_deleted=False,id=id)
    else:
        categoryID=int((request.GET.get('category')))
        cat=Category.objects.filter(is_deleted=False,id=categoryID)
        cat1=Category.objects.get(is_deleted=False,id=categoryID)
    if request.method == 'POST':
        form = search_Product_PriceForm(request.POST,category=cat1)
        if form.is_valid():
            product=form.cleaned_data["product"]
            customer=form.cleaned_data["customer"]
            mydata=Product_Price.objects.filter(is_deleted=False,product=product,customer=customer)
            
        data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
        return render(request, 'stock/search_product_prices.html', data)
    else:
        
        if id:
            cat=Category.objects.filter(is_deleted=False,id=id)
            cat1=Category.objects.get(is_deleted=False,id=id)
        else:
            cat=Category.objects.filter(is_deleted=False,id=categoryID)
            cat1=Category.objects.get(is_deleted=False,id=categoryID)

        mydata=Product_Price.objects.filter(is_deleted=False,product__category_id=cat1).order_by("-id")
        form = search_Product_PriceForm(category=cat1)
    data={'form': form, 'mydata':mydata,'categories':cat,'prod':True,'category':cat1}
    return render(request, 'stock/search_product_prices.html', data)