from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from datetime import datetime


ITEM_TYPE = (
    (1, 'tool'),
    (2, 'resource'),
)

TOOL = (
    (1, 'wood_pickaxe'),
    (2, 'wood_axe'),
    (3, 'metal_pickaxe'),
    (4, 'metal_axe'),
    (5, 'flint'),
    (6, 'stone_tool')
)

RESOURCE = (
    (1, 'wood'),
    (2, 'stone_ore'),
    (3, 'metal_ore'),
    (4, 'sulfur_ore'),
    (5, 'metal_frags'),
    (6, 'sulfur'),
    (7, 'charcoal')

)

STATISTICS = (
    (1, 'digging'),
    (2, 'chopping')
)

class UserManager(UserManager): #usermanager
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permission_set',
        blank=True
    )

    def __str__(self):
        return self.username

# class SuperUserManager(UserManager):
#     email = models.EmailField()
#
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='superuser_groups',
#         blank=True
#     )
#
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='superuser_permission_set',
#         blank=True
#     )
#
#     def __str__(self):
#         return self.username


class User(AbstractUser):
    object = UserManager()
    first_name = None
    last_name = None

    def __str__(self):
        return self.username

# class SuperUser(AbstractUser):
#     object = SuperUserManager()
#     first_name = None
#     last_name = None


class Equipment(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tool(models.Model):
    name = models.CharField(max_length=32)
    experience = models.IntegerField(default=0)
    lvl = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Resource(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Statistics(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# class Blueprints(models.Model):
#     name = models.CharField(max_length=32)
#     item_needed = models.CharField(max_length=32)
#     quantity = models.IntegerField(default=0)
#
# class Planner(models.Model):
#     item_created_name = models.CharField(max_length=32)
#     time_needed = models.IntegerField(default=0)
#     time_start = models.DateField(default=datetime.now)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)