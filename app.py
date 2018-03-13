import pickle
import pandas as pd
import json

from flask import Flask, jsonify, request
from training import guess
from sklearn.externals import joblib

app = Flask(__name__)
dataset = pd.read_csv('data/input.csv')
model = joblib.load('model.pkl')
print('Finish loading')

# Format http
def format_url(url):
    if '//' not in url:
        return '%s%s' % ('http://', url)
    else:
        return url


@app.route('/')
def validate():
    try:
        url = format_url(request.args.get('url'))
        result = guess(url, dataset, model)
        positive = str(result[1][0][1] * 100) + '%'
        negative = str(result[1][0][0] * 100) + '%'
        data = { 'result': bool(str(result[0])), 'positive': positive, 'negative': negative }
        print(data)
        return jsonify(data)
    except Exception as error:
        print(error)
        return jsonify({ 'error': 'Cannot inspect url' })


if __name__ == '__main__':
  app.run()

