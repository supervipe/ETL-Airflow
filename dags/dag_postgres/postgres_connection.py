from datetime import datetime
from airflow import DAG
from operators.postegresql_operator.extract_data_operator import QueryPostgres
from operators.postegresql_operator.transform_data_operator import (
    TransformPostgresOperator,
)
from operators.load_data.load_data_mongodb import LoadMongo


class CreateDagPostgres:
    @staticmethod
    def create_dag(dag_id):
        dag_created = DAG(dag_id, default_args=default_dag_args)

        last_extraction_timestamp = "2023-10-09 17:37:26.952"

        user_attributes = "id, name, login, role, birth_date, created_at, updatedAt"
        course_student_attributes = "id, course_id, user_id"

        task_get_data_users = QueryPostgres(
            task_id="extract_data_users_postgres",
            table="users",
            attributes=user_attributes,
            last_extraction_timestamp=last_extraction_timestamp,
            dag=dag_created,
        )

        task_get_data_course = QueryPostgres(
            task_id="extract_data_course_postgres",
            table="course_student",
            attributes=course_student_attributes,
            last_extraction_timestamp=last_extraction_timestamp,
            dag=dag_created,
        )

        task_transform_data = TransformPostgresOperator(
            task_id="transform_data_postgres",
            dependent_tasks_ids=[
                "extract_data_users_postgres",
                "extract_data_course_postgres",
            ],
            dag=dag_created,
        )

        task_load_data = LoadMongo(
            task_id="load_data_mongodb",
            dependent_tasks_ids=["transform_data_postgres"],
            dag=dag_created,
        )

        (
            [task_get_data_users, task_get_data_course]
            >> task_transform_data
            >> task_load_data
        )

        return dag_created


default_dag_args = {
    "owner": "airflow",
    "job_name": "Connect_postgres",
    "retries": "0",
    "start_date": datetime.now(),
    "email": ["youremail@gmail.com"],
    "schedule_interval": "1 * * *",
}

dag = CreateDagPostgres.create_dag("dag_postgres")
