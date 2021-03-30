from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

snowflake_connection_details = {
    "user": os.environ.get("SNOWFLAKE_USER"),
    "role": os.environ.get("SNOWFLAKE_ROLE", "SYSADMIN"),
    "password": os.environ.get("SNOWFLAKE_PASSWORD"),
    "account": str(os.environ.get("SNOWFLAKE_ACCOUNT"))
    + "."
    + os.environ.get("SNOWFLAKE_REGION", "eu-west-1"),
    "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
}

engine = create_engine(
    f'snowflake://{snowflake_connection_details["user"]}:{snowflake_connection_details["password"]}@{snowflake_connection_details["account"]}'
)

try:
    connection = engine.connect()
    results = connection.execute("show databases;").fetchmany(5)
    print(results)
finally:
    connection.close()
    engine.dispose()
