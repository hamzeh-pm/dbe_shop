from .cart import Cart


def cart(request):
    return {"cart_obj": Cart(request)}
