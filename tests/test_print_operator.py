import unittest
from unittest.mock import Mock
from airflow import DAG
from datetime import datetime
from operators.print_operator.print_operator import PrintOperator


class TestPrintOperator(unittest.TestCase):
    def test_execute(self):
        dag = DAG("test_dag", start_date=datetime(2023, 1, 1))

        first_print = PrintOperator(
            task_id="first_print_task",
            text_to_print="Hello, World!",
            dag=dag,
        )

        second_print = PrintOperator(
            task_id="second_print_task",
            dependent_tasks_ids=["first_print_task"],
            text_to_print="Hello, World!",
            dag=dag,
        )

        context = {"ti": Mock(xcom_pull=Mock(return_value="Hello, World!"))}
        result = first_print.execute(context)
        self.assertEqual(result, "Hello, World!")
        result = second_print.execute(context)
        self.assertEqual(result, "Hello, World!" + " Hello, World!")

        context["ti"].xcom_pull.assert_any_call(
            task_ids="first_print_task", key="return_value"
        )
