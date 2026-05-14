from django.shortcuts import render,redirect
from django.views import View
from shop.models import Product
from cart.models import Cart,Order,OrderItems
from cart.forms import OrderForm
import razorpay
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator




# Create your views here.
class AddToCart(View):
    def get(self,request,i):
        u = request.user
        p=Product.objects.get(id=i)
        try:
            c = Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c = Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')

class CartView(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total = total+(i.quantity*i.product.price)
        context={'cart':c,'total':total}
        return render(request,'carts.html',context)

class CartDecrement(View):
    def get(self,request,i):

        try:
            c = Cart.objects.get(id=i)
            if c.quantity > 1:
               c.quantity-=1
               c.save()
            else:
               c.delete()
        except:
            pass
        return redirect('cart:cartview')
class CartRemove(View):
    def get(self,request,i):
        try:
           c=Cart.objects.get(id=i)
           c.delete()
        except:
            pass
        return redirect('cart:cartview')
import uuid
class Checkout(View):
    def post(self, request):
        form_instance = OrderForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)
            user= request.user
            u.user=user
            c=Cart.objects.filter(user=user)
            total=0
            for i in c:
                total = total+(i.quantity*i.product.price)
            u.amount=total
            u.save()
            if(u.payment_method == 'ONLINE'):
                client = razorpay.Client(auth=('rzp_test_SeUpNfJqzkH1Bt','XgiGyGAEFPcMh13TcJWrxQ5D'))
                response_payment = client.order.create({'amount':int(u.amount*100),'currency':'INR'})
                print(response_payment)
                id=response_payment['id']
                u.order_id = id
                u.save()


                context={'payment':response_payment}
                return render(request, 'payment.html', context)
            else:
                id=uuid.uuid4().hex[:14]
                i='order_COD'+id
                u.order_id=i
                u.is_ordered = True
                u.save()

                c = Cart.objects.filter(user=user)
                for i in c:
                    items = OrderItems.objects.create(order=u, quantity=i.quantity, product=i.product)
                    items.save()
                    # cart deleted after creating order items
                    c.delete()
            return render(request,'payment.html')
    def get(self,request):
        form_instance = OrderForm()
        context={'form':form_instance}
        return render(request,'checkout.html',context)

@method_decorator(csrf_exempt,name='dispatch')
class PaymentSuccess(View):
    def post(self,request):
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()

        c=Cart.objects.filter(user=o.user)
        for i in c:
            items = OrderItems.objects.create(order=o,quantity=i.quantity,product=i.product)
            items.save()
            #cart deleted after creating order items
            c.delete()



        return render(request,'paymentsuccess.html')
class OrderSummary(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'ordersummary.html',context)

