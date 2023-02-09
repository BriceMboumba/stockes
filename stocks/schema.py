import psycopg2 as pg
import pandas as pd
import pandas.io.sql as psql
import hashlib

# establishing the connection
connection = pg.connect(
    user="psc",
    password="psc2020@",
    host="localhost",
    port="5432",
    database="psc_db")

# define the path
path = "/home/brice/Téléchargements/app/database/TSLA.csv"


# path: path to the csv file to send stocks in the database when csv file is updated from the website
# loader_data function is in charge of updating the data from the csv file to the database.


def loader_data(path, connection) -> None:
    # Setting auto commit false
    connection.autocommit = True
    # Creating a cursor object using the cursor() method
    cur = connection.cursor()
    df = pd.read_csv(path)
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tuples from the dataframe values
    tuples = list(set([tuple(x) for x in df.to_numpy()]))
    # SQL query to execute
    try:
        for i in range(1, len(tuples) + 1):
            postgres_insert_query = """ INSERT INTO stocks(id, stock_date, open, high, low, close, adj_close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
            cur.execute(postgres_insert_query, (i,) + tuples[i])
            print("progressing: {}/{}".format(i, len(tuples)))
            connection.commit()

    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()


# get dataframe to the database
def dataset(connection):
    dataframe = psql.read_sql('SELECT * FROM stocks', connection)
    return dataframe


# send login information
def sender(login: tuple, connection):
    cursor = None
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        postgres_insert_query = """ INSERT INTO users (id, user_name, password) VALUES (%s, %s, %s)"""
        values = login
        cursor.execute(postgres_insert_query, values)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, pg.Error) as error:
        print("Failed to insert record into mobile table", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# get login information
def getter(sql_request):
    connection = pg.connect(
        user="psc",
        password="psc2020@",
        host="localhost",
        port="5432",
        database="psc_db")
    # Setting auto commit false
    connection.autocommit = True
    # Creating a cursor object using the cursor() method
    cursor = connection.cursor()
    # Retrieving data
    cursor.execute(sql_request)
    # Fetching 1st row from the table
    result = cursor.fetchall()
    # Commit your changes in the database
    connection.commit()
    # Closing the connection
    connection.close()
    # processing data from the data base
    return result


# count table for generate id
def count_id():
    connection = pg.connect(
        user="psc",
        password="psc2020@",
        host="localhost",
        port="5432",
        database="psc_db")
    connection.autocommit = True
    # Creating a cursor object using the cursor() method
    cursor = connection.cursor()
    # Retrieving data
    cursor.execute('''SELECT count(*) from users''')
    # Fetching 1st row from the table
    result = cursor.fetchall()
    # Commit your changes in the database
    connection.commit()
    # Closing the connection
    connection.close()
    return result[0][0]


def hasher(id: str, password: str):
    dataBase_password = password + id
    # Encoding the password
    hashed = hashlib.md5(dataBase_password.encode())
    return hashed.hexdigest()


# send data to the db
# loader_data(path, connection)
df = dataset(connection)
# sender(('1', 'junior', hasher('1', '123')), connection)
# sender(('2', 'laterreestronde1234@', hasher('2', '1234@1234@')), connection)
# getter(hasher('2', '1234@1234@'))