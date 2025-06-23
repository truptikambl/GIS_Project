# maps/views.py

import json
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform

from .models import State, District, Taluka, Village, Mahamarg
from .serializers import (
    StateSerializer,
    DistrictSerializer,
    TalukaSerializer,
    VillageSerializer,
    VillageDataSerializer
)


def map_view(request):
    return render(request, 'maps/map.html')


# ——— ViewSets for dropdowns ———

class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        state_id = self.request.query_params.get('state')
        return District.objects.filter(state_id=state_id) if state_id else District.objects.none()


class TalukaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TalukaSerializer

    def get_queryset(self):
        district_id = self.request.query_params.get('district')
        return Taluka.objects.filter(district_id=district_id) if district_id else Taluka.objects.none()


class VillageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VillageSerializer

    def get_queryset(self):
        taluka_id = self.request.query_params.get('taluka')
        return Village.objects.filter(taluka_id=taluka_id) if taluka_id else Village.objects.none()


# ——— GeoJSON endpoint for polygon highlighting ———

def get_geojson(request, level, id):
    model_map = {
        'state': State,
        'district': District,
        'taluka': Taluka,
        'village': Village,
    }
    Model = model_map.get(level)
    if not Model:
        return JsonResponse({'error': 'Invalid level'}, status=400)

    # Fetch the object
    obj = get_object_or_404(Model, pk=id)
    # Reproject to 4326 in‑query if needed:
    geom_4326 = obj.geom
    if obj.geom.srid != 4326:
        # Use GEOS to clone and transform
        geom_4326 = GEOSGeometry(obj.geom.geojson, srid=obj.geom.srid)
        geom_4326.transform(4326)

    feature = {
        "type": "Feature",
        "geometry": json.loads(geom_4326.geojson),
        "properties": {
            "id": obj.id,
            "name": getattr(obj, 'name', '')
        }
    }
    return JsonResponse({
        "type": "FeatureCollection",
        "features": [feature]
    })


# ——— Village data endpoint for popup ———

@api_view(['GET'])
def village_data(request, pk):
    """
    Return extra data for a village (for popup).
    """
    village = get_object_or_404(Village, pk=pk)
    serializer = VillageDataSerializer(village)
    return Response({ "data": serializer.data })
