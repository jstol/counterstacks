python mrc.py traces/hm/hm_clean.csv hm 1000
python mrc.py traces/hm/hm_clean.csv hm 500
python mrc.py traces/hm/hm_clean.csv hm 250
python mrc_prune.py traces/hm/hm_clean.csv hm 500 0.2
python mrc_prune.py traces/hm/hm_clean.csv hm 500 0.01

python mrc.py traces/mds/mds_clean.csv mds 1000
python mrc.py traces/mds/mds_clean.csv mds 500
python mrc.py traces/mds/mds_clean.csv mds 250
python mrc_prune.py traces/mds/mds_clean.csv mds 250 0.2
python mrc_prune.py traces/mds/mds_clean.csv mds 250 0.01

python mrc.py traces/wdev/wdev_clean.csv wdev 1000
python mrc.py traces/wdev/wdev_clean.csv wdev 500
python mrc.py traces/wdev/wdev_clean.csv wdev 250
python mrc_prune.py traces/wdev/wdev_clean.csv wdev 250 0.2
python mrc_prune.py traces/wdev/wdev_clean.csv wdev 250 0.01

python mrc.py traces/web/web_clean.csv web 1000
python mrc.py traces/web/web_clean.csv web 500
python mrc.py traces/web/web_clean.csv web 250
python mrc_prune.py traces/web/web_clean.csv web 250 0.2
python mrc_prune.py traces/web/web_clean.csv web 250 0.01

python mrc.py traces/prn_/prn__clean.csv prn 1000
python mrc.py traces/prn_/prn__clean.csv prn 500
python mrc.py traces/prn_/prn__clean.csv prn 250
python mrc_prune.py traces/prn_/prn__clean.csv prn 250 0.2
python mrc_prune.py traces/prn_/prn__clean.csv prn 250 0.01