from airflow.decorators import task, dag
from datetime import datetime
import random


@dag(start_date=datetime(2023, 9, 1), catchup=False)
def xcom_dag():
  @task()
  def generate_random_number(**kwargs):
    task_instance = kwargs["ti"]
    num = random.randint(1, 10)
    print("---------------------------------")
    print("This is my random number: ", num)
    print("---------------------------------")
    task_instance.xcom_push(key="ranint", value=num)

  @task.branch()
  def branch_check_even_or_odd(**kwargs):
    task_instance = kwargs["ti"]
    num = task_instance.xcom_pull(key="ranint", task_ids="generate_random_number")
    if num % 2 == 0:
      return "print_even"
    else:
      return "print_odd"

  @task()
  def print_even():
    print("---------------------------------")
    print("EVEN")
    print("---------------------------------")

  @task()
  def print_odd():
    print("---------------------------------")
    print("ODD")
    print("---------------------------------")

  (generate_random_number()
   >> branch_check_even_or_odd()
   >> [
     print_even(),
     print_odd()
   ])


xcom_dag()
