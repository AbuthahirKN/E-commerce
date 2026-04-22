from django.shortcuts import render,redirect
from django.views import View
from shop.forms import SignupForm,LoginForm,CategoryForm,ProductForm,StockForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from shop.models import Category,Product




# Create your views here.
class Categories(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'categories.html',context)

class Register(View):
    def post(self,request):
        form_instance =SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
    def get(self,request):
        form_instance=SignupForm()
        context={'form':form_instance}
        return render(request,'register.html',context)
class AddCategory(View):
    def post(self,request):
        form_instance = CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
    def get(self,request):
        form_instance = CategoryForm()
        context={'form':form_instance}
        return render(request,'addcategory.html',context)
class AddProduct(View):
    def post(self,request):
        form_instance = ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
    def get(self,request):
        form_instance = ProductForm()
        context={'form':form_instance}
        return render(request,'addcategory.html',context)
class Products(View):
    def get(self, request,i):
        p = Category.objects.get(id=i)
        context={'category':p}
        return render(request, 'product.html',context)

class ProductDetails(View):
    def get(self,request,i):
        p = Product.objects.get(id=i)
        context={'product':p}
        return render(request, 'productdetails.html',context)
class AddStock(View):
    def post(self,request,i):
        p = Product.objects.get(id=i)
        form_instance = StockForm(request.POST,request.FILES,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')

    def get(self,request,i):
        p = Product.objects.get(id=1)
        form_instance= StockForm(instance=p)
        context={'form':form_instance}
        return render(request,'addstock.html',context)


class Login(View):
    def post(self,request):
        form_instance =LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            user=authenticate(request,username=u,password=p)
            if user and user.is_superuser==True:
                login(request,user)
                return redirect('shop:ashop')
            elif user and user.is_superuser==False:
                login(request,user)
                return redirect('shop:user')
            else:
                messages.error(request,'invalid credentials')
                return redirect('shop:login')
    def get(self,request):
        form_instance =LoginForm()
        context={'form':form_instance}
        return render(request,'login.html',context)

class Normaluser(View):
    def get(self, request):
        return render(request, 'user.html')

class Admin(View):
    def get(self, request):
        return render(request, 'admin.html')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:categories')