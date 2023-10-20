
from django.contrib import admin
from django.urls import path, include
from inventory import views
from rest_framework_nested import routers
from dj_rest_auth.views import LoginView, PasswordResetConfirmView, PasswordChangeView, PasswordResetView
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from social_auth.views import GoogleLoginView


router = routers.DefaultRouter()
router.register('api/products', views.Products,)
router.register('api/category', views.Category)
router.register('api/inventory', views.ProductInventory)
router.register('api/brand', views.Brand)
router.register('api/review', views.ReviewView)
router.register('api/wishlist', views.WishlistView)
router.register('api/cart', views.CartView)
router.register('api/order', views.OrderView)
router.register('api/user', views.UserView)

# ? NESTED ROUTES
cart_router = routers.NestedSimpleRouter(
    router, 'api/cart', lookup='cart')  # parent
cart_router.register('items', views.CartItemView,
                     basename='cart-items')  # child/nested

product_router = routers.NestedSimpleRouter(
    router, 'api/products', lookup='product')
product_router.register('reviews', views.ReviewView, basename='reviews')

order_router = routers.NestedSimpleRouter(router, 'api/order', lookup='order')
order_router.register('items', views.OrderItemView, basename='order-items')

user_router = routers.NestedSimpleRouter(router, 'api/user', lookup='user_pk')
user_router.register('address', views.ShippingAddressView,
                     basename='user-address')

wishlist_router = routers.NestedSimpleRouter(
    router, 'api/wishlist', lookup='wishlist')
wishlist_router.register(
    'items', views.WishlistItemView, basename='wishlist_items')

schema_view = get_schema_view(
    openapi.Info(
        title="H&K E-COMMERCE API",
        default_version='v1',
        description="Full E-commerce API for H&K E-commerce website",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("api/admin/", admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('api/auth/register/', include('dj_rest_auth.registration.urls')),
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/send-verify-email/', ResendEmailVerificationView.as_view()),
    path('api/auth/verify-email/', VerifyEmailView.as_view()),
    path('api/auth/password-change/', PasswordChangeView.as_view()),
    path('api/auth/password-reset/', PasswordResetView.as_view()),
    path('api/auth/password-reset-confirm/',
         PasswordResetConfirmView.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('doc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

]

urlpatterns += router.urls + cart_router.urls + \
    order_router.urls + user_router.urls + product_router.urls + \
    wishlist_router.urls
