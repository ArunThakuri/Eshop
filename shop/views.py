from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from cms.models import Menu, TopBanner, BottomBanner
from shop.form import ReviewForm, CartForm
from shop.models import Category, Product

# Create your views here.
from shop.serializers import CategorySerializer


class BaseView(View):
    template_context = {
        'menus': Menu.objects.order_by('-weight'),
        'categories': Category.objects.all(),
    }

    def get_context_data(self, param, param1):
        pass


class HomePage(BaseView):

    def get(self, request):
        self.template_context['top_banners'] = TopBanner.objects.all()
        self.template_context['big_bottom_banner'] = BottomBanner.objects.filter(is_big=True).first()
        self.template_context['small_bottom_banners'] = BottomBanner.objects.filter(is_big=False)[:2]
        self.template_context['deals_products'] = Product.objects.filter(deal_of_the_day=True)
        self.template_context['latest_products'] = Product.objects.order_by('-pub_date')[:8]
        self.template_context['picked_products'] = Product.objects.order_by('?')[:4]
        self.template_context['all_products'] = Product.objects.all()[:9]

        return render(request, 'index.html', self.template_context)


class ProductView(BaseView):
    def get(self, request, product_id, review_form=None):
        self.template_context['review_form'] = review_form if review_form else ReviewForm()
        self.template_context['product'] = Product.objects.get(pk=product_id)
        return render(request, 'single_product_page.html', self.template_context)

    def post(self, request, product_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = Product.objects.get(pk=product_id)
            review.save()
            return redirect(reverse('single_product_page', args=[product_id]))

        return self.get(request, product_id, form)


class CartView(BaseView):
    def post(self, request, product_id):
        form = CartForm(request.POST)
        cart = form.save(commit=False)
        cart.user = request.user
        cart.product = Product.objects.get(pk=product_id)
        cart.save()
        return redirect(reverse('single_product_page', args=[product_id]))


class ProductsView(BaseView):
    def get(self, request):
        self.template_context['product'] = Product.objects.all()
        return render(request, 'products.html', self.template_context)


class CategoryView(BaseView):
    def get(self, request, category_id):
        self.template_context['category'] = Category.objects.get(pk=category_id)
        return render(request, 'products.html', self.template_context)


class SearchView(BaseView):
    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        print(request.get)
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.none()


class CategoryApi(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
