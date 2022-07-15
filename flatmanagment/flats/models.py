from django.db import models

# Create your models here.


class BuildingCompany(models.Model):
    name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='media/')
    descr = models.TextField()

    def __str__(self):
        return self.name


class Apartment(models.Model):
    name = models.CharField(max_length=50)
    builder = models.ForeignKey(BuildingCompany, related_name='apartments', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/', null=True)
    descr = models.TextField()

    def __str__(self):
        return self.name


class House(models.Model):
    name = models.CharField(max_length=30)
    apartment = models.ForeignKey(Apartment, related_name='houses', on_delete=models.SET_NULL, null=True)
    descr = models.TextField()

    def __str__(self):
        return self.name


class Entrance(models.Model):
    number = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class FlatType(models.Model):
    rooms = models.IntegerField()
    square = models.FloatField()
    descr = models.TextField()
    schema = models.ImageField(upload_to='schemas/')
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Placement(models.Model):
    number = models.IntegerField()
    floor = models.IntegerField()
    owner_id = models.BigIntegerField(null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)


class Flat(Placement):
    type = models.ForeignKey(FlatType, on_delete=models.PROTECT)
    entrance = models.ForeignKey(Entrance, on_delete=models.CASCADE)

    def __str__(self):
        return f'Квартира №{self.number}'


class Commercial(Placement):
    square = models.FloatField()
    descr = models.TextField()

    def __str__(self):
        return f'Нежилое помещение №{self.number}'


class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    performer_id = models.BigIntegerField()
    price = models.BigIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.service_type


class DealStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Basket(models.Model):
    user_id = models.IntegerField()


class Deal(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    status = models.ForeignKey(DealStatus, on_delete=models.SET_NULL, null=True)
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, null=True)
    dt = models.DateTimeField()
