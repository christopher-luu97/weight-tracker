import pandas as pd
import numpy as np
import psycopg2 as ps2

from config import *

def connect():
    con = None
    try:
        con = ps2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

        cur = con.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except (Exception, ps2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
            print("Database connection closed")

#con.commit() #commit edits to the database
#con.close() #remember to close the connection



if __name__ == '__main__':
    connect()