from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class TransformPostgresOperator(BaseOperator):
    @apply_defaults
    def __init__(self, dependent_tasks_ids=[], *args, **kwargs):
        super(TransformPostgresOperator, self).__init__(*args, **kwargs)
        self.dependent_tasks_ids = dependent_tasks_ids

    def __transform_data(self, context):
        join_data = []
        for task_id in self.dependent_tasks_ids:
            extracted_data = context["ti"].xcom_pull(
                task_ids=task_id, key="return_value"
            )
            join_data.append(extracted_data)

        transformed_data = []
        for data in join_data[0]:
            transformed_data.append(data)

        for data in join_data[1]:
            for transformed in transformed_data:
                if data["user_id"] == transformed["_id"]:
                    transformed["course_id"] = data["course_id"]
                    print(f"Data transformed: {transformed}")

        return transformed_data

    def execute(self, context):
        return self.__transform_data(context)
