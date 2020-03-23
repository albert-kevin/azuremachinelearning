# Databricks notebook source
# MAGIC %md
# MAGIC Check the current mount points already active

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

# MAGIC %md
# MAGIC Example parameters, to show how it looks

# COMMAND ----------

adlsGen2AccountName = "datalake21032020"
adlsGen2Key = "Ck/4hMq3Zrzq5toZ96zE6cDncjbw2VdkR9ny1xXA3GLBwQXIv7V1ycSc/KpqyNRcoPWKtzKljjpcZVqjWOu+3Q=="
tenantId = "73b49191-8db3-45ab-87b3-b8f956ac123b"
clientId = "38c02221-4a41-4ec8-b8da-a81f16c38e82"
clientKey = "l]ABG6@Z/9r/chRfgoSdklmDR[MA-J1V"
fileSystemName = "datalake"
mount_dir = "/mnt/adlsGen2"

# COMMAND ----------

# MAGIC %md
# MAGIC Mount your ADLS Gen2 account with OAuth to DBFS, using the `configs`  

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": clientId,
           "fs.azure.account.oauth2.client.secret": clientKey,
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/" + tenantId + "/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://" + fileSystemName + "@" + adlsGen2AccountName + ".dfs.core.windows.net/",
  mount_point = mount_dir,
  extra_configs = configs)

# COMMAND ----------

# MAGIC %md
# MAGIC ADLS Gen2 has hierarchical namespace enabled to organize objects/files into a hierarchy of directories for efficient data access  
# MAGIC You cannot use the `wasb` or `wasbs` scheme to access the `blob.core.windows.net` endpoint  
# MAGIC It now will become a `abfs` or `abfss` mount point   
# MAGIC You must initialize a file system once and this code is included in `Cluster Config`  
# MAGIC   
# MAGIC `spark.serializer org.apache.spark.serializer.KryoSerializer`  
# MAGIC `spark.hadoop.fs.azure.createRemoteFileSystemDuringInitialization true`  
# MAGIC `spark.hadoop.fs.azure.account.key.datalake21032020.dfs.core.windows.net Ck/4hMq3Zrzq5toZ96zE6cDncjbw2VdkR9ny1xXA3GLBwQXIv7V1ycSc/KpqyNRcoPWKtzKljjpcZVqjWOu+3Q==`  
# MAGIC `spark.databricks.delta.preview.enabled true`

# COMMAND ----------

# MAGIC %md
# MAGIC verify new mount

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

# MAGIC %md
# MAGIC remove mount (if needed)

# COMMAND ----------

# dbutils.fs.unmount(mount_dir)