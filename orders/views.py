import weasyprint
from cart.cart import Cart
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from orders.models import Order, OrderItem

from .forms import OrderCreateForm


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.coupon = cart.coupon
            order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            return render(request, "orders/order/created.html", {"order": order})

    else:
        form = OrderCreateForm()

    return render(request, "orders/order/checkout.html", {"cart": cart, "form": form})


def order_to_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/order/pdf.html", {"order": order})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "filename=recite.pdf"
    weasyprint.HTML(string=html).write_pdf(response)
    return response
