from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default=' ')
    description = models.TextField(max_length=100, default=' ')

    # Create a toString method for object string representation
    def __str__(self):
        return self.name



# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(null=False, max_length=100, default=' ')
   
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    MINIVAN = 'Minivan'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (MINIVAN, 'Minivan')
    ]

    type = models.CharField(
        null=False,
        max_length=50,
        choices=CAR_TYPES,
        default=SEDAN
    )
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, id, lat, long, st, zip, full_name, short_name):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city

        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long

        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

        # Full name
        self.full_name = full_name

        self.short_name = short_name

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"{self.name}'s Review for {self.dealership} ({self.car_make} {self.car_model} {self.car_year})"