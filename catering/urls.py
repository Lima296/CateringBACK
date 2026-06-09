from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from usuarios.views import UsuarioViewSet
from ingredientes.views import IngredienteViewSet
from recetas.views import RecetaViewSet
from ventas.views import VentaViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'ingredientes', IngredienteViewSet)
router.register(r'recetas', RecetaViewSet, basename='recetas')
router.register(r'ventas', VentaViewSet, basename='ventas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Auth
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.contrib.auth import get_user_model
try:
    User = get_user_model()
    # Cambiá estos datos por los que vos quieras usar
    if not User.objects.filter(correo="admin@catering.com").exists():
        User.objects.create_superuser(
            correo="admin@catering.com",
            contraseña="ContraseñaSegura123",
            nombre="Admin",
            apellido="General",
            DNI="12345678"
        )
        print("✓ Superusuario creado con éxito en producción")
except Exception as e:
    pass
