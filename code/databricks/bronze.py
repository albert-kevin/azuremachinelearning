# Databricks notebook source
# MAGIC %md
# MAGIC ## Transform data

# COMMAND ----------

# MAGIC %md
# MAGIC Load python packages and restart kernel

# COMMAND ----------

dbutils.library.installPyPI("koalas")
dbutils.library.installPyPI("xlrd")
dbutils.library.restartPython()

# COMMAND ----------

import databricks.koalas as pd     #preferred method (default: import databricks.koalas as ks)

# COMMAND ----------

# MAGIC %md
# MAGIC Verify mounts  
# MAGIC   * check for mounted filesystems, azure datalake gen2
# MAGIC   * check filesystem content

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

# MAGIC %fs ls /mnt/adlsGen2

# COMMAND ----------

# MAGIC %fs ls /mnt/adlsGen2/bronze

# COMMAND ----------

# MAGIC %md
# MAGIC Extracting data from Data Lake

# COMMAND ----------

# read in for example an *.xlsx
pharma_ref_koalasDF = pd.read_excel("/dbfs/mnt/adlsGen2/bronze/pharma_ref.xlsx", dtype={"drug_code":'str', "produit_pharma":'str'})

# COMMAND ----------

display(pharma_ref_koalasDF.head(3))

# COMMAND ----------

# MAGIC %md
# MAGIC Transform the data

# COMMAND ----------

# nothing...

# COMMAND ----------

# MAGIC %md
# MAGIC Load the data, store it back in the next storage folder
# MAGIC   * **bronze** (data ingestion: raw files, unstructured/structured, streaming data)
# MAGIC   * **silver** (transformation/feature engineering: merge, clean, transform, new features)
# MAGIC   * **gold** (machine learning ready data: labeled, predictors, balanced for training and testing)
# MAGIC   * **platinum** (aggregated results for visualizations)

# COMMAND ----------

# save parquet only in a folder (not filename.parquet !)
pharma_ref_koalasDF.to_parquet("/mnt/adlsGen2/bronze/pharma_ref_parquet")

# COMMAND ----------

# MAGIC %fs ls /mnt/adlsGen2/bronze