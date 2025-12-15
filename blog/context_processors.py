from .models import Category


def global_context(request):
    selected_category = request.GET.get('category')
    return {
        'categories': Category.objects.all(),
        'selected_category': selected_category,
    }
