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
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        userprofile = UserProfile.objects.all()
        return userprofile

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer_class = UserProfileSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def partial_update(self, request, *args, **kwargs):
        user_object = self.get_object()
        queryset = self.get_queryset()
        data = request.data

        user_object.user_sex = data.get('sex', user_object.user_sex)
        user_object.user_height = data.get('height', user_object.user_height)
        user_object.user_weight = data.get('weight', user_object.user_weight)

        user_object.save()
        serializer_class = UserProfileDetailSerializer(user_object, queryset=queryset)

        return Response(serializer_class.data)

    # def create(self, request, *args, **kwargs):
    #     userprofile_data = request.data
    #
    #     new_userprofile = UserProfile.objects.create(
    #         user_profile=UserProfile.objects.get(
    #             sex=userprofile_data["sex"]),
    #             weight=userprofile_data["weight"],
    #             height=userprofile_data["height"],
    #             email=userprofile_data["email"],
    #             name=userprofile_data["name"],
    #             )
    #
    #     new_userprofile.save()
    #
    #     serializer_class = UserProfileSerializer(new_userprofile)
    #
    #     return Response(serializer_class.data)
    #
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return UserProfileSerializer
    #     if self.action == 'partial_update':
    #         return UserProfileDetailSerializer
    #     return serializers.DefaultSerializer

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

class UserProfile_RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfile_RecipeSerializer
    queryset = userprofile_recipe.objects.all()

    def get(self, request):
        return self.list(request)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES