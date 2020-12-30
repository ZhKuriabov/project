from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profile."""

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given details."""

        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Represents a "user profile" inside out system. Stores all user account
    related data, such as 'email address' and 'name'.
    """
    SEX_TYPES = (
        (1, "Male"),
        (2, "Female"),
    )
    sex = models.IntegerField(choices=SEX_TYPES, null=True)
    height = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)], null=True)
    weight = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)], null=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Django uses this when it needs to get the user's full name."""

        return self.name

    def get_short_name(self):
        """Django uses this when it needs to get the users abbreviated name."""

        return self.name

    def __str__(self):
        """Django uses this when it needs to convert the object to text."""

        return self.email

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image_link_small = models.CharField(max_length=100, null=True)
    image_link_big = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=100)
    portions = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    preparing_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    cooking_time = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    difficulty = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

class Product(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)], null=True)
    calories = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)])
    carbs = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)])
    fat = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)])
    protein = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)])
    price = models.FloatField(default=0.0, max_length=100, validators=[MinValueValidator(0.0)], null=True)
    recipe = models.ManyToManyField(Recipe)

class userprofile_recipe(models.Model):
    profile_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="list of profiles",)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField(default=0.0, max_length=5, validators=[MinValueValidator(0.0)])
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class RecipeStep(models.Model):
    step = models.CharField(max_length=10000)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)