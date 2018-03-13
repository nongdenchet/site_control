import pickle
import pandas as pd
import json
import hashlib
import uuid
import os

from flask import Flask, jsonify, request
from training import guess
from sklearn.externals import joblib
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)
dataset = pd.read_csv('data/input.csv')
model = joblib.load('model.pkl')
print('Finish loading')

ignores = ['youtube.com']

# Format http
def format_url(url):
    if '//' not in url:
        return '%s%s' % ('http://', url)
    else:
        return url


# Encode data
def hash(data, salt):
    encoded = (data + salt).encode('utf-8')
    hashed_data = hashlib.sha512(encoded).hexdigest()
    return hashed_data


@app.route('/')
def validate():
    try:
        secret = request.args.get('secret')
        secret = '' if secret is None else secret
        salt = uuid.uuid4().hex
        authenticated = hash(secret, salt) != hash(os.getenv('SECRET'), salt)

        if (authenticated):
            return jsonify({ 'error': 'Wrong secret' }), 403
        else:
            url = format_url(request.args.get('url'))
            for i in ignores:
                if i in url:
                    return jsonify({ 'result': False, 'positive': '0.0%', 'negative': '100.0%' })
            
            result = guess(url, dataset, model)
            positive = str(result[1][0][1] * 100) + '%'
            negative = str(result[1][0][0] * 100) + '%'
            data = { 
                'result': str(result[0]) == 'True', 
                'positive': positive, 
                'negative': negative 
            }
            print(data)
            return jsonify(data)
    except Exception as error:
        print(error)
        return jsonify({ 'error': 'Cannot inspect url' }), 400


if __name__ == '__main__':
  app.run()

