"""
You are a python programmer. Write a code that should connect to postgresql,
get the description of all tables and generate a text description for each table for plantuml.
The result should be output to a text file.

Certainly! Here's an example of how you can connect to a PostgreSQL database,
retrieve the description of all tables, generate a text description for each table in PlantUML format,
and write the result to a text file:

In this code, we establish a connection to the PostgreSQL database by providing the necessary
database credentials.
We then call the get_table_descriptions function to retrieve the descriptions
of all tables in the database.

The generate_plantuml_description function takes the table descriptions and loops through each table,
creating a PlantUML description for each table.
It starts by indicating whether the table is an entity or an abstract class in PlantUML,
and then appends the table description and field descriptions.

Finally, we write the resulting PlantUML description to a text file named "table_descriptions.txt"
using a context manager.
We also catch any exceptions that may occur during the process and print an error message.

You will need to replace the placeholders
(your-database, your-username, your-password, localhost, and your-port-number)
with the appropriate values for your PostgreSQL database.

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
            SELECT table_name, table_type
            FROM information_schema.tables
            WHERE table_schema = 'rdb_tool' 
            AND table_type = 'BASE TABLE' 
            AND table_name not like '%_2023_%'
            order by table_name ;
        """)

        # Fetch all the table descriptions
        print(f'Fetching all the table descriptions started!')
        table_descriptions = cursor.fetchall()


        # Close the cursor
        cursor.close()

        return table_descriptions

    except (Exception, psycopg2.Error) as e:
        print(f"An error occurred: {str(e)}")
        return []

def generate_plantuml_description(table_descriptions, conn):
    plantuml_description_all = """@startuml
!define table(x) class x << (T,#FFAAAA) >>
!define TABLE(x) class x << (T,#FFAAAA) >>
!define TYPE(x) class x << (C,#FFAAAA) >>
!define primary_key(x) <u>x</u>
!define is_nullable(x) <u><b>x</b></u>
hide methods	
hide stereotypes
title Tables description 
"""
    plantuml_description = plantuml_description_all
    print(f'Creation of table descriptions for Plantuml started!')
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    for table_name, table_type in table_descriptions:
        print(f'table_name={table_name}')
        # Start a new table block in PlantUML
        plantuml_description_all += f"{'TABLE(' if table_type == 'BASE TABLE' else 'abstract'}{table_name}) {{\n"
        plantuml_description += f"{'TABLE(' if table_type == 'BASE TABLE' else 'abstract'}{table_name}) {{\n"

        # Append table description in PlantUML format
        # plantuml_description += "\t-- Table Description --\n"
        # Retrieve and append table description from database metadata or any other source

        # Append fields description in PlantUML
        # Get the columns of the table
        cursor.execute(f"""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}';""")

        # Fetch all the columns
        columns = cursor.fetchall()

        for column_name, data_type, is_nullable in columns:
            # Append the field description in PlantUML format
            if is_nullable == 'NO':
                plantuml_description_all += f"\tis_nullable({column_name}) : {data_type}\n"
            else:
                plantuml_description_all += f"\t{column_name} : {data_type}\n"

        # Close the table block in PlantUML
        plantuml_description_all += "}\n\n"
        plantuml_description += "}\n\n"

    plantuml_description_all += "\n@enduml\n"
    # Close the cursor
    cursor.close()
    return plantuml_description_all, plantuml_description

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
    plantuml_description_all,  plantuml_description = generate_plantuml_description(table_descriptions, connection)

    # Write the PlantUML description to a text file
    with open("table_descriptions.txt", "w") as file:
        file.write(plantuml_description)
    with open("table_descriptions_all.txt", "w") as file:
        file.write(plantuml_description_all)

    # Close the database connection
    connection.close()

except (Exception, psycopg2.Error) as e:
    print(f"An error occurred: {str(e)}")