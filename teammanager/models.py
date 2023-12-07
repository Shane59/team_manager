from django.db import models
from django.forms import ModelForm

ROLE_OPTION = [
  ("admin", "Admin"),
  ("regular", "Regular")
]

class Member(models.Model):
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.CharField(max_length=200)
  location = models.CharField(max_length=200)
  role = models.CharField(max_length=8, choices=ROLE_OPTION, default="regular")
  def __str__(self):
    return self.first_name + " " + self.last_name + " "
  def isAdmin(self):
    return self.role == "admin"
  
class MemberForm(ModelForm):
  class Meta:
      model = Member
      fields = "__all__"