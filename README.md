HANA Persistent Memory Landscape Simplification, I made a copy of Lars Butzmann's HANA benchmark and improvised it with a few python scripts. Plus cross tenant access from Goran's blog https://blogs.sap.com/2018/02/13/cross-tenant-database-access-in-sap-hana/


Goal here is to show how Intel Persistent Memory can be enabled with HANA 2 SP03 & simplify SAP Landscape using the HANA 2 SP00 Inbuilt functionality Cross Tenant Access.



## Process

1. Create schema and define data types
2. Develop concept how the data should look like
3. Implement a data generator in Python (based on a previous data generator)
3.1 The original python does create the scripts for the 5 tables and the supplemental python scripts enable semi colons for VARCHAR allowing us to read
4. Enable Persistent Memory across entire system (global.ini --> persistent_memory table_default = ON)
5. Enable Cross Tenant Access 
6. Write a query across 2 tenants which there by removes the need to replicate data across multiple systems


## Assumptions
1. HANA 2 SP03 is installed with RHEL 7.5 or Higher
2. 128 GB DDR DIMMS are used to Populate half the channels and the rest are populated with 512 GB Intel Persistent Memory DIMMS
3. 2 Tenants are created ECC, ECCW are created 


## Challenges

* Re-write python script and load data files using HDB versus front end which was time consuming on the HANA Studio via Eclipse


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

* Intel Xeon CPU E7 8180 Platinum 4S

* In average 10 items per transaction
* Scale Factor 1
  * 100 customers
  * 200 stores
  * 500 items
  * 20.000 transactions
  * approximately 100.000 transaction items

This was not intended to be a performance test but a showcase how to simplify architecture.

## Results

