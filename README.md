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
