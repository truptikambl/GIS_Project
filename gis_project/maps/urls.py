from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# DRF Router: for automatic API endpoints like /api/states/, etc.
router = DefaultRouter()
router.register('states', views.StateViewSet, basename='state')
router.register('districts', views.DistrictViewSet, basename='district')
router.register('talukas', views.TalukaViewSet, basename='taluka')
router.register('villages', views.VillageViewSet, basename='village')

urlpatterns = [
    # 1. Root map view
    path('', views.map_view, name='map'),

    # 2. API endpoints (used in dropdowns)
    path('api/', include(router.urls)),

    # 3. Village-specific info for popup (e.g., name, population, pincode)
    path('api/village-data/<int:pk>/', views.village_data, name='village-data'),

    # 4. GeoJSON highlight endpoints for state, district, taluka, village
    path('geojson/<str:level>/<int:id>/', views.get_geojson, name='get_geojson'),
]
