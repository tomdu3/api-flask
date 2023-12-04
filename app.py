from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
import os
# import sqlite3
import pymysql

# load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# books_list_file = os.path.join(BASE_DIR, 'assets/data/books_list.json')

# if os.path.exists(books_list_file):
#     with open(books_list_file, 'r') as file:
#         books_list = json.load(file)

def db_connection():
    conn = None
    try:
        # conn = sqlite3.connect('books.sqlite')
        conn = pymysql.connect(
            host=os.environ.get('HOST'),
            database=os.environ.get('DATABASE'),
            user=os.environ.get('USER_NAME'),
            password=os.environ.get('PASSWORD'),
            charset='utf8',
            port=int(os.environ.get('PORT')),
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.error as e:
        print(e)
    return conn

# @app.route('/')
# def index():
# 	return 'Hello World'

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute('SELECT * FROM book')
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
            ]
        if books is not None:
            return jsonify(books)
        # if len(books_list) > 0:
        #     return jsonify(books_list)
        # else:
        #     'Nothing Found', 404

    if request.method == 'POST':
        print(request.form)
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        # new_id = books_list[-1]['id'] + 1  # it's added automatically
        sql = '''INSERT INTO book (author, language, title)
                 VALUES (?, ?, ?)'''
        cursor = conn.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f'Book with the id: {cursor.lastrowid} created successfully.', 201

        # new_obj = {
        #     'id': new_id,
        #     'author': new_author,
        #     'language': new_lang,
        #     'title': new_title,
        # }
        # books_list.append(new_obj)
        # return jsonify(books_list), 201

@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        cursor.execute('SELECT * FROM book WHERE id=?', (id,))
        rows = cursor.fetchall()
        for row in rows:
            book = rows
        if book is not None:
            return jsonify(book), 200
        else:
            return 'Something is wrong', 404

    if request.method == 'PUT':
        sql = '''UPDATE book
                 SET title=?,
                     author=?,
                     language=?
                 WHERE id=?'''
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
            'id': id,
            'author': author,
            'language': language,
            'title': title
        }
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)

    # if request.method == 'GET':
    #     for book in books_list:
    #         if book['id'] == id:
    #             return jsonify(book)
    #         pass
    # if request.method == 'PUT':
    #     for book in books_list:
    #         if book['id'] == id:
    #             book['author'] = request.form['author']
    #             book['language'] = request.form['language']
    #             book['title'] = request.form['title']
    #             updated_book = {
    #                 'id': id,
    #                 'author': book['author'],
    #                 'language': book['language'],
    #                 'title': book['title']
    #             }
    #             return jsonify(updated_book)

    if request.method == 'DELETE':
        sql = '''DELETE FROM book WHERE id=?'''
        conn.execute(sql, (id,))
        conn.commit()
        return f'The book with id: {id} has been deleted', 200

        # for index, book in enumerate[books_list]:
        #     books_list.pop(index)
        #     return jsonify(books_list)


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', '5000')),
        debug=True)