from databricks import sql
from memory_profiler import profile


@profile
def sqlconnect():
    try:
        with sql.connect(server_hostname="xx.azuredatabricks.net",
                         http_path="/sql/1.0/endpoints/xx",
                         access_token="DATABRICKS_TOKEN") as connection:

            ...

    except sql.exc.RequestError as e:
        print(e)


sqlconnect()
