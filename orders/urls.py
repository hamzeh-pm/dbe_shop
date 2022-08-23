from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.order_create, name="order_create"),
    path("pdf/<int:order_id>/", views.order_to_pdf, name="order_pdf"),
]
