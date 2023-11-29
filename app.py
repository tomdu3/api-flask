from flask import Flask
from dotenv import load_dotenv
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




@app.route('/')
def index():
	return 'Hello World'


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP', '0.0.0.0'),
        port=int(os.environ.get('PORT', '5000')),
        debug=True)