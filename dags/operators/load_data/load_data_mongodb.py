from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.providers.mongo.hooks.mongo import MongoHook
import json


class LoadMongo(BaseOperator):
    @apply_defaults
    def __init__(self, dependent_tasks_ids=[], *args, **kwargs):
        super(LoadMongo, self).__init__(*args, **kwargs)
        self.dependent_tasks_ids = dependent_tasks_ids

    def execute(self, context):
        mongo_hook = MongoHook(conn_id="datalake_mongodb")

        transformed_data = context["ti"].xcom_pull(
            task_ids=self.dependent_tasks_ids[0], key="return_value"
        )

        conn = mongo_hook.get_conn()
        database_name = "datalake-mongodb"
        collection_name = "users"
        data_json = json.dumps(transformed_data, default=str)
        data_dict = json.loads(data_json)

        for data in data_dict:
            unique_id = data.get("_id")
            filter_query = {"_id": unique_id}

            result = conn[database_name][collection_name].update_one(
                filter_query, {"$set": data}, upsert=True
            )

            if result.upserted_id:
                print(f"Data inserted: {result.upserted_id}")
            else:
                print(f"Data updated: {unique_id}")

        return "Data loaded/updated successfully"
