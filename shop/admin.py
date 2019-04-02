# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, ProductHasImage


class ProductHasImageInline(admin.TabularInline):
    model = ProductHasImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductHasImageInline,
    ]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
