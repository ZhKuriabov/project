from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

# router.register('car-specs', CarSpecsViewset, basename='car-specs')
router = DefaultRouter()
router.register('user-profile', views.UserProfileViewSet, basename='user-profile')
# router.register('user-profile/<int:pk>', views.UserProfileViewSet()({'get': 'partial_update'}))
# router.register('recipe', views.RecipeViewSet)
# router.register('product', views.ProductViewSet)
# router.register('ingredient', views.IngredientViewSet)
# router.register('profile-recipe', views.UserProfile_RecipeViewSet)

# urlpatterns = format_suffix_patterns([
#     path('user-profile/', views.UserProfileViewSet.as_view({'get': 'list'})),
#     path('user-profile/<int:pk>/', views.UserProfileViewSet.as_view({'put': 'update'})),
# ])

urlpatterns = [
    path('', include(router.urls))
]

# urlpatterns = [
#     # path('generic/userprofile/<int:pk>', UserProfileDetail.as_view()),
#     # path('', include(router.urls)),
#     path('login/', views.UserLoginApiView.as_view()),
# ]
