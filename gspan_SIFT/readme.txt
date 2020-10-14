how to run:
python -m gspan_mining -s "minRF" ./graphdata/"datasetname"

eg:
python -m gspan_mining -s 0.2 ./graphdata/papertoydata.txt.

output:
"min_sup"_"dataset_name"flat_trans.txt ---- contains flat transactions 
"min_sup"_"dataset_name"_stats.txt     ----- contains statistics like time , no of subgraphs,execution time and average no of transactions.


After extracting flat transactions, run cmine_mapreduce.py using

python cmine_mapreduce.py $minRF $minCS $maxOR $proc $1 pre $1\_$dataset\_Output.txt

proc defines the number of machines
