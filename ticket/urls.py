from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import MaintenanceRequest_ViewSet, Assignament_ViewSet
from comment.views import Comment_ViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'maintenance_requests', MaintenanceRequest_ViewSet)
router.register(r'assignaments', Assignament_ViewSet)
router.register(r'comments', Comment_ViewSet)

urlpatterns = [
    path('', views.List_Maitenance_Requests, name="listar_solicitudes"),                            #Listo
    path('crear/', views.Maintenance_Request_FormView, name='crear_solicitudes'),                   #Listo

    path('detalle/<int:id>', views.detail_request, name='detalle_solicitud'),                       #Listo
    path('asignar/<int:id>', views.Assign_Maintenance_Request_FormView, name='asignar_solicitud'),  #Listo

    path('', include(router.urls)),
    path('cantidad/', views.maintenance_request_count),

    # path('api/auth/', include('dj_rest_auth.urls')),
    # path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]