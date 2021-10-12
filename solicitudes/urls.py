from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

"""
router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
router.register('cotizaciones', EcoSolicitudCotizacionViewSet, basename='cotizaciones')
"""

urlpatterns = [
    #path('cotizaciones', EcoSolicitudCotizacionViewSet, name='cotizaciones'),

 
]