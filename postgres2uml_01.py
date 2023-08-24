"""
You are a python programmer. Write a code that should connect to postgresql,
get the description of all tables and generate a text description
for each table for plantuml
"""
"""
Sure! Here's an example of how you can connect to a PostgreSQL database, 
retrieve the description of all tables, and generate a text description for each table in PlantUML format:

In this code, we first establish a connection to the PostgreSQL database using the psycopg2 library. 
You need to provide the appropriate values for the database, user, password, host, and port 
parameters based on your specific PostgreSQL setup.

Then, we call the get_table_descriptions function, which retrieves the descriptions 
for all the tables in the 'public' schema. 
The function executes a SQL query to fetch the table names and their descriptions using 
the information_schema.tables and pg_class tables.

Once we have the table descriptions, we call the generate_plantuml_description function, 
which takes the table descriptions and generates a text description in PlantUML format. 
It iterates over each table description and appends the table name and description to the 
Plant

"""

import psycopg2
from dotenv import load_dotenv
import os

def get_table_descriptions(conn):
    try:
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Get the description of all tables in the database
        cursor.execute("""
                    SELECT table_name, column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'rdb_tool';
                """)

        # Fetch all the table descriptions
        table_descriptions = cursor.fetchall()
        # print(f'table_descriptions={table_descriptions}')
        print(f'Fetching all the table descriptions started!')

        # Close the cursor and connection
        cursor.close()

        return table_descriptions

    except (Exception, psycopg2.Error) as e:
        print(f"An error occurred: {str(e)}")
        return []

def generate_plantuml_description(table_descriptions):
    plantuml_description = ""

    current_table = None
    for table_name, column_name, data_type in table_descriptions:
        if table_name != current_table:
            # Start a new table block in PlantUML
            if current_table:
                plantuml_description += "}\n\n"
            plantuml_description += f"entity {table_name} {{\n"
            current_table = table_name

        # Append the field description in PlantUML format
        plantuml_description += f"\t{column_name} : {data_type}\n"

    # Close the last table block in PlantUML
    if current_table:
        plantuml_description += "}\n\n"

    return plantuml_description

# Connect to the PostgreSQL database
try:
    # Loading values from .env file
    load_dotenv()
    DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT_NUMBER = os.environ.get("DB_PORT_NUMBER")

    connection = psycopg2.connect(
        database=DB_DATABASE_NAME,           # your-database-name
        user=DB_USERNAME,                    # your-username
        password=DB_PASSWORD,                # your-password
        host=DB_HOST,                        # localhost
        port=DB_PORT_NUMBER                  # your-port-number
    )

    # Get the table descriptions
    table_descriptions = get_table_descriptions(connection)

    # Generate PlantUML description for each table
    plantuml_description = generate_plantuml_description(table_descriptions)

    # Print the PlantUML description
    # print(plantuml_description)
    print(f'Creation of table descriptions for Plantuml started!')

    # Write the PlantUML description to a text file
    with open("table_descriptions.txt", "w") as file:
        file.write(plantuml_description)

    # Close the database connection
    connection.close()

except (Exception, psycopg2.Error) as e:
    print(f"An error occurred: {str(e)}")