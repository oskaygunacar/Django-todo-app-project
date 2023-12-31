from todo_app.models import Category

def context_processor(request):
    if request.user.is_authenticated:
        categories = Category.objects.filter(is_active=True, user=request.user).all()
    else:
        categories = Category.objects.filter(is_active=True).all()
    return {'categories':categories}