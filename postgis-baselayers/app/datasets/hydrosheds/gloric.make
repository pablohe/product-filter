install:
	# Copy what we're doing. This shows up in the logs afterwards.
	@echo Installing hydrosheds.gloric

	# Create the 'src' directory if it doesn't exist yet
	mkdir -p src
	@echo STATUS=Downloading
	cd src && wget -q -O GloRiC_v10_shapefile.zip https://postgis-baselayers-mirrors.s3.eu-central-1.amazonaws.com/hydrosheds_gloric/GloRiC_v10_shapefile.zip

	psql "$(POSTGRES_URI)" -c 'CREATE SCHEMA IF NOT EXISTS hydrosheds;'
	psql "$(POSTGRES_URI)" -c 'DROP TABLE IF EXISTS hydrosheds.gloric CASCADE'

	# Note! Using -lco PRECISION=NO to avoid numeric field overflow errors.
	@echo STATUS=Importing Gloric
	ogr2ogr -f PostgreSQL -update -append -nlt PROMOTE_TO_MULTI $(POSTGRES_OGR) -lco PRECISION=NO -lco SCHEMA=hydrosheds -lco GEOMETRY_NAME=geom -nln hydrosheds.gloric /vsizip/src/GloRiC_v10_shapefile.zip/GloRiC_v10_shapefile/GloRiC_v10.shp

	# Create indices
	@echo STATUS=Creating Indices
	psql "$(POSTGRES_URI)" -c "CREATE INDEX IF NOT EXISTS idx_gloric_reach_id ON hydrosheds.gloric (reach_id);"
	psql "$(POSTGRES_URI)" -c "CREATE INDEX IF NOT EXISTS idx_gloric_next_down ON hydrosheds.gloric (next_down);"

	# Clean up
	@echo STATUS=Complete

uninstall:
	@echo STATUS=Uninstalling
	psql "$(POSTGRES_URI)" -c 'DROP TABLE IF EXISTS hydrosheds.gloric CASCADE'


