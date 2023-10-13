from airflow import DAG
from operators.print_operator.print_operator import PrintOperator


class CreateDagPrintExample:
    @staticmethod
    def create_dag(dag_id, default_dag_args):
        dag_created = DAG(dag_id, default_args=default_dag_args)

        task_print_text_welcome = PrintOperator(
            task_id="print_welcome",
            text_to_print="Welcome to airflow project!",
            dag=dag_created,
        )

        text_to_print = (
            "Just write something to print in the task execution"
            + "{{ params.text_to_print }}"
        )
        task_print_text_something = PrintOperator(
            task_id="print_something",
            dependent_tasks_ids=["print_welcome"],
            text_to_print=text_to_print,
            dag=dag_created,
        )

        task_print_text_welcome >> task_print_text_something
        return dag_created


default_dag_args = {
    "owner": "airflow",
    "job_name": "Print_Text",
    "retries": "0",
    "start_date": "2023-09-28",
    "email": ["youremail@gmail.com"],
    "schedule_interval": "1 * * *",
}

dag = CreateDagPrintExample.create_dag("dag_print_example", default_dag_args)

if __name__ == "__main__":
    dag.test(
        run_conf={"text_to_print": "Hello, World!"},
    )
