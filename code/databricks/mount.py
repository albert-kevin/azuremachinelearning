# Databricks notebook source
# MAGIC %fs mounts

# COMMAND ----------

adlsGen2AccountName = "datalake21032020"
adlsGen2Key = "Ck/4hMq3Zrzq5toZ96zE6cDncjbw2VdkR9ny1xXA3GLBwQXIv7V1ycSc/KpqyNRcoPWKtzKljjpcZVqjWOu+3Q=="
tenantId = "73b49191-8db3-45ab-87b3-b8f956ac123b"
clientId = "38c02221-4a41-4ec8-b8da-a81f16c38e82"
clientKey = "l]ABG6@Z/9r/hX7EK0zavK5Nx[MA-J1V"
fileSystemName = "datalake"
mount_dir = "/mnt/adlsGen2"

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

# MAGIC %fs mounts

# COMMAND ----------

# dbutils.fs.unmount(mount_dir)