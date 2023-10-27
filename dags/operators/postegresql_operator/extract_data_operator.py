from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.postgres.hooks.postgres import PostgresHook


class QueryPostgres(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        table=None,
        last_extraction_timestamp=None,
        attributes=None,
        *args,
        **kwargs,
    ):
        super(QueryPostgres, self).__init__(*args, **kwargs)
        self.table = table
        self.last_extraction_timestamp = last_extraction_timestamp
        self.attributes = attributes

    def execute(self, context):
        postgres_hook = PostgresHook(postgres_conn_id="postgres_homero")

        sql_query = f"""
                    SELECT {self.attributes}
                    FROM {self.table}
                    WHERE updatedAt > '{self.last_extraction_timestamp}'
                """

        conn = postgres_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()

        data_list = []

        for data in result:
            record = dict(zip(self.attributes.split(", "), data))
            record["_id"] = record.pop("id")
            data_list.append(record)

        cursor.close()
        conn.close()

        return data_list
