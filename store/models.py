from django.db import models
from django.db.models.fields.related import ForeignKey


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # When you delete a collection, you dont delete product (PROTECTED)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # many to many relationship
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BROZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIPS = [
        (MEMBERSHIP_BROZE, 'Bronze'),
        (MEMBERSHIP_BROZE, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIPS, default=MEMBERSHIP_BROZE)


class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_COMPLETE = 'C'
    STATUS_FAILED = 'F'
    STATUS = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
        (STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=STATUS, default=STATUS_PENDING)
    # When you delete a customer you should not delete order too (PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = ForeignKey(Cart, on_delete=models.CASCADE)
    product = ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
