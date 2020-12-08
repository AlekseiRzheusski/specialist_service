from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class City(models.Model):
    """Model representing city"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Model representing enhanced user"""
    phone = models.CharField(max_length=20,null=True)
    street = models.CharField(max_length=50, help_text='Введите адрес места работы', null=True)
    house = models.IntegerField(null=True)
    latitude = models.FloatField(null=True)
    longtitude = models.FloatField(null=True)
    profile_pic = models.ImageField(null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Specialty(models.Model):
    """Model representing specialty"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Specialist(models.Model):
    """Model representing information about specialist that extends user"""
    person = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    works_at_home = models.BooleanField()


    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'


class Comment(models.Model):
    """Model representing comments by users"""
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000,help_text="Введите комментарий")

    
