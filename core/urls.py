from django.urls import path

from .views import (
    PizzaDetailView,
    CheckoutView,
    IndexView,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    remove_single_pizza_from_cart,
    add_single_pizza_to_cart,
    PickupView,
    DeliveryView,
    reset_cart_delivery,
    order_tracker,
    reset_cart_pickup
)
app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('order-summary/', OrderSummaryView.as_view(), name="order-summary"),
    path('pizza/<slug>/', PizzaDetailView.as_view(), name="pizzas"),
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"),
    path('remove-single-pizza-from-cart/<slug>/',
         remove_single_pizza_from_cart, name="remove-single-pizza-from-cart"),
    path('add-single-pizza-to-cart/<slug>/',
         add_single_pizza_to_cart, name="add-single-pizza-to-cart"),
    path('transaction/pickup/', PickupView.as_view(),
         name="pickup"),
    path('transaction/delivery/', DeliveryView.as_view(),
         name="delivery"),
    path('reset-cart-delivery', reset_cart_delivery, name="reset-cart-delivery"),
    path('reset-cart-pickup', reset_cart_pickup, name="reset-cart-pickup"),
    path('order-tracker', order_tracker, name="order-tracker"),
]
