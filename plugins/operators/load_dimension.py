from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """Load Dimension Table Operator"""
    
    ui_color = '#80BD9E'
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 query="",
                 append="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.query = query
        self.append = append


    def execute(self, context):
        """Load Dimension table"""
        self.log.info('Creating hook for dimension table {self.table}')

        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Clear the table if append = False
        if self.append == False:
            self.log.info("Clearing data from {self.table} table")
            redshift.run(f"TRUNCATE {self.table}")
        
        self.log.info('Loading dimension table {self.table} ')
        redshift.run(f"INSERT INTO {self.table} {self.query}")
        self.log.info('Loading is complete for dimension table {self.table}')