from snowflake_connector import SnowflakeConnector, snowflake_connection_details
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

snowflake_instance = SnowflakeConnector(snowflake_connection_details)
cursor = snowflake_instance.set_session_parameters(
    role="SYSADMIN", warehouse="COMPUTE_WH"
)
create_view = snowflake_instance.run_sql(
    cursor, f'''CREATE VIEW IF NOT EXISTS "KANYE_{os.environ.get("ENV", "DEV")}"."QUOTES"."Inspirational_Teachings_of_Mr_West" AS (SELECT "quote": quote AS Quotes FROM "KANYE_DEV"."QUOTES"."COMPLETE");''')
