import asyncio
import os
import csv

from databases import Database

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
DATABASE_URI = 'sqlite+aiosqlite:///' + os.path.join(BASE_DIR, 'app.db')
CSV_FILE = os.path.join(BASE_DIR, 'sales_data_sample.csv')

def get_querys_from_csv():
    """
        Method that mapping csv 
        - create query table
        - storre all values in list of dictionaries
        - create insert query table
    """
    with open(CSV_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        columns_names = []
        values_rows = []
        for line_count, row in enumerate(csv_reader, start=0):
            if line_count == 0: # first row
                columns_names = row # store columns name 
                line_count += 1
            else: # all rows except first
                # generate list of dictionary that inserted later
                values_row = { columns_names[index]: str(value) for index, value in enumerate(row, start=0) } # dictionary with columns name: value column
                values_rows.append(values_row)
        
        # generate create query from columns name
        query_create = """CREATE TABLE sales (id INTEGER PRIMARY KEY AUTOINCREMENT, """
        len_columns = len( columns_names )
        for num, column_name in enumerate(columns_names, start=1):
            if num < len_columns: # every record add comma ,
                query_create += f" {column_name} VARCHAR(100), "
            else: # the last column name dont need put comma ,
                query_create += f" {column_name} VARCHAR(100) "
        query_create += f")"

        # generate insert query from columns name
        # EXAMPLE INSERT INTO table(id,name) VALUES (:id ,:name)
        query_insert = f"""INSERT INTO sales({",".join(columns_names)}) VALUES (:id ,:name)"""
        query_insert = f"""INSERT INTO sales({",".join(columns_names)}) VALUES ({":"+",:".join(columns_names)})"""

        return query_create, query_insert, values_rows

async def main(query_create, query_insert, values_rows):
    database = await start_connection()
    result = await createTable(database, query_create)
    result = await insert_data(database, query_insert, values_rows)
    result = await get_records(database)
    result = await close_connection(database)
    
async def start_connection( ):
    database = Database(DATABASE_URI)
    try:
        await database.connect()
        print('Connected to Database')
        return database
    except Exception as e:
        print(f'Connection to Database Failed with error\n {e}')
        return None

async def createTable(database, query_create):
    try:
        print('Created Table Successfully')
        await database.execute(query=query_create)
        return database
    except Exception as e:
        print(f'Connection to Database Failed with error\n {e}')

async def insert_data(database, query_insert, values_rows):
    try:
        print(f'Total rows {len(values_rows)}')
        print(f'query_insert {query_insert}')
        print(f'inserting data..')
        await database.execute_many(query=query_insert, values=values_rows)
        print('Inserted values in Table Successfully')
        return database
    except Exception as e:
        print(f'Connection to Database Failed with error\n {e}')

async def get_records(database):
    try:
        print(f"\nget records from table sales")
        query = """SELECT * FROM sales"""
        rows = await database.fetch_all(query=query)
        print(rows[0])
        print(rows[1])
        return database
    except Exception as e:
        print(f'Connection to Database Failed with error\n {e}')

async def close_connection(database):
    try:
        await database.disconnect()
        print(f"Connection closed")
        return True
    except Exception as e:
        print(f'Connection to Database Failed with error\n {e}')
        return False

if __name__ == '__main__':
    query_create, query_insert, values_rows = get_querys_from_csv()
    asyncio.run(main(query_create, query_insert, values_rows))
    