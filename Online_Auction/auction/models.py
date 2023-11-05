from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.core.exceptions import ValidationError
from datetime import datetime


def validate_future_datetime(value):
    """
    Validator function to ensure that the datetime value is in the future.
    """
    if value <= datetime.now():
        raise ValidationError(
            _('%(value)s is not a future date and time.'),
            params={'value': value},
        )


class Member_fee(models.Model):
    fee = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.fee


class Bidder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Auction_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=10, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name + " " + self.category.name


class Session_date(models.Model):
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.date


class Session_Time(models.Model):
    date = models.ForeignKey(Session_date, on_delete=models.CASCADE, null=True)
    time = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.date.date + " " + self.time


class Status(models.Model):
    status = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.status


class Product(models.Model):
    # temp = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=True)
    min_price = models.IntegerField(null=True)
    images = models.FileField(null=True)
    session = models.DateTimeField(validators=[validate_future_datetime])
    category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Aucted_Product(models.Model):
    winner = models.ForeignKey(Bidder, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Auction_User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.user.username + " " + self.product.name


class Result(models.Model):
    result = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.result


class Payment(models.Model):
    pay = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.pay


class Participant(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    new_price = models.IntegerField(null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Bidder, on_delete=models.CASCADE, null=True)
    aucted_product = models.ForeignKey(Aucted_Product, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user) + str(self.product)


class Send_Feedback(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.profile.username


class Order(models.Model):
    name = models.CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
