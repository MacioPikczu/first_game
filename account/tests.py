from django.test import TestCase
from .models import User

# Create your tests here.

all_users = User.objects.all()
print(all_users)
print(all_users[0].email)

