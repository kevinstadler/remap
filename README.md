remap
=====

remap is a collection of scripts for generating interesting experimental large scale maps and other visualisations of geospatial data, primarily for print. a previous version of some of the scripts for rendering directly from osm files (rather than a postgis sever) can be found [here](https://github.com/kevinstadler/remap-legacy).

bits
----

`overlay.py` makes use of proj.4's [ob\_tran](https://github.com/kevinstadler/notes/raw/master/ob_tran.pdf) pseudo-projection to overlay several PostGIS query results, typically from different locations, on top of each other. all layers are translated so that the center of their extents coincide with the center of the canvas, allowing interesting visual size comparisons, among other things.

`maparrangement.py` is a replacement for python-mapnik's [PDFPrinter](mapnik.org/docs/v2.0.2/api/python/mapnik.printing.PDFPrinter-class.html) class which offers several improvements: - rendering occurs at the correct map scale - map backgrounds are actually drawn - allows several maps to be rendered on the same canvas without overlap (including insets) - option to draw borders around the maps

setup
-----

to use `remap.py` and `overlay.py` you will need [mapnik](http://mapnik.org) (v3 branch plus [python bindings](https://github.com/mapnik/python-mapnik)) installed. you will also need access to a PostGIS database populated with some ([OpenStreetMap](http://www.openstreetmap.org/)) data.

a handy script for automatic installation+setup of both under Fedora (which should be easily transferrable to other Linux distributions) can be found [here](scripts/setup-mapnik-postgis-fedora).

data
----

OSM's full planet data is big, takes an awful long time to import, and you probably don't need it. handy extracts can be found on these two sites:

-   for urban extracts: <https://mapzen.com/data/metro-extracts/>
-   for country/continent extracts: <https://download.geofabrik.de>

useful scripts for further filtering of extracts, as well as for querying small data sets directly from osm's [overpass api](https://wiki.openstreetmap.org/wiki/Overpass_API) can be found in \[scripts/\].

links
-----

interested in rendering experimental or 'unusual' *world* maps for web or print? check out my [south up!](https://github.com/kevinstadler/southup) repository!

other interesting projects:

-   [tactical cartography](http://ccra.mitotedigital.org/taxonomy/term/71)
-   [Anti-eviction Mapping Project](https://www.antievictionmap.com)

usage: `overlay.py`
-------------------

``` bash
./overlay.py --help
```

    ## usage: overlay.py [-h] -s SCALE [--srs SRS] [--dbsrs DBSRS]
    ##                   [--queries [QUERIES [QUERIES ...]]]
    ##                   [-lon [LONGITUDE [LONGITUDE ...]]]
    ##                   [-lat [LATITUDE [LATITUDE ...]]] [-f FORMAT] [-m MARGIN]
    ##                   [--columns COLUMNS] [--rows ROWS] [--dpi DPI] [-o OUTPUT]
    ## 
    ## overlay several PostGIS query results on top of each other. by default all
    ## layers are translated so that the centers of their extents coincide with the
    ## center of the target map (which is the origin). different centers can be
    ## specified per query with the -lon and -lat options, of which there need to be
    ## as many as there are queries.
    ## 
    ## optional arguments:
    ##   -h, --help            show this help message and exit
    ##   -s SCALE, --scale SCALE
    ##                         output map scale denominator (required)
    ##   --srs SRS             target projection to be used (proj.4 string, default:
    ##                         +proj=ortho +ellps=WGS84)
    ##   --dbsrs DBSRS         projection of the postgis database (default: Web
    ##                         Mercator, i.e. +proj=merc +k=1 +a=6378137 +b=6378137
    ##                         +no_defs)
    ##   --queries [QUERIES [QUERIES ...]], -q [QUERIES [QUERIES ...]]
    ##                         sql queries to be run
    ##   -lon [LONGITUDE [LONGITUDE ...]], --longitude [LONGITUDE [LONGITUDE ...]]
    ##                         map center longitude, one per osm file (e.g. -3.1977
    ##                         -.2326)
    ##   -lat [LATITUDE [LATITUDE ...]], --latitude [LATITUDE [LATITUDE ...]]
    ##                         map center latitude, one per osm file (e.g. 55.9486
    ##                         51.5465)
    ##   -o OUTPUT, --output OUTPUT
    ##                         output filename (default: overlay.pdf)
    ## 
    ## output/rendering options:
    ##   -f FORMAT, --format FORMAT
    ##                         Cairo target page format (default: "a4l")
    ##   -m MARGIN, --margin MARGIN
    ##                         page margin in meters (default: 0.0)
    ##   --columns COLUMNS     number of columns to use for map gallery (default: 1)
    ##   --rows ROWS           number of rows to use for map gallery (default: 1)
    ##   --dpi DPI             output dpi (default: 72)

todos
=====

-   switch to imposm3
-   unify ways which are connected when they share the same name and highway classification (see [here](https://gis.stackexchange.com/questions/61845/how-to-merge-connected-lines-with-same-direction-postgis) and [here](https://gis.stackexchange.com/questions/94203/grouping-connected-linestrings-in-postgis))
-   maybe use [Skeletron](https://github.com/migurski/Skeletron)?
