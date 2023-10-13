from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class PrintOperator(BaseOperator):
    @apply_defaults
    def __init__(self, dependent_tasks_ids=[], text_to_print=None, *args, **kwargs):
        super(PrintOperator, self).__init__(*args, **kwargs)
        self.dependent_tasks_ids = dependent_tasks_ids
        self.text_to_print = text_to_print

    def __print_text(self, context):
        join_string = ""
        for task_id in self.dependent_tasks_ids:
            text_to_print = context["ti"].xcom_pull(
                task_ids=task_id, key="return_value"
            )
            print(f"The last task {task_id}, printed: ", text_to_print)
            join_string += text_to_print + " "
        if self.text_to_print is not None:
            self.text_to_print = join_string + self.text_to_print
            print(self.text_to_print)

    def execute(self, context):
        self.__print_text(context)
        return self.text_to_print
