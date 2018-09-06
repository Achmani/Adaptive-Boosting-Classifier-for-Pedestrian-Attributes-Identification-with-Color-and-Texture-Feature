import graphviz
import pydot
import time
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from sklearn.externals import joblib
from sklearn import tree


def training(X=None, y=None, estimator=1, output='adaboost_dir.pkl'):
    rus = RandomUnderSampler(random_state=0)
    #smote_enn = SMOTEENN(random_state=0)
    #X_resampled, y_resampled = rus.fit_sample(X, y)
    X_resampled, y_resampled = rus.fit_sample(X, y)
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=estimator, algorithm='SAMME')
    clf.fit(X_resampled, y_resampled)
    #clf.fit(X, y)
    clf.score(X_resampled, y_resampled)
    joblib.dump(clf, output+".pkl")
    return clf


def eval_score(classifier, X, y):
    height = X.shape[0]
    # T = 0, F = 1
    result = np.zeros(5)  # TN,FP,FN,TP, Acc

    predicty = classifier.predict(X)
    for i in range(0, height):
        predicty_temp = predicty[i]
        # y_temp = y[i, index]
        y_temp = y[i]
        if (y_temp == 0):
            if (predicty_temp == 0):
                result[0] = result[0] + 1
            else:
                result[1] = result[1] + 1
        elif (y_temp == 1):
            if (predicty_temp == 0):
                result[2] = result[2] + 1
            else:
                result[3] = result[3] + 1
    result[4] = classifier.score(X,y)
    return result


def save(clf, filename):
    joblib.dump(clf, filename)


def load(filename):
    clf = joblib.load(filename)
    return clf


def exportgraphviz(clf, output):
    temp = 1
    for estimator in clf.estimators_:
        print(temp)
        tree.export_graphviz(estimator, out_file=str(output) + str(temp) + '.dot')
        temp = temp + 1


def estimatorweight(clf):
    for weight in clf.estimator_weights_:
        print(weight)
    return clf.estimator_weights_


def estimatorerror(clf):
    for error in clf.estimator_errors_:
        print(error)
    return clf.estimator_errors_


def gui_train(cf, mf, cv, wc, i_label):
    X_array = []
    if (cf != ""):
        X_array = np.load(cf)
        if (mf != ""):
            mf = np.load(mf)
            X_array = np.concatenate((X_array, mf), axis=1)
    else:
        X_array = mf
    train_array = np.load("crossvalidation" + str(cv) + "/train_array.npy")
    test_array = np.load("crossvalidation" + str(cv) + "/test_array.npy")
    label_subset = np.load("labelsubset-cv5/AllLabelSubset.npy")
    temp_result = np.zeros([cv, 4])
    for k in range(0, cv):
        X_train = X_array[train_array[k, :]]
        X_test = X_array[test_array[k, :]]
        y_train = label_subset[train_array[k, :], i_label]
        y_test = label_subset[test_array[k, :], i_label]
        # This point start calculating a computation time
        start = time.time()
        clf = training(X=X_train, y=y_train, estimator=wc)
        end = time.time()
        # end calculating
        temp = eval_score(clf, X_test, y_test)
        temp_result[k, :] = temp
    result = np.mean(temp_result, axis=0)
    result_string = "Time to training is " + str(end - start) + " milisecond /n"
    result_string = result_string + "From " + str(y_test.shape[0]) + " Data Test the result is : /n"
    result_string = result_string + "False True = " + str(result[0]) + "/n"
    result_string = result_string + "False False = " + str(result[1]) + "/n"
    result_string = result_string + "True False = " + str(result[2]) + "/n"
    result_string = result_string + "True True = " + str(result[3]) + "/n"


""""    print("Time to training is "+str(end-start)+" milisecond")
    print("From "+str(y_test.shape[0])+" Data Test the result is :")
    print("False True = "+str(result[0]))
    print("False False = "+str(result[1]))
    print("True False = "+str(result[2]))
    print("True True = "+str(result[3]))
"""
