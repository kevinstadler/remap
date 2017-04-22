#!/usr/bin/env python2

# hide redefined mapnik python bindings warning on import
import warnings
warnings.simplefilter('ignore')
from mapnik import *
warnings.resetwarnings()
import mapnik.printing

from maparrangement import *
import xml.dom.minidom as xml
from colorsys import hsv_to_rgb

from argparse import ArgumentParser
parser = ArgumentParser(description='overlay several PostGIS query results on top of each other. by default all layers are translated so that the centers of their extents coincide with the center of the target map (which is the origin). different centers can be specified per query with the -lon and -lat options, of which there need to be as many as there are queries.')

# general rendering & geography
parser.add_argument('-s', '--scale', required=True, type=float, help='output map scale denominator (required)')
parser.add_argument('--srs', default='+proj=ortho +ellps=WGS84', help='target projection to be used (proj.4 string, default: %(default)s)')
# +init=epsg:3857
parser.add_argument('--dbsrs', default='+proj=merc +k=1 +a=6378137 +b=6378137 +no_defs', help='projection of the postgis database (default: Web Mercator, i.e. %(default)s)')

parser.add_argument('--queries', '-q', nargs='*', help='sql queries to be run')
parser.add_argument('-lon', '--longitude', type=float, default=[None], help='map center longitude, one per osm file (e.g. -3.1977 -.2326)', nargs='*')
parser.add_argument('-lat', '--latitude', type=float, default=[None], help='map center latitude, one per osm file (e.g. 55.9486 51.5465)', nargs='*')

# output
output = parser.add_argument_group('output/rendering options')
output.add_argument('-f', '--format', default='a4l',
  help='Cairo target page format (default: "%(default)s")')
output.add_argument('-m', '--margin', type=float, default=0.0,
  help='page margin in meters (default: %(default)s)')
output.add_argument('--columns', type=int, default=1,
  help='number of columns to use for map gallery (default: %(default)s)')
output.add_argument('--rows', type=int, default=1,
  help='number of rows to use for map gallery (default: %(default)s)')

output.add_argument('--dpi', type=float, default=72,
  help='output dpi (default: %(default)s)')
parser.add_argument('-o', '--output', default='overlay.pdf', help='output filename (default: %(default)s)')

args = vars(parser.parse_args())

nlayers = len(args['queries'])

def checkarglen(argname):
  if args[argname] != None and len(args[argname]) != nlayers:
    if len(args[argname]) == 1:
     args[argname] = args[argname][0:1] * nlayers
    else:
      print 'number of ' + argname + 's does not match number of layers, ignoring ' + argname + 's'
      args[argname] = None

checkarglen('longitude')
checkarglen('latitude')

# pale rainbow
colours = map(lambda rgb: Color(int(256*rgb[0]), int(256*rgb[1]), int(256*rgb[2]), 200),
  [hsv_to_rgb(i / float(nlayers+1), 0.5, 0.7) for i in range(nlayers)])

m = Map(1, 1, args['srs'])

def addlayer(i, query):
  l = Layer(str(i))
  l.datasource = PostGIS(host='localhost', dbname='gis', table=query, extent_from_subquery=True)

  s = Style()
  r = Rule()
  sb = LineSymbolizer()
  sb.stroke = colours[i]
  r.symbols.append(sb)
  s.rules.append(r)
  m.append_style(str(i), s)

  l.styles.append(str(i))

  # identify center
  center = Projection(args['dbsrs']).inverse(l.envelope().center())
  if args['longitude'][i] != None:
    center.x = args['longitude'][i]
  if args['latitude'][i] != None:
    center.y = args['latitude'][i]

  print 'layer ' + str(i) + ': transposing ' + str(center) + ' to center'

  l.srs = '+proj=ob_tran +o_lon_p=' + str(center.x) + ' +o_lat_p=' + str(center.y+90) + ' +o_' + args['dbsrs'][1:]

  m.layers.append(l)

for i in range(len(args['queries'])):
  addlayer(i, args['queries'][i])

m.zoom_to_box(Box2d(-1, -1, 1, 1))

print 'Zooming by a factor', args['scale'] / m.scale_denominator()
m.zoom(args['scale'] / m.scale_denominator())

pagesize = printing.pagesizes[args['format']]

surface = MapArrangement(pagesize=pagesize, resolution=args['dpi'], ncols=args['columns'], nrows=args['rows'])

print 'writing map at scale 1:' + str(m.scale_denominator())
surface.render_map(m, args['output'], split_layers=True if args['columns']*args['rows']>1 else False, draw_border=False)

#print surface.render_scale(m)

surface.finish()

print 'successfully wrote to', args['output']
