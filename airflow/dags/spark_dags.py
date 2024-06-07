from airflow import DAG
from datetime import datetime, timedelta
import time
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator


today = time.strftime("%Y-%m-%d")
# Spark config
spark_master = "spark://spark:7077"
movies_file_path = f"/opt/spark/resources/{today}/movies.csv"
tvs_file_path = f"/opt/spark/resources/{today}/tvs.csv"
cassandra_host = 'cassandra'
cassandra_password = 'cassandra'
cassandra_username = 'cassandra'
cassandra_keyspace = 'mainkeyspace'

# Description of the Direct Acyclic Graph
now = datetime.now()
dag = DAG(
    dag_id = 'spark_main',
    description = 'This DAG runs the principal Pyspark app to extract data from the movieDB and store it in Cassandra',
    default_args = dict(
        owner = 'airflow',
        email = ['hienjang910@gmail.com'],
        retries = 0,
        retry_delay = timedelta(minutes=1),
        start_date = datetime(now.year, now.month, now.day),
        schedule_interval = timedelta(days=1),
        catchup = False
    )
)

# Dummy operator to add an initial step
start = DummyOperator(task_id = "start", dag = dag)

# Spark job to extract the data from thedb movies, transform and load it in .csv file
movie_spark_submit = SparkSubmitOperator(
    task_id = 'movie_spark_job',
    application = '/opt/spark/app/movieETL.py',
    name = 'Movie Spark Extraction',
    conn_id = 'spark_conn',
    verbose = 1,
    conf = {"spark.master": spark_master},
    application_args = [movies_file_path],
    dag = dag
)


tv_spark_submit = SparkSubmitOperator(
    task_id = 'tv_spark_job',
    application = '/opt/spark/app/tvETL.py',
    name = 'TV Spark Extraction',
    conn_id = 'spark_conn',
    verbose = 1,
    conf = {"spark.master": spark_master},
    application_args = [tvs_file_path],
    dag = dag
)


# Bash command to load the .csv file to Cassandra
movie_cassandra_load = BashOperator(
    task_id = "movies_cassandra_load",
    bash_command = "cqlsh %s -u %s -p %s -k %s -e \"TRUNCATE TABLE Movies; COPY Movies(id, popularity, title, release_date, vote_average, vote_count, genres) FROM '/opt/spark/resources/%s/movies.csv' WITH DELIMITER = ',' AND HEADER = TRUE;\" " % (cassandra_host, cassandra_username, cassandra_password, cassandra_keyspace, today),
    dag = dag
)


tv_cassandra_load = BashOperator(
    task_id = "tvs_cassandra_load",
    bash_command = "cqlsh %s -u %s -p %s -k %s -e \"TRUNCATE TABLE TVs; COPY TVs(id, origin_country, popularity, name, first_air_date, vote_average, vote_count, genres) FROM '/opt/spark/resources/%s/tvs.csv' WITH DELIMITER = ',' AND HEADER = TRUE;\" " % (cassandra_host, cassandra_username, cassandra_password, cassandra_keyspace,today),
    dag = dag
)


end = DummyOperator(task_id = "end", dag = dag)


# Flow
#start >> [movie_spark_submit, tv_spark_submit]
#movie_spark_submit >> movie_cassandra_load
#tv_spark_submit >> tv_cassandra_load
#[movie_cassandra_load, tv_cassandra_load] >> end 

start >> movie_spark_submit >> movie_cassandra_load >> tv_spark_submit >> tv_cassandra_load >> end
