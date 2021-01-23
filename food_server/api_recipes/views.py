from .models import Recipe, UserProfile, Product, Ingredient, userprofile_recipe
from .serializers import *
from django.db import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from drf_multiple_model.views import ObjectMultipleModelAPIView, FlatMultipleModelAPIView

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        return self.list(request)

class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get(self, request):
        return self.list(request)

class RecipeStepViewSet(viewsets.ModelViewSet):
    serializer_class = Recipe_StepSerializer
    queryset = RecipeStep.objects.all()

    def get(self, request):
        return self.list(request)

class UserProfile_RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfile_RecipeSerializer
    queryset = userprofile_recipe.objects.all()

    def get(self, request):
        return self.list(request)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class FullIngredientAPIView(FlatMultipleModelAPIView):
    # add_model_type = False
    querylist = [
        {'queryset': Ingredient.objects.all(), 'serializer_class': IngredientSerializer},
        {'queryset': Product.objects.all(), 'serializer_class': ProductSerializer},
    ]