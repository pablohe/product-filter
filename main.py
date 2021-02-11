
import netCDF4 as nc
from numpy.lib.function_base import select
import psycopg2
import numpy as np

from io import BytesIO
from struct import pack
import psycopg2

def create_product_table():

    my_connexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
    my_cursor = my_connexion.cursor()
    query = "CREATE TABLE polder3_l1b_bg1 (id SERIAL PRIMARY KEY, timestamp DATE NOT NULL, lon real, lat real, oad real, geom geography)  ;"
    my_cursor.execute(query)
    my_cursor.close()
    my_connexion.commit()





def get_product_from_netcdf():
    fn = 'POLDER3_L1B-BG1-082124M_2008-07-01T11-53-11_V1-01_null.nc'
    date_set = nc.Dataset(fn)
    time = date_set.variables["time"] 

    timestamp = nc.num2date(date_set.variables['time'][:],units=date_set.variables['time'].units)
    
    lon = np.array(date_set.variables["lon"])
    lat = np.array(date_set.variables["lat"])
    aod = np.array(date_set.variables["aod"])
    
    return timestamp, lat, lon, aod

def connect_to_db():
    conexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
    cursor = conexion.cursor()
    return cursor, conexion

def insert_product(cursor, conexion, data_set):
    
    timestamp, lon, lat, aod = data_set

    data_set = np.hstack((
            timestamp.reshape(timestamp.size,1),
            lon.reshape(lon.size,1),
            lat.reshape(lat.size,1),
            aod.reshape(aod.size,1)
    ))

    

    for data in data_set:   
        #  INSERT INTO polder3_l1b_bg1 (timestamp, lon, lat, oad, geom ) VALUES ('20200101 13:00', 10, 66, 125, ST_GeometryFromText('POINT(10 66)', 4326) );
        query = """
        INSERT INTO polder3_l1b_bg1 (timestamp, lon, lat, oad, geom ) VALUES 
        ('%s', %s, %s, %s,
        ST_Buffer(ST_GeographyFromText('POINT(%s %s %s)'), 3000))
        """%(data[0], data[2], data[1], data[3], data[2], data[1],data[3])
        # print(query)
        cursor.execute(query)
    
    cursor.close()
    conexion.commit()
 	
    sql="""
    SELECT
        ST_Intersection(
        polder3_l1b_bg1.geom, naturalearth.ne_10m_admin_1_states_provinces.geom
        )::geometry as geom
    FROM
        polder3_l1b_bg1, naturalearth.ne_10m_admin_1_states_provinces 
    WHERE
        name='Bremen' 
    AND
        ST_Intersects(polder3_l1b_bg1.geom, naturalearth.ne_10m_admin_1_states_provinces.geom)
    """
    
    # cuadradito
    # SELECT * from polder3_l1b_bg1 where geom && ST_MakeEnvelope(8.4, 52.9, 8.6, 53.1, 4326)

    # select circular section
    # SELECT * FROM polder3_l1b_bg1 WHERE ST_DWithin ( geography (ST_Point(lon,lat)), geography (ST_Point(8.7979694, 53.0763431)), 60000)

    # CIRCULARSTRING(0 0, 4 0, 4 4, 0 4, 0 0)
    # The CIRCULARSTRING is the basic curve type, similar to a LINESTRING in 
    # the linear world. A single segment required three points, the start and 
    # end points (first and third) and any other point on the arc. The exception 
    # to this is for a closed circle, where the start and end points are the same.
    # In this case the second point MUST be the center of the arc, ie the opposite 
    # side of the circle. To chain arcs together, the last point of the previous arc 
    # becomes the first point of the next arc, just like in LINESTRING. This means
    # that a valid circular string must have an odd number of points greater than 1.

create_product_table()

data_set = get_product_from_netcdf()
cursor, conexion = connect_to_db()
insert_product(cursor, conexion, data_set)

