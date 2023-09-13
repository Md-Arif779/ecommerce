from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg
from taggit.models import Tag
from calc.forms import ProductReviewForm
from calc.models import Product, Category, Vendor, ProductImage, CartOrder, CartOrdrItems, ProductReview, Wishlist, Adress
# Create your views here.
def home(request):
    #products = Product.objects.all()
    products = Product.objects.filter(products_status="published", featured=True)

    context = {
        'product': products
    }
    return render(request, 'calc/home.html', context)


def product_list(request):
    products = Product.objects.filter(products_status="published")

    context = {
        'product': products
    }
    return render(request, 'calc/product-list.html', context)


def category_list(request):
    #categorys = Category.objects.all()
    categorys = Category.objects.all().annotate(product_count=Count("category")) 

    context = {
        'category': categorys
    }
    return render(request, 'calc/category-list.html', context)

 

def category_product_list(request, cid):
    category = Category.objects.get(cid=cid)
    product = Product.objects.filter(products_status="published", category=category)

    context = {
        'category': category,
        'product': product,
    }
    return render(request, 'calc/category-product-list.html', context)


def vendor(request):
    vendors = Vendor.objects.all()

    context = {
        'vendors': vendors,
    }

    return render(request, 'calc/vendor.html', context)


def vendor_detail(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    product = Product.objects.filter(vendor=vendor, products_status="published",)
    context = {
        'vendor':vendor,
        'product':product
    }
    return render(request, 'calc/vendor-detail.html', context)


def product_detail(request, pid):
    #product = get_object_or_404(Product, pid=pid)
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Gatting all review 
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Gatting  average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    # Product review form
    review_form = ProductReviewForm()
    
    p_image = product.p_image.all()

    context = {
        'review_form': review_form,
        'product':product,
        'p_image':p_image,
        'products':products,
        'reviews':reviews,
        'average_rating':average_rating,
    }

    return render(request, 'calc/product-detail.html', context)


def tag_list(request, tag_slug=None):
    product = Product.objects.filter(products_status="published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = product.filter(tags__in=[tag])

        context = {
            'products':products,
            'tag':tag,
        }
        return render(request, 'calc/tag.html', context)
    

def search(request):
    query = request.GET.get("q", None)

    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "query": query,
        "products": products
    }
    return render(request, 'calc/search.html', context)
       