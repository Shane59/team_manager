from django.db import models

# Create your models here.

class Member(models.Model):
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  location = models.CharField(max_length=200)
  is_admin = models.BooleanField(default=False)
  def __str__(self):
    return self.first_name + " " + self.last_name + " " + str(self.is_admin)
  def isAdmin(self):
    return self.is_admin