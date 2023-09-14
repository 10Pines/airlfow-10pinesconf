from datetime import datetime
import time
from airflow.decorators import task, dag


@dag(start_date=datetime(2023, 9, 1), catchup=False)
def tasks_relations():
  @task()
  def say_hello():
    print("---------------------------------")
    print("hello world")
    print("---------------------------------")

  @task()
  def divide():
    print("---------------------------------")
    print("two tasks at the same time")
    print("---------------------------------")

  @task()
  def fast():
    print("---------------------------------")
    print("fast")
    print("---------------------------------")

  @task()
  def slow():
    print("---------------------------------")
    print("wait")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("3")
    print("---------------------------------")

  @task()
  def the_end():
    print("---------------------------------")
    print("end")
    print("---------------------------------")

  (say_hello()
   >> divide()
   >> [
     fast(),
     slow()
   ]
   >> the_end())


tasks_relations()
