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
]
