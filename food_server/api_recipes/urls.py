from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user-profile', views.UserProfileViewSet, basename='user-profile')
router.register('recipe', views.RecipeViewSet)
router.register('product', views.ProductViewSet)
router.register('ingredient', views.IngredientViewSet)
router.register('profile-recipe', views.UserProfile_RecipeViewSet)
router.register('recipe_step', views.RecipeStepViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view()),
    path('fullinfo/', views.FullIngredientAPIView.as_view())
]