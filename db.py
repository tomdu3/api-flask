import os
from dotenv import load_dotenv
import pymysql
# import sqlite3

# conn = sqlite3.connect("books.sqlite")

# load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    import sys
    print('".env" is missing.')
    sys.exit(1)


conn = pymysql.connect(
    host=os.environ.get('HOST'),
    database=os.environ.get('DATABASE'),
    user=os.environ.get('USER_NAME'),
    password=os.environ.get('PASSWORD'),
    charset='utf8',
    port=int(os.environ.get('PORT')),
    cursorclass=pymysql.cursors.DictCursor,
)

cursor = conn.cursor()
sql_query = """ CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""
cursor.execute(sql_query)
conn.close()