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

from django.http import HttpResponse
from django.contrib.auth import get_user_model
def crear_admin_remoto(request):
    try:
        User = get_user_model()
        email_buscar = "admin@catering.com"
        
        if not User.objects.filter(correo=email_buscar).exists():
            # Creamos el superusuario asegurando los campos obligatorios de tu modelo
            User.objects.create_superuser(
                correo=email_buscar,
                password="admincatering", # Django nativo usa 'password' internamente para el hash
                nombre="Leonardo",
                apellido="Lima",
                DNI="42787728",
                is_staff=True,    # Esto es lo que te pide el cartel ("staff account")
                is_superuser=True
            )
            return HttpResponse("<h1>¡Éxito! Superusuario creado correctamente en la nube.</h1>")
        else:
            return HttpResponse("<h1>El usuario admin@catering.com ya existía en la base de datos.</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>Error al crear: {str(e)}</h1>")