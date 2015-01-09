pos-hana-benchmark
==================

Evaluate the performance of POS queries on SAP HANA


## Process

1. Create schema and define data types
2. Develop concept how the data should look like
3. Implement a data generator in Python (based on a previous data generator)
4. Import data using csv importer
5. Benchmark different data set sizes for given queries


## Challenges

* slow VPN connection to Germany
* HANA Python connector only works on the server, so some back and forth to fix some bugs
* 1y old HANA version -> I suggest to get a recent version at the end of the week to confirm the results (I assume the database got faster over the time)


## File structure

Most files are self explaining (schema, queries, sample_data).
The benchmark.py contains a data generation section and the benchmark for the query itself.
There are two files in the generator folder, one file containing the basic generator class with all required functions to create csv files. The other file contains a class for each table with some data creation logic.


## HowTo Data Generator

* open data_generator.py
* adjust SCALE_FACTOR
* run python data_generator.py
* output is found in generator/generated_data/


## Stats

* Intel Xeon CPU E5450 @ 3.00GHz
* 64GB RAM

* In average 10 items per transaction
* Scale Factor 1
  * 100 customers
  * 200 stores
  * 500 items
  * 20.000 transactions
  * approximately 100.000 transaction items


## Results

* Scale Factor 100 (19Mio transaction items -> 665MB csv file, 2Mio transactions -> 102MB csv file)
  * Average Time: 0.827041
  * [0.81100010871887207, 0.81727099418640137, 0.81864404678344727, 0.82291293144226074, 0.82594799995422363, 0.82802987098693848, 0.82954597473144531, 0.83091306686401367, 0.8407599925994873, 0.84538006782531738]
* Scale Factor 10 (1.9Mio transaction items -> 61MB csv file, 200k transactions -> 9.6MB csv file)
  * Average Time: 0.099740
  * [0.093641996383666992, 0.096506834030151367, 0.097066879272460938, 0.097069025039672852, 0.097651004791259766, 0.098144054412841797, 0.099153041839599609, 0.099488973617553711, 0.10074210166931152, 0.11793303489685059]
* Scale Factor 1 (190k transaction items, 20k transactions)
  * Average Time: 0.044614
  * [0.042074918746948242, 0.042280912399291992, 0.042377948760986328, 0.042675971984863281, 0.042942047119140625, 0.042946815490722656, 0.043231010437011719, 0.043322086334228516, 0.043447017669677734, 0.060845136642456055]


