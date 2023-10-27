from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from operators.postegresql_operator.extract_data_operator import QueryPostgres
from operators.postegresql_operator.transform_data_operator import (
    TransformPostgresOperator,
)
from operators.load_data.load_data_mongodb import LoadMongo


class CreateDagPostgres:
    @staticmethod
    def create_dag(dag_id):
        last_extraction_timestamp = Variable.get(
            "last_successful_execution_date",
            default_var="2021-01-01 00:00:00.000000",
        )

        dag_created = DAG(dag_id, default_args=default_dag_args)

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

        task_update_time = PythonOperator(
            task_id="update_last_successful_execution_date",
            python_callable=lambda: Variable.set(
                "last_successful_execution_date",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            ),
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
            >> task_update_time
            >> task_transform_data
            >> task_load_data
        )

        Variable.set("last_execution_time", str(datetime.now()))
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

Variable.set("last_execution_time", str(dag.start_date))
