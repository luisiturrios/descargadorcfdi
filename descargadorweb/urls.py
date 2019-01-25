from django.urls import path

from . import views

app_name = 'descargadorweb'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('caracteristicas/', views.CaracteristicasView.as_view(), name='caracteristicas'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('contacto-completo/', views.ContactoCompletoView.as_view(), name='contacto_completo'),

    path('empresas/', views.EmpresasView.as_view(), name='empresas'),
    path('empresas/crear/', views.EmpresasCrearView.as_view(), name='empresas_crear'),
    path('empresas/<int:pk>/', views.EmpresasDetalleView.as_view(), name='empresas_detalle'),
    path(
        'empresas/<int:empresa_pk>/solicitud-descarga/crear/',
        views.SolicitudDeDescargaCrearView.as_view(),
        name='solicitud_de_descarga_crear'
    ),
    path(
        'empresas/<int:empresa_pk>/solicitud-descarga/<int:pk>/',
        views.SolicitudDeDescargaDetalleView.as_view(),
        name='solicitud_de_descarga_detalle'
    ),
    path(
        'empresas/<int:empresa_pk>/solicitud-descarga/<int:pk>/verificar/',
        views.SolicitudDeDescargaVerificarView.as_view(),
        name='solicitud_de_descarga_verificar'
    ),
]
