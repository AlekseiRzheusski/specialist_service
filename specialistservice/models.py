from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .decorators import path_and_rename
# Create your models here.


class City(models.Model):
    """Model representing city"""
    name = models.CharField(max_length=20, primary_key=True)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Model representing enhanced user"""
    phone = models.CharField(max_length=20, null=True)
    street = models.CharField(
        max_length=50, help_text='Введите адрес места работы', null=True)
    house = models.IntegerField(null=True)
    latitude = models.FloatField(null=True)
    longtitude = models.FloatField(null=True)
    profile_pic = models.ImageField(
        default="default-user-image.png", null=True, upload_to=path_and_rename)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Specialty(models.Model):
    """Model representing specialty"""
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "specialties"

    def __str__(self):
        return self.name


class Specialist(models.Model):
    """Model representing information about specialist that extends user"""
    person = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, null=True)
    departure_to_client = models.BooleanField(null=True)
    about = models.TextField(max_length=1000, null=True)

    class Meta:
        permissions = (('can_update_specialist_info', 'Set new specialist info'),
                       ('can_become_specialist', 'Can become specialist'))

    def __str__(self):
        return f'{self.person.first_name} {self.person.last_name}'

    def get_absolute_url(self):
        return reverse('specialist-detail', args=[str(self.id)])


class Comment(models.Model):
    """Model representing comments by users"""
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(
        max_length=1000, help_text="Введите комментарий")

    def __str__(self):
        return f'{self.user.username} {self.specialist.person.username}'


class Request(models.Model):
    """Model representing request to work to specialist"""
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PrivateRoom(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='creator_of_room', related_query_name='creators_of_rooms')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100, unique=True)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    private_room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Notification(models.Model):
    Message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
