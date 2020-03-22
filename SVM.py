from sklearn.svm import *
import pickle
import pandas as pd
import os
from globals import *
from sklearn.model_selection import train_test_split
from sklearn import metrics

class SVM:
    def __init__(self, model = None, C = 1.0, kernel='rbf', degree=3, gamma='scale'):
        if model == None:
            self.__model = SVC(C, kernel, degree, gamma, verbose=True)

    def get_model(self):
        return self.__model

    def load_model(self, filename):
        self.__model = pickle.load(open(filename, 'rb'))

    def save_model(self, filename):
        pickle.dump(self.__model, open(filename, 'wb'))

    def train(self, X_train, y_train):
        self.__model.fit(X_train, y_train)

    def test(self, X_test, y_test):
        y_pred = self.__model.predict(X_test)
        print("\tAccuracy: ", metrics.accuracy_score(y_test, y_pred))


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(PROCESSED_DATA_FOLDER, "tf-idf/tf_idf_representation.csv"))
    input = df.iloc[:, 0:-1]
    X = input.values
    output = df.iloc[:, -1]
    Y = output.values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

    for g in ['scale', 'auto']:
        for c in [0.01, 0.1, 1.0, 10.0, 100.0]:
            svm = SVM(model = None, C = c, gamma=g)
            svm.train(X_train, y_train)
            model_file = "model_rbf_" + str(c) + "_" + str(g) + ".bin"
            svm.save_model(os.path.join("models/svm", model_file))
            print("C = " + str(c) + ", gamma = " + str(g))
            svm.test(X_test, y_test)

