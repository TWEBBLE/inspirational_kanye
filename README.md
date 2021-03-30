# Kanye rest data pipeline

This project connects to the kanye.rest API, receives Kanye quotes, process them, stores them in a Snowflake data warehouse and creates a wordcloud of his most commonly used phrases.

## How to run the code
This project relies on environment variables for user authentication. You will need to export the following variables to your shell or include them in the `.env` file:

    SNOWFLAKE_USER=
    SNOWFLAKE_ROLE=
    SNOWFLAKE_PASSWORD=
    SNOWFLAKE_ACCOUNT=
    SNOWFLAKE_REGION=
    SNOWFLAKE_WAREHOUSE=

### Dependencies

    pip3 install --requirement requirements.txt

### To run the code use:

    python3 query_snowflake.py

This will populate your database on snowflake with data on every match in FIFA World Cup history.

## Continuous Integration

The project includes automated deployment pipelines using GitHub Actions.

### User
This is dependent on having a programmatic user, it must be created in Snowflake for the deployment to run. The user should be stored in GitHub secrets.

SNOWFLAKE_USER = CI_CD
SNOWFLAKE_PASSWORD = "yourpass"

### Warehouse
The pipelines depends on a warehouse, create that with the following code:

    CREATE OR REPLACE WAREHOUSE CI_CD WITH WAREHOUSE_SIZE ='X-SMALL';
