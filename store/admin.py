from django.contrib import admin
from .models import Category, Product, Gallery, Size, Specification, Color, Cart,CartOrder, CartOrderItem, Wishlist, Notification, Review

class ProductImagesAdmin(admin.TabularInline):
    model = Gallery

class SpecificationAdmin(admin.TabularInline):
    model = Specification

class ColorAdmin(admin.TabularInline):
    model = Color

class SizeAdmin(admin.TabularInline):
    model = Size

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, SpecificationAdmin, ColorAdmin, SizeAdmin]
    search_fields = ['title', 'price', 'slug']
    list_filter = ['featured', 'status', 'in_stock', 'vendor']
    list_editable = [ 'price', 'featured', 'status',  'shipping_amount',  ]
    list_display =  ['title', 'image',   'price', 'featured', 'shipping_amount', 'in_stock' ,'stock_qty','status' ]
    # actions = [make_published, make_in_review, make_featured]
    list_per_page = 100
    prepopulated_fields = {"slug": ("title", )}
    # form = ProductAdminForm




admin.site.register(Category,)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
# Register your models here.
