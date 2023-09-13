from calc.models import Product, Category, Vendor, ProductImage, CartOrder, CartOrdrItems, ProductReview, Wishlist, Adress
from django.db.models import Min, Max

def default(request):
    # Your custom context variables
    categories = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    return {
        'categories':categories,
        'min_max_price': min_max_price,
    }
