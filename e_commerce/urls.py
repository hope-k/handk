
from django.contrib import admin
from rest_framework import permissions
from django.urls import path, include, re_path
from inventory import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_nested import routers
from dj_rest_auth.views import LoginView, PasswordResetConfirmView, PasswordChangeView, PasswordResetView
from dj_rest_auth.registration.views import ResendEmailVerificationView, VerifyEmailView, RegisterView


schema_view = get_schema_view(
    openapi.Info(
        title="H&K API",
        default_version='v1',
        description="H&K E-Commerce API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = routers.DefaultRouter()
router.register('api/products', views.Products,)
router.register('api/category', views.Category)
router.register('api/inventory', views.ProductInventory)
router.register('api/brand', views.Brand)
router.register('api/review', views.ReviewView)
router.register('api/cart', views.CartView)
router.register('api/order', views.OrderView)
router.register('api/user', views.UserView)

cart_router = routers.NestedSimpleRouter(router, 'api/cart', lookup='cart')
cart_router.register('items', views.CartItemView, basename='cart-items')

order_router = routers.NestedSimpleRouter(router, 'api/order', lookup='order')
order_router.register('items', views.OrderItemView, basename='order-items')

user_router = routers.NestedSimpleRouter(router, 'api/user', lookup='user')
user_router.register('address', views.ShippingAddressView, basename='user-shipping-address')


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("api/admin/", admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/register/', include('dj_rest_auth.registration.urls')),
    path('api/auth/login/', LoginView.as_view()),
    path('api/auth/send-verify-email/', ResendEmailVerificationView.as_view()),
    path('api/auth/verify-email/', VerifyEmailView.as_view()),
    path('api/auth/password-change/', PasswordChangeView.as_view()),
    path('api/auth/password-reset/', PasswordResetView.as_view()),
    path('api/auth/password-reset-confirm/',
         PasswordResetConfirmView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'
            ),
    re_path(r'^api/swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0),
            name='schema-swagger-ui'
            ),
    re_path(r'^api/doc/$', schema_view.with_ui('redoc',
            cache_timeout=0),
            name='schema-redoc'
            ),
]

urlpatterns += router.urls + cart_router.urls + order_router.urls + user_router.urls
