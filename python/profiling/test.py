from databricks import sql
from memory_profiler import profile


@profile
def sqlconnect():
    try:
        with sql.connect(server_hostname="adb-3763075652873156.16.azuredatabricks.net",
                         http_path="/sql/1.0/endpoints/ee8260e92561e43b",
                         access_token="DATABRICKS_TOKEN") as connection:

            ...

    except sql.exc.RequestError as e:
        print(e)


sqlconnect()
