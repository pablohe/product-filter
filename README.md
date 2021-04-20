# product-filter

https://github.com/kokoalberti/postgis-baselayers

## Deploy 

```
cd
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh ./Miniconda3-latest-Linux-x86_64.sh 
cd miniconda3/
eval "$(/home/pechevar/miniconda3/bin/conda shell.bash hook)" 
conda create -n product-filter-env python
conda activate product-filter-env
conda install python=3.8.5
conda install netcdf4=1.5.3

git clone git@github.com:pablohe/product-filter.git
cd product-filter
```

## usage 
```
eval "$(/home/pechevar/miniconda3/bin/conda shell.bash hook)" 
conda activate product-filter-env
```

## German regions

The source of the German regions came from:

https://github.com/highsource/postgis-verwaltungsgebiete

The difeerent levels of administratives areas are stored in the data folder 
to import into the data base you have to call:

```
 shp2pgsql -I -d -s 31467:4326 "data/vg-shape-files/VG250_KRS.shp" public.VG250_KRS | psql -q --username=postgis --dbname=postgis-database --password  --host="localhost" --port=35432
```
```
 sudo apt-get install libgeos-dev
 sudo apt-get install libproj-dev
 pip install cartopy
```