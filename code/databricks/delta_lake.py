# Databricks notebook source
dbutils.library.installPyPI("koalas")
dbutils.library.installPyPI("xlrd")
dbutils.library.restartPython()

# COMMAND ----------

import databricks.koalas as pd

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

koalasDF1 = pd.DataFrame({"col1":["a","b","c"], "col2":[1,2,3]})
koalasDF2 = pd.DataFrame({"col1":["d","e","f"], "col2":[4,5,6]})
koalasDF3 = pd.DataFrame({"col1":[7,8,9], "col2":["g","h","i"]})

# COMMAND ----------

print(type(koalasDF1))
print(type(koalasDF2))

# COMMAND ----------

# save the first koalasDF1 dataframe onto disk as a Delta Lake
# even if there were already files it simply add, but ignores previous upon a read of latest version
koalasDF1.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="overwrite")

# COMMAND ----------

# append koalasDF2 from any other notebook into the same storage location and same Schema
# mode = "append"  means it add these records and update the logs
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")

# COMMAND ----------

# appending koalasD3 with a mismatched schema will fail and enforce a message saving future trouble
## Failed to merge incompatible data types StringType and LongType

koalasDF3.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")

# COMMAND ----------

# let's open a connection to the delta lake named "koalasDF" as a dynamic dataframe
koalasDF = pd.read_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF")

# COMMAND ----------

# the amount of records should be 3 + 3
len(koalasDF)

# COMMAND ----------

# still seen as a koalas dataframe
type(koalasDF)

# COMMAND ----------

# it lost indexing and created a new one, but it shows the 6 records
koalasDF

# COMMAND ----------

# remember we had 6 records
len(koalasDF)

# COMMAND ----------

# let's test by adding 9 more records in 3 write actions 3 + 3 + 3 using "append"
# ‘append’: Append the new data to existing data
# ‘overwrite’: Overwrite existing data
# ‘ignore’: Silently ignore this operation if data already exists
# ‘error’ or ‘errorifexists’: Throw an exception if data already exists
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")
koalasDF2.to_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", mode="append")

# COMMAND ----------

# expect to have 6 + 9 just by calling the dataframe !
# it simply updates automatically, no need for reading in the dataframe
len(koalasDF)

# COMMAND ----------

# MAGIC %fs ls "dbfs:/mnt/adlsGen2/delta/koalas-DF"

# COMMAND ----------

# MAGIC %md
# MAGIC to see the old revisions of data changes

# COMMAND ----------

# MAGIC %fs ls "dbfs:/mnt/adlsGen2/delta/koalas-DF/_delta_log"

# COMMAND ----------

# MAGIC %md
# MAGIC let's try to load an older revision, for example the first creation and then show its content

# COMMAND ----------

koalasDF = pd.read_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", version=0)

# COMMAND ----------

# ideal for testing, or other stuff
# notice, it shows 3x records and not 15x
koalasDF

# COMMAND ----------

# loading the latest version again
koalasDF = pd.read_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF")

# COMMAND ----------

len(koalasDF)

# COMMAND ----------

# MAGIC %fs ls "dbfs:/mnt/adlsGen2/delta/koalas-DF/_delta_log"

# COMMAND ----------

# or loading a specific timestamp
#koalasDF = pd.read_delta(path="dbfs:/mnt/adlsGen2/delta/koalas-DF", timestamp="2020-03-24 09:34:32.000")

# COMMAND ----------

# let's demonstrate you can run SQL code on the dataframe in {}
pd.sql("""
SELECT * FROM {koalasDF}
WHERE col1 = 'e'
LIMIT 5
""")

# COMMAND ----------

# you can use Spark visualizations display()
display(koalasDF.plot.line(x="col1", y="col2", title="show the trend"))

# COMMAND ----------

