from django.db import models


# Non-model class for testing
class NonModelClass:
    def __init__(self, name):
        self.name = name


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BuyableType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Buyable(TimeStampMixin):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(BuyableType, on_delete=models.CASCADE)


class Property(models.Model):
    address = models.CharField(max_length=255)
    owner = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=15, decimal_places=2)


# Another non-model class for testing
class UtilityClass:
    def utility_method(self):
        return "This is a utility method"
