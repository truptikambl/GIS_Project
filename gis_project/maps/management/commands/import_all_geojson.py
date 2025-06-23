import json
from collections import defaultdict
from django.core.management.base import BaseCommand
from shapely.geometry import shape, mapping, MultiPolygon, Polygon as ShapelyPolygon
from shapely.ops import unary_union
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon as GEOSMultiPolygon, Polygon as GEOSPolygon
from maps.models import State, District, Taluka, Village


class Command(BaseCommand):
    help = 'Import and assign geometries for all levels (State, District, Taluka, Village)'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Clearing old data...")
        Village.objects.all().delete()
        Taluka.objects.all().delete()
        District.objects.all().delete()
        State.objects.all().delete()

        files = ['data/mh1.geojson', 'data/mh2.geojson']
        district_geoms = defaultdict(list)
        taluka_geoms = defaultdict(list)
        state_geoms = []

        for file_path in files:
            self.stdout.write(f'🔄 Processing {file_path}...')
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson = json.load(f)

            for feature in geojson.get('features', []):
                props = feature['properties']
                geom_data = feature.get('geometry')
                if not geom_data:
                    continue

                try:
                    geo = GEOSGeometry(json.dumps(geom_data), srid=4326)
                    if isinstance(geo, GEOSPolygon):
                        geo = GEOSMultiPolygon(geo)
                    if geo.empty:
                        continue
                except Exception as e:
                    print(f"❌ Skipping invalid geometry: {e}")
                    continue

                geom_json = json.loads(geo.geojson)

                state_name = props.get('STATE', '').strip()
                district_name = props.get('DISTRICT', '').strip()
                taluka_name = props.get('SUB_DIST', '').strip()
                village_name = props.get('NAME', '').strip()

                state, _ = State.objects.get_or_create(name=state_name)
                district, _ = District.objects.get_or_create(name=district_name, state=state)
                taluka, _ = Taluka.objects.get_or_create(name=taluka_name, district=district)

                district_geoms[district.id].append(geom_json)
                taluka_geoms[taluka.id].append(geom_json)
                state_geoms.append(geom_json)

                if village_name:
                    if isinstance(geo, GEOSPolygon):
                        geo = GEOSMultiPolygon(geo)
                    village, created = Village.objects.get_or_create(
                        name=village_name,
                        taluka=taluka,
                        defaults={'geom': geo}
                    )
                    if not created:
                        village.geom = geo
                        village.save()
                    print(f"✅ Saved village: {village.name}, geom valid: {village.geom.valid}")

        self.stdout.write("🧩 Combining geometries...")

        # 🔹 DISTRICT GEOMETRIES
        for did, geom_jsons in district_geoms.items():
            district = District.objects.get(id=did)
            try:
                shapely_geoms = [shape(g) for g in geom_jsons]
                merged = unary_union(shapely_geoms)
                if not merged.is_valid:
                    print(f"⚠️ Fixing invalid district geom: {district.name}")
                    merged = merged.buffer(0)
                district.geom = GEOSGeometry(json.dumps(mapping(merged)), srid=4326)
                district.save()
                print(f"✅ District saved: {district.name}, geom valid: {district.geom.valid}")
            except Exception as e:
                print(f"❌ Error saving district {district.name}: {e}")

        # 🔹 TALUKA GEOMETRIES
        for tid, geom_jsons in taluka_geoms.items():
            taluka = Taluka.objects.get(id=tid)
            try:
                shapely_geoms = [shape(g) for g in geom_jsons]
                merged = unary_union(shapely_geoms)
                if not merged.is_valid:
                    print(f"⚠️ Fixing invalid taluka geom: {taluka.name}")
                    merged = merged.buffer(0)
                taluka.geom = GEOSGeometry(json.dumps(mapping(merged)), srid=4326)
                taluka.save()
                print(f"✅ Taluka saved: {taluka.name}, geom valid: {taluka.geom.valid}")
            except Exception as e:
                print(f"❌ Error saving taluka {taluka.name}: {e}")

        # 🔹 STATE GEOMETRY (Maharashtra)
        # 🔹 STATE GEOMETRY (Assuming only Maharashtra)
        if state_geoms:
            try:
                state = State.objects.get(name__iexact="Maharashtra")
                shapely_geoms = [shape(gjson) for gjson in state_geoms]
                flat_polygons = []
                for geom in shapely_geoms:
                    if isinstance(geom, ShapelyPolygon):
                        flat_polygons.append(geom)
                    elif isinstance(geom, MultiPolygon):
                        flat_polygons.extend(geom.geoms)
                if flat_polygons:
                    merged = MultiPolygon(flat_polygons) if len(flat_polygons) > 1 else flat_polygons[0]
                    if isinstance(merged, ShapelyPolygon):
                        merged = MultiPolygon([merged])
                    
                    # ✅ FIX invalid geometry (like self-intersections)
                    if not merged.is_valid:
                        print("⚠️ Fixing invalid state geometry using buffer(0)...")
                        merged = merged.buffer(0)

                    fixed_geom = GEOSGeometry(json.dumps(mapping(merged)), srid=4326)
                    state.geom = fixed_geom
                    state.save()
                    print(f"✅ State saved: {state.name}, geom valid: {state.geom.valid}")
            except State.DoesNotExist:
                print("❌ 'Maharashtra' state not found for final aggregation.")
