from __future__ import annotations
from typing import Callable
from airflow import DAG
from airflow.models import XCom
from airflow.decorators import dag
from airflow.utils.session import provide_session
from sqlalchemy.orm.session import Session


@provide_session
def cleanup_xcom(context, session: Session | None = None):
    dag_id = context["task"].dag_id
    session and session.query(XCom).filter(XCom.dag_id == dag_id).delete()


def ephemeral_dag(
    before_on_success=None, after_on_success=None, **kwargs
) -> Callable[[Callable], Callable[..., DAG]]:
    """
    Python cleanup dag decorator. Wraps a function into an Airflow DAG that
    runs cleanup X_COM on success.
    Accepts kwargs for operator kwarg. Can be used to parameterize DAGs.

    :param dag_args: Arguments for DAG object
    :param dag_kwargs: Kwargs for DAG object.
    """

    def callback(context):
        if before_on_success:
            before_on_success(context)
        cleanup_xcom(context)
        if after_on_success:
            after_on_success(context)

    def wrapper(f: Callable) -> Callable[..., DAG]:
        return dag(**kwargs, on_success_callback=callback)(f)

    return wrapper
