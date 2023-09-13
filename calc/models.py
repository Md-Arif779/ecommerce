from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from users.models import User
from taggit.managers import TaggableManager

# Create your models here.
STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "⭐"),
    (1, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)



def user_derectory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



####Category############
####Category############
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcde12345")
    title = models.CharField(max_length=100, default="Food")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50", height="50", />' % (self.image.url))

    def __str__(self):
        return self.title

####Vendor############
####Vendor############
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcde12345")

    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(upload_to=user_derectory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_derectory_path, default="vendor.jpg")
    description = models.CharField(max_length=200, null=True, blank=True, default=" Hello! i am amazing vendor")

    address = models.CharField(max_length=100, default="159/3/C/1 Main Street")
    contact = models.CharField(max_length=100, default="+800 1955 685500")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="159/3/C/1 Main Street")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True) 

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50", height="50", />' % (self.image.url))

    def __str__(self):
        return self.title
    
#############Tags###############   
#############Tags###############   

class Tags(models.Model):
    pass



    
####Product############
####Product############
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcde12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="product")

    title = models.CharField(max_length=100, default="Fresh product")
    image = models.ImageField(upload_to=user_derectory_path, default="product.jpg")
    description = models.CharField(max_length=200, null=True, blank=True, default="This a good product")

    price = models.DecimalField(max_digits=999999, decimal_places=2, default="2.99")
    old_price = models.DecimalField(max_digits=999999, decimal_places=2, default="3.99")

    specification = models.TextField(null=True, blank=True)
    size = models.CharField(max_length=100, default="L", null=True, blank=True)
    color = models.CharField(max_length=100, default="black", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="10", null=True, blank=True)
    type = models.CharField(max_length=100, default="organic", null=True, blank=True)
    life = models.CharField(max_length=100, default="50 days", null=True, blank=True)
    manufacture = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    product_information = models.TextField(default="its a product information", null=True, blank=True)
    tags = TaggableManager(blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True, blank=True)

    products_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)

    sku = ShortUUIDField(unique=True, length=5, max_length=10, prefix="sku", alphabet="12345")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50", height="50", />' % (self.image.url))

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
####ProductImage############
####ProductImage############
class ProductImage(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")  
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_image")
    date = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name_plural = "Product Images"



####CartOrder############
####CartOrder############
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=999999, decimal_places=2, default="2.99") 
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing") 


    class Meta:
        verbose_name_plural = "Cart Order"


####CartOrderItems############
####CartOrderItems############
class CartOrdrItems(models.Model):
    order = models.ForeignKey( CartOrder, on_delete=models.CASCADE)
    invoice = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2, default="2.99") 
    total = models.DecimalField(max_digits=99999, decimal_places=2, default="2.99")


    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50", height="50", />' % (self.image))
    

######## Product Review, Wislist, Adress#####
######## Product Review, Wislist, Adress#####


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Review"

    

    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlist"

    

    def __str__(self):
        return self.product.title
    


class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
     
    class Meta:
        verbose_name_plural = "Address" 