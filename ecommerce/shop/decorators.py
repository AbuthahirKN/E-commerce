from django.http import HttpResponse
def admin_required(fun):
    def wrapper(request):
        if request.user.is_superuser:
            return HttpResponse('Admin only')
        else:
            return fun(request)
    return wrapper