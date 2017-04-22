#!/usr/bin/env python2

from sys import argv, exit
if len(argv) != 0:
  print 'Usage: ./osm-tileurl.py [zoom/lat/lon]'
  exit(1)

import math

def deg2num(zoom, lat_deg, lon_deg):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

coords = map(float, argv[1].strip().split('/'))
tn = map(str, deg2num(*coords))
print 'http://tile.openstreetmap.org/' + str(int(coords[0])) + '/' + tn[0] + '/' + tn[1] + '.png'
