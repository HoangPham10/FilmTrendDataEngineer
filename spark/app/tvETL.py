from models.TVModel import TVModel
import time
from datetime import datetime, timedelta
import pandas as pd
import os
import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, functions
from pyspark.sql.types import StringType


conf = SparkConf().setAppName("Tv Spark  App").setMaster("spark://spark:7077")


# Create Spark context
sc = SparkContext(conf = conf)
filename = sys.argv[1]

# Extract
end_date = time.strftime("%Y-%m-%d")
start_date = datetime.now() + timedelta(days=-30)
model = TVModel()
data = model.discover(start_date, end_date)


#Transforms 
genres = model.genres()
for v in data:
    v['genres'] = '|'.join([genres[id] for id in v['genre_ids']])
    v['origin_country'] = '|'.join(v['origin_country'])
df = pd.DataFrame.from_dict(data, orient='columns')
df = df.dropna()
df = df.drop('genre_ids', axis = 1)

# Load
os.makedirs(os.path.dirname(filename), exist_ok=True)
df.to_csv(filename, encoding='utf-8', index = False, header = True)

