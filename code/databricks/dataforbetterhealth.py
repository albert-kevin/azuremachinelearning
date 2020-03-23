# Databricks notebook source
# MAGIC %md
# MAGIC ## Transform data

# COMMAND ----------

# MAGIC %md
# MAGIC Load python packages and restart kernel

# COMMAND ----------

dbutils.library.installPyPI("koalas")
dbutils.library.installPyPI("xlrd")
#dbutils.library.installPyPI("xlrd")
dbutils.library.restartPython()

# COMMAND ----------

import databricks.koalas as pd     #preferred method (default: import databricks.koalas as ks)
import numpy as np

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

db_v2_koalasDF = pd.read_parquet("/mnt/adlsGen2/bronze/docph/DB_V2.parquet")

# COMMAND ----------

pharma_ref_koalasDF = pd.read_excel("/dbfs/mnt/adlsGen2/bronze/pharma_ref.xlsx", dtype={"drug_code":'str', "produit_pharma":'str'})

# COMMAND ----------

reimb_category_koalasDF = pd.read_excel("/dbfs/mnt/adlsGen2/bronze/reimb_category.xlsx", dtype={"reimbt_cat_id":'str'})

# COMMAND ----------

display(db_v2_koalasDF.head(3))

# COMMAND ----------

display(pharma_ref_koalasDF.head(3))

# COMMAND ----------

display(reimb_category_koalasDF.head(3))

# COMMAND ----------

# MAGIC %md
# MAGIC Transform the data

# COMMAND ----------

db_v2_koalasDF = db_v2_koalasDF.drop_duplicates()
db_v2_koalasDF = db_v2_koalasDF.drop('year', axis=1)
db_v2_koalasDF = db_v2_koalasDF.drop('account_yy_ss', axis=1)

# COMMAND ----------

pharma_ref_koalasDF = pharma_ref_koalasDF.drop_duplicates()

# COMMAND ----------

reimb_category_koalasDF = reimb_category_koalasDF.drop_duplicates()
reimb_category_koalasDF = reimb_category_koalasDF.drop('min_pct', axis=1)
reimb_category_koalasDF = reimb_category_koalasDF.drop('reimbt_cat_desc_fr', axis=1)
reimb_category_koalasDF_dict = {'nd':'other', 'A':'A', 'B':'B', 'Cat 1':'other', 'Cat 2 (A)':'other', 'Cat 3':'other', 'Cat 4':'other',
       'Cat 5 (D)':'other', 'C':'C', 'Cs':'C', 'Cx':'C', 'Cxg':'C', 'D':'D', 'Csg':'C', 'Ag':'A', 'Bg':'B', 'Cg':'C',
       'Forf Ant':'other', 'Nutri Par':'other', 'Br':'other', 'Ar':'other', 'Cr':'C', 'Csr':'C', 'Cxr':'C',
       'Forf Adm':'other', 'Forf BH':'forf', 'V08':'other', 'Fa':'other', 'Fb':'other', 'Forf 1-3':'other',
       'Forf 4-':'other', 'Ri-D11':'other', 'Ri-T1':'other', 'Ri-T2':'other', 'Ri-T3':'other', 'Ri-D5':'other', 'Ri-D7':'other',
       'Ri-D2':'other', 'Ri-D9':'other', 'Ri-D6':'other', 'Ri-D10':'other', 'Ri-D3':'other', 'Ri-D1':'other', 'Ri-D8':'other',
       'Ri-T4':'other', 'Ri-D4':'other', 'Forf PET':'other', '90-A':'A', '90-B':'B', '90-Fa':'other', '90-Fb':'other',
       'Ri-T5':'other', 'Ri-T6':'other', 'Ri-T7':'other', 'Ri-T8':'other', '90-C':'C', '90-Cs':'C', '90-Cx':'C'}
reimb_category_koalasDF["reimbt_crit_long"] = reimb_category_koalasDF["reimbt_crit_long"].map(reimb_category_koalasDF_dict)

# COMMAND ----------

# MAGIC %md
# MAGIC MERGE left join these dataframes

# COMMAND ----------

df = pd.merge(db_v2_koalasDF, pharma_ref_koalasDF, how="left", left_on="drug_code", right_on="drug_code")

# COMMAND ----------

df = pd.merge(df, reimb_category_koalasDF, how="left", left_on="reimbt_cat_id", right_on="reimbt_cat_id")

# COMMAND ----------

# MAGIC %md
# MAGIC Cleaning Phase 1

# COMMAND ----------

#df.columns

# COMMAND ----------

#df = df.astype({'Type':'category', 'type_drug_code':'category', 'statut_produit_pharma':'category',
#               'orphan_flag':'bool', 'chapter_IV_bis_flag':'bool', 'reimbt_cat_acute_yn':'bool',
#               'reimbt_cat_chron_yn':'bool', 'reimbt_cat_psy_yn':'bool', 'reimbt_cat_fixed_rate_yn':'bool',
#               'relative_care_yn':'bool', 'ami_ziv_amount_null_yn':'bool', 'not_reimbursed_null_yn':'bool', 'fee_cat':'category'})

# COMMAND ----------

#df["fee_cat"].head(5)

# COMMAND ----------

# MAGIC %md
# MAGIC Our domain expert suggest to only keep these columns

# COMMAND ----------

df = df[['patient_cat', 'province', 'type', 'hosp_serv_id', 'reimbt_cat_id', 'drug_code',
       'realization_date', 'quantity', 'amount_reimb', 'amount_not_reimb',
       'trim_pharma', 'produit_pharma', 'type_drug_code',
       'famille_produit_pharma', 'drug_name_aggregated',
       'conditionnement', 'mode_administration',
       'date_debut_rembourse', 'statut_produit_pharma', 'code_atc',
       'code_atc_5', 'code_atc_4', 'code_atc_3', 'code_atc_1', 'DDD',
       'nombre_prises', 'orphan_flag', 'chapter_IV_bis_flag',
       'link_same_tablet', 'dbegin', 'dend',
       'reimbt_cat_desc_nl', 'reimbt_crit_long', 'reimbt_crit_short',
       'reimbt_cat_fixed_rate_yn', 'fee_cat']]

# COMMAND ----------

df.drop_duplicates(inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC Cleaning Phase 2

# COMMAND ----------

# MAGIC %md
# MAGIC patient_cat
# MAGIC only keep hospitalised data, ignore ambulant data

# COMMAND ----------

df = df[ (df["patient_cat"] == 'HOSP') ]
df = df.drop("patient_cat", axis=1)
# removing all the duplicate rows
df.drop_duplicates(inplace=True)

# COMMAND ----------

# MAGIC %md
# MAGIC Province

# COMMAND ----------

#df["province"].unique()

# COMMAND ----------

province = {'Anvers':'Antwerpen',
            'Brabant Flamand':'Vlaams-Brabant',
            'Brabant Wallon':'Waals-Brabant',
            'Bruxelles-Capitale':'Brussel',
            'Flandre Occidentale':'West-Vlaanderen',
            'Flandre orientale':'Oost-Vlaanderen',
            'Hainaut':'Henegouwen',
            'Limbourg':'Limburg',
            'Liège':'Luik',
            'Luxembourg':'Luxemburg',
            'Namur':'Namen'}

# COMMAND ----------

# replace the values
df["province"] = df["province"].map(province)

# COMMAND ----------

# MAGIC %md
# MAGIC Type

# COMMAND ----------

# keep General types, ignore all psycholocal drugs (9%)
df = df[(df["type"] == 'Général')]

# COMMAND ----------

# remove the column it has all the same values
df = df.drop("type", axis=1)

# COMMAND ----------

#df.shape

# COMMAND ----------

# removing all the duplicate rows
df.drop_duplicates(inplace=True)
#display(df.shape)

# COMMAND ----------

# MAGIC %md
# MAGIC realization_date

# COMMAND ----------

# here we replace for example 20132 into 2013 as being the year 2013 ...
df = df.astype({"realization_date":'str'})
df["realization_date"] = df["realization_date"].str.slice(start=0, stop=4, step=1)

# COMMAND ----------

# here we will sort the realization_date "years" first,
# then we sort per year per Province per hospital per remiburce category (let's add quantity for fun)
# ascending fashion
df.sort_values(by=['realization_date', 'province', 'hosp_serv_id', 'reimbt_cat_id', 'quantity'], ascending=True, inplace=True)

# COMMAND ----------

df.reset_index(inplace=True, drop=True)

# COMMAND ----------

# MAGIC %md
# MAGIC quantity

# COMMAND ----------

#df.columns

# COMMAND ----------

#df["quantity"].dtypes

# COMMAND ----------

df = df.astype({"quantity":"int"})

# COMMAND ----------

x = np.random.randn(5)

# COMMAND ----------

np.abs(1.2)

# COMMAND ----------



# COMMAND ----------

#df["quantity"][0]

# COMMAND ----------

#quantityDF = df["quantity"].head(500)

# COMMAND ----------

#quantityDF.head(5)

# COMMAND ----------

#df.info()

# COMMAND ----------

df.to_parquet("/mnt/adlsGen2/silver/dataforbetterhealth_parquet")

# COMMAND ----------

# put positive values in "quantity_delivered" and the rest zero
# put negative values in "quantity_returned" and the rest zero
# and make all values absolute
# (2h to run!)

df[["quantity_returned", "quantity_delivered"]] = df.apply(lambda x: pd.Series([np.abs(x["quantity"]), 0]
                                                  if x["quantity"] < 0
                                                  else [0, np.abs(x["quantity"])],
                                                  index=['quantity_returned', 'quantity_delivered']), axis=1)

# COMMAND ----------

# MAGIC %md
# MAGIC amount_reimb

# COMMAND ----------

# grab the negative values
negative_amount_reimb = df[ (df["amount_reimb"] < 0) ]
# store the whole table to *.csv
negative_amount_reimb.to_csv('../data/dataset/bad_negative_amount_reimb.csv', index=False)

# COMMAND ----------



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