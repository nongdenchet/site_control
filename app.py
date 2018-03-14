import pickle
import pandas as pd
import json
import hashlib
import os
import json

from flask import Flask, jsonify, request, render_template
from training import guess
from sklearn.externals import joblib
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS

# Load env
load_dotenv(find_dotenv())

# Load app
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
dataset = pd.read_csv('data/input.csv')
model = joblib.load('model.pkl')

# TODO: need to improve
ignores = ['youtube.com']

def format_url(url):
    if '//' not in url:
        return '%s%s' % ('http://', url)
    else:
        return url


def hash(data):
    encoded = data.encode('utf-8')
    hashed_data = hashlib.sha512(encoded).hexdigest()
    return hashed_data


def predict(_secret, _url):
    secret = '' if _secret is None else _secret
    authenticated = hash(secret) != os.getenv('SECRET_HASH')

    if (authenticated):
        return None, 403
    else:
        url = format_url(_url)
        print(url)
        for i in ignores:
            if i in url:
                return (False, [[100.0, 0.0]]), 200
        return guess(url, dataset, model), 200


@app.route('/')
def home():
    return render_template('index.html', url='', clazz='teal', title='Check adult website')


@app.route('/', methods=['POST'])
def validate():
    url = request.form['url']
    secret = os.getenv('SECRET')
    
    try:
        prediction = predict(secret, url)
        clazz = 'red darken-4' if prediction[0][0] else 'teal'
        title = 'This site is dangerous' if prediction[0][0] else 'This site is safe'
        print(prediction)
        return render_template('index.html', url=url, clazz=clazz, title=title)
    except Exception as error:
        print(error)
        return render_template('index.html', url=url, clazz='lime darken-3', title='Cannot inspect url')


@app.route('/api/validate', methods=['POST'])
def api_validate():
    try:
        data = data = request.get_json()
        prediction = predict(data['secret'], data['url'])

        if (prediction[1] == 403):
            return jsonify({ 'error': 'Wrong secret' }), 403
        else:
            result = prediction[0]
            data = {
                'result': str(result[0]) == 'True', 
                'positive': str(result[1][0][1] * 100) + '%', 
                'negative': str(result[1][0][0] * 100) + '%' 
            }
            print(prediction)
            return jsonify(data), 200
    except Exception as error:
        print(error)
        return jsonify({ 'error': 'Cannot inspect url' }), 400


if __name__ == '__main__':
  app.run(host='0.0.0.0')

