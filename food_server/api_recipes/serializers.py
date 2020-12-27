from rest_framework import serializers
from .models import Recipe, UserProfile, Product, Ingredient, userprofile_recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new user."""
        user = UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

# class UserProfileDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['sex', 'height', 'weight']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

class UserProfile_RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = userprofile_recipe
        fields = '__all__'
