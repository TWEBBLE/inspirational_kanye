from snowflake_connector import SnowflakeConnector, snowflake_connection_details
import os
from pathlib import Path
from dotenv import load_dotenv
import glob

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
create_db_kanye = snowflake_instance.run_sql(
    cursor, f"CREATE DATABASE IF NOT EXISTS kanye_{os.environ.get('ENV', 'DEV')};"
)
result = snowflake_instance.run_sql(cursor, "SHOW DATABASES;")
df = snowflake_instance.fetch_dataframe_from_sql(cursor, "SHOW DATABASES;")
# print(df)

create_schema_quotes = snowflake_instance.run_sql(
    cursor,
    f"CREATE SCHEMA IF NOT EXISTS kanye_{os.environ.get('ENV', 'DEV')}.quotes;",
)

table_ddl_statement = """ "quote" VARIANT """
create_table_complete = snowflake_instance.run_sql(
    cursor,
    f"CREATE TABLE IF NOT EXISTS kanye_{os.environ.get('ENV', 'DEV')}.quotes.complete ({table_ddl_statement});",
)

kanye_glob = glob.glob("kanye_quote_data/**/*.json", recursive=True)
# print(kanye_glob)

read = snowflake_instance.run_sql(cursor, f"LIST @~")

for quote in kanye_glob:
    snowflake_instance.run_sql(
        cursor, f"PUT file://{quote} @~ auto_compress=false;"
    )

    data_copier = snowflake_instance.run_sql(
        cursor,
        f"""COPY INTO kanye_{os.environ.get('ENV', 'DEV')}.quotes.complete from @~/{Path(quote).name} FILE_FORMAT = (TYPE = 'json');"""
    )
