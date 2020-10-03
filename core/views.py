
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import *
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm
# Create your views here.


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'order': order,
            'form': form,
        }
        return render(self.request, "checkout-page.html", context)

    def post(self, *args, **kwargs):

        try:
            form = CheckoutForm(self.request.POST or None)
            order = Order.objects.get(
                order_status='Order Submitted', user=self.request.user, is_ordered=False)
            print(self.request.POST)

            if self.request.method == "POST":
                if form.is_valid():
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    contact = form.cleaned_data.get('contact')
                    street = form.cleaned_data.get('street')
                    barangay = form.cleaned_data.get('barangay')
                    text = form.cleaned_data.get('text')
                    transaction = form.cleaned_data.get('transaction')
                    money = form.cleaned_data.get('money')

                    order_detail = OrderDetail(
                        user=self.request.user,
                        first_name=first_name,
                        last_name=last_name,
                        contact=contact,
                        street=street,
                        barangay=barangay,
                        text=text,
                        order=order,
                        money=float(money),
                    )

                    order.order_detail = order_detail

                    if float(money) >= order.get_total():
                        order_detail.save()
                        order.save()
                        messages.success(
                            self.request, "Your order was Successful!")
                        return redirect("core:index")
                    else:
                        messages.error(
                            self.request, "Invalid money amount!")
                        return redirect("core:checkout")

                    messages.success(
                        self.request, "Your order was Successful!")
                    return redirect("core:index")

                else:
                    print("FORM IS NOT VALID")
                    messages.warning(self.request, "Failed to Checkout!")
                    return redirect("core:checkout")
            else:
                print("FORM ERROR")
                messages.warning(self.request, "Failed to Checkout!")
                return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order!")
            return redirect("core:order-summary")
        return redirect("core:")


class PickupView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'order': order,
        }
        return render(self.request, "pickup.html", context)


class DeliveryView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, is_ordered=False)
        context = {
            'order': order,
        }
        return render(self.request, "delivery.html", context)


class IndexView(ListView):
    model = Pizza
    paginate_by = 9
    template_name = "home.html"


@method_decorator(login_required, name='dispatch')
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, is_ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order!")
            return redirect("/")


class PizzaDetailView(DetailView):
    model = Pizza
    template_name = "pizzas.html"


@login_required
def add_to_cart(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    pizza_item, created = OrderPizza.objects.get_or_create(
        pizza=pizza,
        user=request.user,
        is_ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if order item it is in the order
        if order.pizzas.filter(pizza__slug=pizza.slug).exists():
            pizza_item.quantity += 1
            pizza_item.save()
            messages.success(request, "This item quantity was updated.")
            return redirect("core:pizzas", slug=slug)
        else:
            messages.success(request, "This item added to cart.")
            order.pizzas.add(pizza_item)
            return redirect("core:pizzas", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.pizzas.add(pizza_item)
        messages.success(request, "This item added to cart.")
        return redirect("core:pizzas", slug=slug)


def reset_cart_delivery(request):
    order = Order.objects.all()
    order.delete()
    messages.success(
        request, "You order was Successful!, We'll notify you if your order is on its way")
    return redirect("core:index")


def reset_cart_pickup(request):
    order = Order.objects.all()
    order.delete()
    messages.success(
        request, "You order was Successful! We'll notify you if your order is ready to pickup")
    return redirect("core:index")


@login_required
def remove_from_cart(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.pizzas.filter(pizza__slug=pizza.slug).exists():
            pizza_item = OrderPizza.objects.filter(
                pizza=pizza,
                user=request.user,
                is_ordered=False
            )[0]
            order.pizzas.remove(pizza_item)
            pizza_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")

    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:pizzas", slug=slug)


@login_required
def remove_single_pizza_from_cart(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        is_ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.pizzas.filter(pizza__slug=pizza.slug).exists():
            pizza_item = OrderPizza.objects.filter(
                pizza=pizza,
                user=request.user,
                is_ordered=False
            )[0]
            if pizza_item.quantity > 1:
                pizza_item.quantity -= 1
                pizza_item.save()
            else:
                order.pizzas.remove(pizza_item)

            messages.info(
                request, "This item quantity was updated from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:pizzas")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:pizzas")


def add_single_pizza_to_cart(request, slug):
    pizza = get_object_or_404(Pizza, slug=slug)
    pizza_item, created = OrderPizza.objects.get_or_create(
        pizza=pizza,
        user=request.user,
        is_ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if order item it is in the order
        if order.pizzas.filter(pizza__slug=pizza.slug).exists():
            pizza_item.quantity += 1
            pizza_item.save()
            messages.success(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.success(request, "This item added to cart.")
            order.pizzas.add(pizza_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.pizzas.add(pizza_item)
        messages.success(request, "This item added to cart.")
        return redirect("core:order-summary")


def order_tracker(request):
    return render(request, "pizza-tracker.html")
