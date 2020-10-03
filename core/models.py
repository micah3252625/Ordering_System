from django.conf import settings
from django.db import models
from django.shortcuts import reverse
CATEGORY_CHOICES = (
    ('Pizzalet', 'Pizzalet'),
    ('Pizza', 'Pizza'),
)
LABEL_CHOICES = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('danger', 'danger'),
)
SIZE_CHOICES = (
    (8, 8),
    (10, 10),
    (12, 12),
)
ORDER_STATUS = (
    ('Order Submitted', 'Order Submitted'),
    ('Order Processing', 'Order Processing'),
    ('Order Preparing', 'Order Preparing'),
    ('Order on its way', 'Order on its way'),
)


class Pizza(models.Model):
    title = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    category = models.CharField(
        choices=CATEGORY_CHOICES, max_length=10, default="Pizza")
    label = models.CharField(choices=LABEL_CHOICES,
                             max_length=10, default="primary")
    size = models.IntegerField(choices=SIZE_CHOICES, default=8, null=True)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:pizzas", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_pizza_size_price(self):
        if self.pizza.size == 10:
            return self.pizza.price + 60
        elif self.pizza.size == 12:
            return self.pizza.price + (60 * 2)
        else:
            return self.pizza.price


class OrderPizza(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.pizza.title}"

    def get_total_pizza_price(self):
        return self.quantity * self.pizza.price

    def get_final_price(self):
        return self.get_total_pizza_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    pizzas = models.ManyToManyField(OrderPizza)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    order_status = models.CharField(choices=ORDER_STATUS,
                                    max_length=100, default="Order Submitted")

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for pizza_item in self.pizzas.all():
            total += pizza_item.get_final_price()
        return total

    def get_delivery_fee(self):
        return 50
    # for delivery

    def get_total_add_delivery_fee(self):
        return self.get_total() + self.get_delivery_fee()


class OrderDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    street = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    text = models.TextField(max_length=250, blank=True, null=True)
    money = models.FloatField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " | " + self.user.username + " Adress: " + self.street + ", " + self.barangay
