from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2018, 11, 12),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'depends_on_past': False,
    'catchup': False
}

dag = DAG('etl_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          catchup=False
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table='staging_events',
    provide_context=True,
    redshift_conn_id='redshift',
    s3_bucket='udacity-dend',
    s3_key='log_data/{execution_date.year}/{execution_date.month}/{ds}-events.json',
    execution_date='{{ execution_date }}',
    aws_credentials_id='aws_credentials',
    region='us-west-2',
    extra_params="FORMAT AS JSON 's3://udacity-dend/log_json_path.json' \
                  TIMEFORMAT AS 'epochmillisecs' \
                  TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL"
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table='staging_songs',
    provide_context=True,
    redshift_conn_id='redshift',
    s3_bucket='udacity-dend',
    s3_key='song_data',
    execution_date='{{ execution_date }}',
    aws_credentials_id='aws_credentials',
    region='us-west-2',
    extra_params="FORMAT AS JSON 'auto' \
                  TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL"
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    table="songplays",
    query=SqlQueries.songplay_table_insert,
    append=True
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    table="users",
    query=SqlQueries.user_table_insert,
    append=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    table="songs",
    query=SqlQueries.song_table_insert,
    append=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    table="artists",
    query=SqlQueries.artist_table_insert,
    append=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    table="time",
    query=SqlQueries.time_table_insert,
    append=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    provide_context=True,
    redshift_conn_id='redshift',
    tables=["songplays", "users", "songs", "artists", "time"]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> stage_events_to_redshift
start_operator >> stage_songs_to_redshift

stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift  >> load_songplays_table

load_songplays_table >> load_song_dimension_table
load_songplays_table >> load_user_dimension_table
load_songplays_table >> load_artist_dimension_table
load_songplays_table >> load_time_dimension_table

load_song_dimension_table   >> run_quality_checks
load_user_dimension_table   >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table   >> run_quality_checks

run_quality_checks >> end_operator
