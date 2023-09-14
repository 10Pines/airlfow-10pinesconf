from unittest import mock

import pytest
from airflow.models.connection import Connection
from airflow.models import DagBag

conn = Connection(
    conn_type="postgres",
    login="postgres",
    host="postgrest",
)
conn_uri = conn.get_uri()
with mock.patch.dict("os.environ", AIRFLOW_CONN_POSTGRES=conn_uri):
    assert "postgres" == Connection.get("postgres").login

@pytest.fixture()
def dagbag(request):
    rootdir = request.config.rootdir

    return DagBag(
        include_examples=False,
        dag_folder=f"{rootdir}/../dags",
        read_dags_from_db=False
    )


def test_dag_loaded(dagbag: DagBag):
    dag = dagbag.get_dag(dag_id="xcom_dag")
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 4


