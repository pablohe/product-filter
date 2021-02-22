
import netCDF4 as nc
from numpy.lib.function_base import select
import numpy as np

from io import BytesIO
from struct import pack
import psycopg2

import pandas as pd

from Aod_ac3 import Aod_ac3
from Polder import Polder


# https://www.postgresql.org/docs/9.5/datatype-numeric.html


def connect_to_db():
    conexion = psycopg2.connect(database="postgis-database", user="postgis", password="postgis", host="localhost", port=35432)
    cursor = conexion.cursor()
    return cursor, conexion

    sql="""
    SELECT
        ST_Intersection(
        polder3_l1b_bg1.geom, vg250_krs.geom
        )::geometry as geom
    FROM
        polder3_l1b_bg1, 
        "public"."vg250_krs"
        naturalearth.ne_10m_admin_1_states_provinces 
    WHERE
        gen='Verden' 
    AND
        ST_Intersects(polder3_l1b_bg1.geom, vg250_krs.geom)
    """

cursor, conexion = connect_to_db()

# my_polder3_l1b_bg1 = POLDER3()
# my_polder3_l1b_bg1.create_product_table()
# data_set = my_polder3_l1b_bg1.get_from_file()
# my_polder3_l1b_bg1.insert(cursor, conexion, data_set)

my_AOD_AC3 = Aod_ac3()
# my_AOD_AC3.create_table()

# /misc/projectspace/XBAERout/AOD_AC3r06/2008
from os import walk

path = "./misc/projectspace/XBAERout/AOD_AC3r06/2008/"
for (dirpath, dirnames, filenames) in walk(path):
    for file in filenames: 
        print("inserting... "+file)
        data_set = my_AOD_AC3.get_data_from_file(dirpath+file)
        my_AOD_AC3.insert(data_set)
