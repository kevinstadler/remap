collection of handy shell and python scripts for a number of tasks

## postgis installation and setup

run [setup-postgis-mapnik-fedora] as root to install all remap dependencies and set up your postgis server. probably easily adaptable to other linux distributions.

## osm/overpass data extraction

[overpass] is a mini shell script for querying osm data from an overpass API server over http. [download-area] contains a small readymade query that is useful for retrieving small custom extracts of specific areas given either by their [overpass area name](http://wiki.openstreetmap.org/wiki/Overpass_API/Areas) or osm [relation id](http://wiki.openstreetmap.org/wiki/Relation#Tools) (think of it as a poor man's [vector tiles](https://www.mapbox.com/vector-tiles/)).

```{bash}
./overpass-area "Greater London"
./overpass-area 11
```
will download an osm file containing all the nodes, ways and relations found within the given area *plus the ways' and relations' extensions outside the area*. this way you can be sure that most polygons that are only partially within an area are extracted intact (i.e. as closed ways).

to create overlays (such as the ones in the [examples/]) you might only be interested in downloading a small subset of the features of an area, see e.g. [download-boundaries].

<!--
## data cleaning and manipulation

### clipping to a polygon

ogr2ogr: https://giswiki.hsr.ch/HowTo_OGR2OGR#R.C3.A4umlicher_Ausschnitt_.28ogr2ogr-Option_spat_und_clip.29

```{bash}
 ogr2ogr -f "SQLite" triesen.sqlite
   /vsicurl/http://download.geofabrik.de/europe/liechtenstein-latest.osm.pbf
   -dsco SPATIALITE=YES -skipfailures -progress -overwrite -gt 65536    
   -clipsrc "http://tools.wmflabs.org/wiwosm/osmjson/getGeoJSON.php?lang=en&article=Triesen" 
   -clipsrclayer OGRGeoJSON
   -nlt PROMOTE_TO_MULTI
```

osmconvert: http://wiki.openstreetmap.org/wiki/Osmconvert#Clipping_based_on_a_Polygon
http://m.m.i24.cc/osmconvert64
-->

## data import to postgis

the [postgis-append] script calls [osm2pgsql](https://github.com/openstreetmap/osm2pgsql) with some standard options to *add* data in various osm formats to your local postgis database. it uses the [remap.style] database style, which is identical to the default style except that it also preserves `[cycleway](http://wiki.openstreetmap.org/wiki/Key:cycleway)` tags.

to get an idea of disk space and processing requirements on a non-dedicated computer, see the following osm2pgsql log for an import of the mapzen [london metro extract](https://mapzen.com/data/metro-extracts/metro/london_england/) (127MB pbf download yielding 2814MB on disk once imported into postgis) on a dual-core laptop with ssd. [imposm3](https://github.com/omniscale/imposm3) is an osm-import alternative worth looking into.

<!--
#!/bin/sh

# get binary: https://imposm.org/static/rel/

# import: https://github.com/openmaptiles/import-osm
# https://github.com/omniscale/imposm3#usage
imposm3 import -connection postgis://user:passwd@host/database \
    -mapping mapping.json -deployproduction

# for mapping routes see: http://wiki.openstreetmap.org/wiki/Types_of_relation#Established_relations

# good starting point for import style definition:
#https://github.com/mapbox/osm-bright/blob/master/imposm-mapping.py
-->

```
Reading in file: london_england.osm.pbf
Using PBF parser.
Processing: Node(11836k 1.4k/s) Way(1707k 0.81k/s) Relation(32950 35.20/s)  parse time: 11341s
Node stats: total(11836319), max(4791749024) in 8303s
Way stats: total(1707014), max(486585298) in 2098s
Relation stats: total(32952), max(7153030) in 936s

...

Using 2 helper-processes
Finished processing 942245 ways in 1095 s

942245 Pending ways took 1095s at a rate of 860.50/s

...

Going over pending relations...
	5611 relations are pending

Using 2 helper-processes
Finished processing 5611 relations in 13 s

5611 Pending relations took 13s at a rate of 431.62/s

...

node cache: stored: 11836319(100.00%), storage efficiency: 50.06% (dense blocks: 16, sparse nodes: 11757548), hit rate: 100.08%

Osm2pgsql took 12450s overall
```
