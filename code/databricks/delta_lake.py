# Databricks notebook source
dbutils.library.installPyPI("koalas")
dbutils.library.installPyPI("xlrd")
dbutils.library.restartPython()

# COMMAND ----------

import databricks.koalas as pd

# COMMAND ----------

# MAGIC %fs ls /mnt/

# COMMAND ----------

koalasDF1 = pd.DataFrame({"col1":["a","b","c"], "col2":[1,2,3]})
koalasDF2 = pd.DataFrame({"col1":["d","e","f"], "col2":[4,5,6]})

# COMMAND ----------

type(koalasDF1)

# COMMAND ----------

# write koalasDf1 
koalasDF1.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="overwrite")

# COMMAND ----------

# append koalasDF2
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")

# COMMAND ----------

# if we read in the data will it be larger ?
koalasDF = pd.read_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF")
len(koalasDF)

# COMMAND ----------

type(koalasDF)

# COMMAND ----------

koalasDF

# COMMAND ----------

len(koalasDF)

# COMMAND ----------

# let's test by adding 9 more records in 3 write actions
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")

# COMMAND ----------

len(koalasDF)

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

pharma_ref_koalasDF = pd.read_excel("/dbfs/mnt/adlsGen2/bronze/pharma_ref.xlsx", dtype={"drug_code":'str', "produit_pharma":'str'})

# COMMAND ----------

# koalas --> spark
rawDataDF = pharma_ref_koalasDF.to_spark()

# COMMAND ----------

deltaDataPath = "dbfs:/mnt/adlsGen2/delta/customer-data-using-spark/"

# COMMAND ----------

# write to delta dataset (parquet files)
rawDataDF.write.mode("overwrite").format("delta").save("dbfs:/mnt/adlsGen2/delta/customer-data-using-spark/")

# COMMAND ----------

#koalas delta
pharma_ref_koalasDF.to_delta(path="dbfs:/mnt/adlsGen2/delta/customer-data-using-koalas/", mode="overwrite")

# COMMAND ----------

spark.sql("""
  DROP TABLE IF EXISTS pharmaref_delta
""")
spark.sql("""
  CREATE TABLE pharmaref_delta 
  USING DELTA 
  LOCATION '{}' 
""".format("dbfs:/mnt/adlsGen2/delta/customer-data-using-spark/"))
#deltaDataPath = "dbfs:/mnt/adlsGen2/delta/customer-data/"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM pharmaref_delta

# COMMAND ----------

len(pharma_ref_koalasDF)

# COMMAND ----------

#pharma_ref_koalasDF.head(5).to_csv("dbfs:/mnt/adlsGen2/temp")
extra_data = pd.read_csv("dbfs:/mnt/adlsGen2/temp",
                         dtype={"drug_code":'str', "produit_pharma":'str', 'trim_pharma':'int64',
                                'nombre_prises':'int64', "orphan_flag":'int64', "chapter_IV_bis_flag":'int64', "link_same_tablet":'int64'})
pharma_ref_koalasDF.dtypes

# COMMAND ----------

extra_data.dtypes

# COMMAND ----------

#koalas delta
extra_data.to_delta(path="dbfs:/mnt/adlsGen2/delta/customer-data-using-koalas/", mode="append")

# COMMAND ----------

len(extra_data)

# COMMAND ----------

# 36898 + 5 = 36903
len(pharma_ref_koalasDF)

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL pharmaref_delta

# COMMAND ----------

# lets add data
pharma_ref_koalasDF.write.mode("append").format("delta").save("dbfs:/mnt/adlsGen2/delta/customer-data-using-spark/")

# COMMAND ----------

