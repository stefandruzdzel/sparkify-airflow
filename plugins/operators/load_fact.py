from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """Load Fact Table Operator"""
    
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.query = query

    def execute(self, context):
        """Load Fact table"""
        self.log.info('Creating hook for fact table {self.table}')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Loading fact table {self.table}')
        redshift.run(f"INSERT INTO {self.table} {self.query}")
        self.log.info('{self.table} Fact table loading is completed')
