import psycopg2
from functools import reduce

class Aod_ac3(object):

    table_name = "AOD_AC3"

    def get_data_from_file(self, filename):

        COMMENT_CHAR = '#'
        rows = []
        # ATS_TOA_1PUUPA20080315_161752_000065272066_00469_31585_4814.N1.txt
        # ATS_TOA_1PUUPA20080315_161752_000065272066_00469_31585_4814.N1.txt
        date_filename = filename.split("/")[-1]
        date = date_filename.split("_")[2][6:]
        my_time = date_filename.split("_")[3]
        # 2008 03 15_16 17 52
        timestamp = "%s-%s-%s %s:%s:%s"%(date[0:4],date[4:6],date[6:8],my_time[0:2],my_time[2:4],my_time[4:6])
        with open(filename, 'r') as td:
            for line in td:
                if line[0] != COMMENT_CHAR:
                    line = [timestamp]+line.split()
                    rows.append(line)
        return rows
        

    def create_table(self):
        
        # lo la tau sunn sunf satn satf azn azf itercnt 
        # 90.5999 63.2934 0.929862 84.9887 84.9995 21.0964 52.7284 37.8088 12.9453 13
        
        # float* , int unsined or byte

        my_connexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
        my_cursor = my_connexion.cursor()
        query = """
            CREATE TABLE %s (
            id SERIAL PRIMARY KEY, 
            timestamp DATE NOT NULL, 
            lon real, 
            lat real, 
            tau real, 
            sunm real, 
            sunf real,
            satn real,
            satf real,
            azn real,
            azf real, 
            itercnt smallint,
            geom geography)  ;
            """%self.table_name
        my_cursor.execute(query)
        my_cursor.close()
        my_connexion.commit()
    
    def insert(self, data_set):
        
        my_connexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
        my_cursor = my_connexion.cursor()

        fields = "timestamp, lon, lat, tau, sunm, sunf, satn, satf, azn, azf, itercnt, geom"
        query_header = "INSERT INTO %s (%s) VALUES " %(self.table_name, fields)

        for data in data_set:               
            line_db = reduce(lambda x,y: x+", "+y, data[1:])

            row = """
            ('%s', %s , ST_Buffer(ST_GeographyFromText('POINT(%s %s)'), 3000))
            """%(data[0], line_db, data[1], data[2])
            
            query = query_header + row 
            my_cursor.execute(query)
        
        my_cursor.close()
        my_connexion.commit()




# my_Aod_ac3 = Aod_ac3()
# path = "./misc/projectspace/XBAERout/AOD_AC3r06/2008/"
# my_Aod_ac3.get_data_from_file(path+"ATS_TOA_1PUUPA20080325_074030_000065272067_00106_31723_4952.N1.txt")