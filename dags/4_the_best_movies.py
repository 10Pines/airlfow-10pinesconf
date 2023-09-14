from datetime import datetime
from airflow.decorators import dag, task
from pandas import DataFrame, read_csv, read_json, read_sql_query
from airflow.providers.postgres.hooks.postgres import PostgresHook

# db connection
postgres_hook = PostgresHook("postgres")
connection = postgres_hook.get_sqlalchemy_engine()

# constants
MOVIES_INPUT_CSV_FILE = r"./dags/data/movies.csv"
MOVIES_OUTPUT_CSV_FILE = r"./dags/output/movies.csv"

@dag(start_date=datetime(2023, 9, 1), catchup=False)
def the_best_movies():
    @task()
    def filter_movies(**kwargs):
        task_instance = kwargs["ti"]

        def now():
            return datetime.now().strftime(r"%Y%m%d")

        def filter_movies_by_score_over_80(movies):
            return movies[movies["Audience score %"] >= 80]

        # Read movies
        movies = read_csv(MOVIES_INPUT_CSV_FILE)

        # Save filtered movies in temporary folder
        best_rated_tmp = f"./dags/tmp/best_rated_tmp_{now()}.json"
        filter_movies_by_score_over_80(movies).filter(
            items=["Film", "Genre", "Audience score %"]
        ).to_json(best_rated_tmp, orient="records")

        # Save path in xcom
        task_instance.xcom_push(key="movies", value= best_rated_tmp)

    @task()
    def insert_movies(**kwargs):
        task_instance = kwargs["ti"]

        # Get path from xcom
        best_rated_tmp = task_instance.xcom_pull(key="movies", task_ids="filter_movies")

        # Get filtered movies
        original_employees = read_json(best_rated_tmp).rename(
            columns={
                "Film": "film",
                "Genre": "genre",
                "Audience score %": "score",
            }
        )

        # Save movies to database
        original_employees.to_sql(
            "movies",
            con=connection,
            if_exists="replace",
            chunksize=500,
            method="multi",
        )

    @task()
    def read_movies():
        # Read movies from database
        query_movies = read_sql_query(
            """
            SELECT film, genre, score FROM "movies";
        """,
            connection,
        )

        # Output movies to new csv file
        DataFrame(query_movies).to_csv(MOVIES_OUTPUT_CSV_FILE)

    (
        filter_movies()
        >> insert_movies()
        >> read_movies()
    )


the_best_movies()
