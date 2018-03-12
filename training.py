import numpy as np
import pandas as pd

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from scraper import to_document

# Generate dictionary of all words
def dic_process(dataset):
    all_words = []
    x = dataset.iloc[:, 0].values
    for line in x:
        all_words += line.split(';')
    return Counter(all_words)


# Generate features
def features(dataset):
    dictionary = dic_process(dataset)
    counter = CountVectorizer(vocabulary=dictionary.keys())
    documents = dataset.iloc[:, 0].values
    documents = list(map(lambda x: x.replace(';', ' '), documents))
    return counter.fit_transform(documents).toarray()


# Encode category data
def labels(dataset):
    labelEncoder_y = LabelEncoder()
    y = dataset.iloc[:, 1].values
    y = labelEncoder_y.fit_transform(y)
    return y


# Guessing
def guess(url, dataset, model):
    dictionary = dic_process(dataset)
    counter = CountVectorizer(vocabulary=dictionary.keys())
    matrix = counter.fit_transform([to_document(url)]).toarray()
    result = model.predict(matrix)
    return result[0] == 1, model.predict_proba(matrix)


def main():
    dataset = pd.read_csv('input.csv')
    X = features(dataset)
    y = labels(dataset)

    # Splitting data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Training
    model1 = MultinomialNB()
    model1.fit(X_train, y_train)
    result1 = model1.predict(X_test)

    model2 = GaussianNB()
    model2.fit(X_train, y_train)
    result2 = model2.predict(X_test)

    model3 = BernoulliNB()
    model3.fit(X_train, y_train)
    result3 = model3.predict(X_test)

    # Assert
    print("Confusion_matrix: MultinomialNB() ", confusion_matrix(y_test, result1))
    print("Confusion_matrix: GaussianNB()", confusion_matrix(y_test, result2))
    print("Confusion_matrix: BernoulliNB()", confusion_matrix(y_test, result3))

    print("acc of using model: MultinomialNB() is : ", accuracy_score(y_test, result1))
    print("acc of using model: GaussianNB() is : ", accuracy_score(y_test, result2))
    print("Confusion_matrix: BernoulliNB()", accuracy_score(y_test, result3))


# Process
main()
