import os
from osgeo import ogr
from osgeo import osr
import collections

if __name__ == '__main__':

    target_vector_path = 'hidroweb_points.gpkg'
    gpkg_driver = ogr.GetDriverByName('GPKG')
    target_vector = gpkg_driver.CreateDataSource(target_vector_path)
    layer_name = os.path.basename(os.path.splitext(target_vector_path)[0])
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)
    wgs84_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    target_layer = (
        target_vector.CreateLayer(layer_name, wgs84_srs, ogr.wkbPoint))
    target_layer.StartTransaction()

    with open('hidroweb_bck_summary.csv', 'r') as csv_file:
        csv_table = csv_file.read()
    lines = csv_table.split('\n')

    headers = lines[0].split(',')

    for header in headers[1:]:
        layer_defn = target_layer.GetLayerDefn()
        target_field = ogr.FieldDefn(header, ogr.OFTInteger)
        target_layer.CreateField(target_field)

    feature_defn = target_layer.GetLayerDefn()
    site_to_data = collections.defaultdict(dict)

    with open('coords.csv', 'r') as coords_file:
        coords_table = coords_file.read()
    coords = coords_table.split('\n')
    for coord in coords:
        if coord == '':
            continue
        site, lng, lat = coord.split(',')
        site = int(site)
        lng, lat = float(lng), float(lat)
        site_to_data[site]['coords'] = (lng, lat)

    for table_row in lines[1:]:
        if table_row == '':
            continue
        vals = table_row.split(',')
        site = int(vals[0])
        site_to_data[site]['vals'] = vals[1:]

    for site, lookup in site_to_data.items():
        if 'vals' not in lookup:
            continue
        point_geom = ogr.Geometry(ogr.wkbPoint)
        point_geom.AddPoint(*lookup['coords'])
        point_feature = ogr.Feature(feature_defn)
        point_feature.SetGeometry(point_geom)
        for field, val in zip(headers[1:], lookup['vals']):
            point_feature.SetField(field, val)
        target_layer.CreateFeature(point_feature)
    target_layer.CommitTransaction()
