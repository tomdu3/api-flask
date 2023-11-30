from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json
import os


# load environment variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    import sys
    print('".env" is missing.')
    sys.exit(1)


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

books_list_file = os.path.join(BASE_DIR, 'assets/data/books_list.json')

if os.path.exists(books_list_file):
    with open(books_list_file, 'r') as file:
        books_list = json.load(file)


@app.route('/')
def index():
	return 'Hello World'

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            'Nothing Found', 404

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        new_id = books_list[-1]['id'] + 1

        new_obj = {
            'id': new_id,
            'author': new_author,
            'language': new_lang,
            'title': new_title,
        }
        books_list.append(new_obj)
        return jsonify(books_list), 201

@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
            pass
    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                return jsonify(updated_book)

    if request.method == 'DELETE':
        for index, book in enumerate[books_list]:
            books_list.pop(index)
            return jsonify(books_list)


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', '5000')),
        debug=True)