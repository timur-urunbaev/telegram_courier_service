from django.db import models

# Create your models here.
class Product(models.Model):
    '''
    The Product object contains information about product

    Attributes
    ----------
    name : str
        [required] store the name of the product e.g. pen, pencil and so on.
    description : str
        [required] store the descripstion of the product.
    
    Methods
    -------
    __str__(self)
        Represent an object as a string
    '''
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    brand = models.CharField(max_length=256)

    def __str__(self):
        return f'NAME: {self.name}, BRAND: {self.brand}'


class ProductSet(models.Model):
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return f'Product {self.product.name}, quantity:{self.quantity}'


class Branch(models.Model):
    '''
    The Branch object contains information about a branch

    Attributes
    ----------
    branch_name : str
        [required] store the name of the branch from where the order should be taken.
    address : str
        [required] store the address of the branch from where the order should be taken.
    address_link : str
        [required] store the url of the branch from where the order should be taken (YandexMaps).
    
    Methods
    -------
    __str__(self)
        Represent an object as a string
    '''
    branch_name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    address_link = models.URLField(blank=False)

    def __str__(self):
        return f'BRANCH: {self.branch_name}\nADDRESS: {self.address}'


class Courier(models.Model):
    '''
    The Courier object contains information about courier
    
    Attributes
    ----------
    telegram_id : str
        [required] store a Telegram ID of the courier.
    first_name : str
        [required] store the first name of the courier.
    last_name : str, optional
        store the last name of the courier.
    preferred_language : str
        [required] store the preferred language of the courier.
    phone_number : str
        [required] store the phone number of the courier.
    
    Methods
    -------
    __str__(self)
        Represent an object as a string
    '''
    telegram_id = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    LANGUAGE_CHOICES = (
        ('ru', 'Russian Language'),
        ('uz', 'Uzbek Language')
    )
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ru', blank=False)
    

    def __str__(self):
        return f'TELEGRAM ID: {self.telegram_id}, FIRST NAME: {self.first_name}'


class Order(models.Model):
    '''
    The Order object contains information about an Order

    Attributes
    ----------
    id: int
        [required] Primary Key
    username: str
        Name of User who ordered Items, needed for calling 
    userphone: str
        Phone number of User who ordered Items, needed for calling
    products: many to many
        products
    branch
        [required] Branch from where courier should take the order from.
    courier : Courier, optional
        [optional] Courier who will responsible for delivery.
    price: float
        the total price for delivery
    address : str
        [required] store the address order, should be ordered to,
    active : bool
        [read-only] store the state of the order

    Methods
    -------
    __str__(self)
        Represent an object as a string
    '''
    id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    userphone = models.CharField(max_length=15)
    products = models.ManyToManyField(ProductSet)
    courier = models.ForeignKey(Courier, null=True, on_delete=models.SET_NULL, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=1)
    address = models.CharField(max_length=500)
    active = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return f'ID: {self.pk}, ACTIVE: {self.active}, COURIER: {self.courier.__str__()}'