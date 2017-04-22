## oxfords

all the oxfords in the united states, from west to east

```{bash}
cd ..

# grab boundaries of every area called Oxford
scripts/download-boundaries "Oxford"
scripts/postgis-append Oxford-boundaries.osm
# copy Oxford MS from polygon to line table
psql gis < INSERT INTO planet_osm_line (osm_id, way) SELECT osm_id, ST_ExteriorRing(way) FROM planet_osm_polygon WHERE osm_id = -109850;

# 1:120.000 for overlaid a4 (including Oxford, UK) from east to west to reduce overlay:
./overlay.py --format a4l --scale 120000 --queries '(select way from planet_osm_line where osm_id='{-394037,34299570,-1844185,-170997,37863485,-188715,-133733,38064152,34370509,-119608,-182574,-110495,34094425,-109850,40844255,34121983,34151110,37506613,33736028}') as boundary' -o "oxfords-overlay.pdf"

# 1:550.000 for a 3x6 grid of just US Oxfords (fits both landscape + portrait)
./overlay.py --format a4l --columns 3 --rows 6 --scale 550000 --queries '(select way from planet_osm_line where osm_id='{33736028,37506613,34151110,34121983,40844255,-109850,34094425,-110495,-182574,-119608,34370509,38064152,-133733,-188715,37863485,-170997,-1844185,34299570}') as boundary' -o "oxfords-gallery.pdf"
```
