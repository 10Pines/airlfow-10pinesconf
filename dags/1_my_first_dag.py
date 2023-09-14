from datetime import datetime

from airflow.decorators import task, dag


@dag(start_date=datetime(2023, 9, 1), catchup=False)
def my_first_dag():
  @task()
  def say_hello():
    print("---------------------------------")
    print("hello world")
    print("---------------------------------")

  say_hello()


my_first_dag()
