import numpy as np
import pandas as pd

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


# Training
def main():
    # Prepare data
    dataset = pd.read_csv('input.csv')
    X = features(dataset)
    y = labels(dataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Naive Bayes
    from sklearn.naive_bayes import MultinomialNB
    model1 = MultinomialNB()
    model1.fit(X_train, y_train)
    result1 = model1.predict(X_test)
    
    # KNN
    from sklearn.neighbors import KNeighborsClassifier
    model2 = KNeighborsClassifier(n_neighbors=10, metric='minkowski', p=2)
    model2.fit(X_train, y_train)
    result2 = model2.predict(X_test)

    # SVM
    from sklearn.svm import SVC
    model3 = SVC(kernel='rbf', random_state=0)
    model3.fit(X_train, y_train)
    result3 = model3.predict(X_test)
    
    # Random Forest
    from sklearn.ensemble import RandomForestClassifier
    model4 = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    model4.fit(X_train, y_train)
    result4 = model4.predict(X_test)

    # Assert
    print("Confusion_matrix: MultinomialNB ", confusion_matrix(y_test, result1))
    print("Confusion_matrix: KNeighborsClassifier ", confusion_matrix(y_test, result2))
    print("Confusion_matrix: SVC ", confusion_matrix(y_test, result3))
    print("Confusion_matrix: RandomForestClassifier ", confusion_matrix(y_test, result3))
    
    print("acc of using model: MultinomialNB is: ", accuracy_score(y_test, result1))
    print("acc of using model: KNeighborsClassifier is: ", accuracy_score(y_test, result2))
    print("acc of using model: SVC is: ", accuracy_score(y_test, result3))
    print("acc of using model: RandomForestClassifier is: ", accuracy_score(y_test, result4))
    
    