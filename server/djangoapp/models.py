from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, default='unknown')
    description = models.TextField(null=False)
    def __str__(self):
        return f"{self.name}: {self.description}"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=40, default='unknown')
    dealer_id = models.IntegerField(default=0)
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    year = models.DateField('Year')
    type = models.CharField(null=False, max_length=20,
                            choices=[
                                ('Hatch','hatch'),
                                ('Sedan','sedan'),
                                ('SUV','suv'),
                                ('WAGON','wagon')
                            ], default="Hatch")
    def __str__(self):
        return f"Name: {self.name}, Make: {self.make}, Year: {self.year}, Type: {self.type}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
