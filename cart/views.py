from coupons.forms import CouponApplyForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product

from .cart import Cart
from .forms import CartAddProduct


# Create your views here.
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProduct(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd["quantity"], cd["override"])

    return redirect("cart:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    coupon_form = CouponApplyForm()
    for item in cart:
        item["update_quantity_form"] = CartAddProduct(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(
        request, "cart/detail.html", {"cart": cart, "coupon_form": coupon_form}
    )
