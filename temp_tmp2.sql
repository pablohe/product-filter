SET standard_conforming_strings = OFF;
DROP TABLE IF EXISTS "public"."temp_tmp2" CASCADE;
DELETE FROM geometry_columns WHERE f_table_name = 'temp_tmp2' AND f_table_schema = 'public';
BEGIN;
CREATE TABLE "public"."temp_tmp2" ( "ogc_fid" SERIAL, CONSTRAINT "temp_tmp2_pk" PRIMARY KEY ("ogc_fid") );
SELECT AddGeometryColumn('public','temp_tmp2','wkb_geometry',-1,'GEOMETRY',2);
CREATE INDEX "temp_tmp2_wkb_geometry_geom_idx" ON "public"."temp_tmp2" USING GIST ("wkb_geometry");
COMMIT;
