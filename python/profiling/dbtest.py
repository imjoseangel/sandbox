import os
from databricks import sql
from memory_profiler import profile


@profile
def sqlconnect():
    try:
        with sql.connect(server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
                         http_path=os.getenv("DATABRICKS_HTTP_PATH"),
                         access_token=os.getenv("DATABRICKS_TOKEN")):

            ...

    except sql.exc.RequestError as e:
        print(e)


sqlconnect()
