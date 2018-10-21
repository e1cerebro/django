from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    portfolio_site = models.URLField(blank=True)
    profile_pics = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


# Create your models here.
class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)

    def __str__(self):
        return self.top_name


class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class AccessRecord(models.Model):
    name = models.ForeignKey(Webpage, on_delete=models.PROTECT)
    date = models.DateField()

    def __str__(self):
        return str(self.date)

