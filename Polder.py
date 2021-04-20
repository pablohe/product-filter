import psycopg2
import numpy as np
import netCDF4 as nc

class Polder(object):
    
    table_name = "polder3_l1b_bg1"

    def create_product_table(self):
        
        my_connexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
        my_cursor = my_connexion.cursor()
        query = "CREATE TABLE polder3_l1b_bg1 (id SERIAL PRIMARY KEY, timestamp DATE NOT NULL, lon real, lat real, oad real, geom geography)  ;"
        my_cursor.execute(query)
        my_cursor.close()
        my_connexion.commit()


    def get_from_file(self):
        fn = 'POLDER3_L1B-BG1-082124M_2008-07-01T11-53-11_V1-01_null.nc'
        date_set = nc.Dataset(fn)
        time = date_set.variables["time"] 
        time = date_set.variables["time"] 
        time = date_set.variables["time"] 

        timestamp = nc.num2date(date_set.variables['time'][:],units=date_set.variables['time'].units)
        
        lon = np.array(date_set.variables["lon"])
        lat = np.array(date_set.variables["lat"])
        aod = np.array(date_set.variables["aod"])
        
        return timestamp, lat, lon, aod

    def insert(self, cursor, conexion, data_set):
        
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
            ST_Buffer(ST_GeographyFromText('POINT(%s %s)'), 3000))
            """%(data[0], data[2], data[1], data[3], data[2], data[1])
            # print(query)
            cursor.execute(query)
        
        cursor.close()
        conexion.commit()
 	