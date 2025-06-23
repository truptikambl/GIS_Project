# 🗺️ Maharashtra GIS Project (Django)

A Django-based GIS platform for visualizing and managing **Maharashtra's administrative boundaries** — State, Districts, Talukas, and Villages — using **GeoDjango**, **Shapely**, and **PostGIS**.

---

## 🌐 Features

- 🗂️ Hierarchical models: State → District → Taluka → Village
- 📥 Import multi-level GeoJSON files
- 🧠 Automatic geometry merging with Shapely
- 🧼 Cleans and fixes invalid geometries using `buffer(0)`
- 🌍 Visualize or process geospatial data with Django ORM

Map Interface-
Include up to 3 base layers:
OpenStreetMap
Satellite
Terrain

The default zoom level and center of the map should focus on India upon
initialization.
Dropdown Filters (Hierarchical):

State Selector

District Selector
Should update based on selected State

Taluka Selector
Should update based on selected District

Village Selector
Should update based on selected Taluka

Polygon Highlighting:
When a State, District, Taluka, or Village is selected, the
corresponding polygon boundary should be highlighted on the map.

Point Layer on Village Selection:
Upon selecting a Village data specific to that village should be fetched
from the database.

This data should appear in a popup when clicking the village polygon on
the map.


---

## 📦 Technologies Used

- Django 5+
- GeoDjango
- PostGIS
- GDAL/GEOS
- Shapely
- Python 3.12
- JSON-based Geo data

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanvantari-26/gis_project.git
cd gis_project

2. Set Up Virtual Environment
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Configure Database (PostgreSQL + PostGIS)
Ensure PostGIS is installed. Update settings.py with your DB credentials:
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

5. Import GeoJSON Data
Make sure your .geojson files are in the data/ folder.
python manage.py import_all_geojson

🗃️ Folder Structure
gis_project/
├── maps/                  # Django app with models (State, District, etc.)
├── data/                  # GeoJSON files: mh1.geojson, mh2.geojson
├── manage.py
├── gis_project/           # Django settings and URLs
├── requirements.txt
├── .gitignore
└── README.md

🧑‍💻 Author
Dhanvantari Latambale



