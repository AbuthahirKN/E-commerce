from cart.models import Cart

def cart_items(request):
    u=request.user
    total=0
    try:
     c=Cart.objects.filter(user=u)

     for i in c:
         total=total+i.quantity
    except:
          total=0
    return {'count':total}





