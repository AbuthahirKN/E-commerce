from django.shortcuts import render,render
from django.views import View
from django.db.models import Q
from shop.models import Product

# Create your views here.
class SearchProduct(View):

    def get(self,request):
        query=request.GET['q']
        print(query)
        p=Product.objects.filter(Q(name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(price__icontains=query))
        context={'product':p}
        return render(request,'search.html',context)




