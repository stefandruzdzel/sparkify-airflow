from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """Operator that checks that data exists in all provided tables"""

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tables=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        """Operator that checks that data exists in all provided tables"""
        self.log.info("Creating Postgres hook for Redshift")
        redshift_hook = PostgresHook(self.conn_id)
                
        for table in self.tables:
            self.log.info("Querying counts in {table} table")
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError("{table} table has no results")
            if records[0][0] < 1:
                raise ValueError(f"{table} table has no rows")
            self.log.info("Data exists for {table} table. {records[0][0]} records")

