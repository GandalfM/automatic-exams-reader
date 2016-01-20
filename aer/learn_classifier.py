# USAGE
# python rbm.py --dataset data/digits.csv --test 0.4 --search 1

# import the necessary packages
from sklearn.externals import joblib
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import BernoulliRBM
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import ensemble
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
import argparse
import time
import os
from aer.ocr.ocr import Ocr

# IMPORTANT - RESULTS OF TEST
#
# SEARCHING LOGISTIC REGRESSION
# Fitting 3 folds for each of 3 candidates, totalling 9 fits
# [Parallel(n_jobs=-1)]: Done   9 out of   9 | elapsed:   16.0s finished
# done in 25.782s
# best score: 0.869
# LOGISTIC REGRESSION PARAMETERS
# 	 C: 100.000000
# SEARCHING RBM + LOGISTIC REGRESSION
# Fitting 3 folds for each of 81 candidates, totalling 243 fits
# [Parallel(n_jobs=-1)]: Done  34 tasks      | elapsed:  4.9min
# [Parallel(n_jobs=-1)]: Done 184 tasks      | elapsed: 30.0min
# [Parallel(n_jobs=-1)]: Done 243 out of 243 | elapsed: 41.4min finished
#
# done in 2537.621s
# best score: 0.760
# RBM + LOGISTIC REGRESSION PARAMETERS
# 	 logistic__C: 100.000000
# 	 rbm__learning_rate: 0.001000
# 	 rbm__n_components: 200.000000
# 	 rbm__n_iter: 20.000000

CLASSIFIER_FILE = "cls.pkl"
ALLOWED_DIRECTORY_NAMES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def load_mnist(should_disable_mnist):
    if should_disable_mnist:
        return [], []
    dataset = datasets.fetch_mldata("MNIST Original")
    features = np.array(dataset.data, 'int16')
    labels = dataset.target.tolist()
    hog_features = []

    # return a tuple of the data and targets
    for feature in features:
        fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1),
                 visualise=False)
        hog_features.append(fd)
    return hog_features, labels


def load_from_directory(main_directory):
    hog_features = []
    labels = []

    # add additional, real data
    ocr = Ocr()
    for directory in os.listdir(main_directory):
        path = os.path.join(main_directory, directory)
        if not os.path.isdir(path):
            continue
        if directory not in ALLOWED_DIRECTORY_NAMES:
            raise Exception("Name of directory isn't one of the allowed names. Only names with one sign 0-9 are allowed")

        expected = int(directory)

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            feature = ocr.features_from_file(file_path)
            hog_features.append(feature)
            labels.append(expected)
    return hog_features, labels


def load_digits(should_disable_mnist, additional):

    data, labels = load_mnist(should_disable_mnist)

    for directory in additional:
        dir_data, dir_label = load_from_directory(directory)

        data.extend(dir_data)
        labels.extend(dir_label)

    return np.array(data, 'float32'), np.array(labels, "int")


def scale(X, eps=0.001):
    # scale the data points s.t the columns of the feature space
    # (i.e the predictors) are within the range [0, 1]
    # return
    return (X - np.min(X, axis=0)) / (np.max(X, axis=0) + eps)


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--test", required=False, type=float,
                help="size of test split", default=0.1)
ap.add_argument("--disable-mnist", action="store_true", help="Disable MNIST database")
ap.add_argument("additional-directories", nargs="*", help="Include additional files. Each passed directory should contains ten directories with files. Name of subdirectory should have only one, recognized sign")
ap.add_argument("-m", "--mode", default="rfc",
                help="Program options:"
                     "\nrbm (default) - rbm + logistic regression"
                     "\nlog - logistic regression only"
                     "\nsearch - search for the best parameters in program"
                     "\nsvc - linear svc mode"
                     "\nrfc - random forest classifier"
                )
args = vars(ap.parse_args())

# load the digits dataset, convert the data points from integers
# to floats, and then scale the data s.t. the predictors (columns)
# are within the range [0, 1] -- this is a requirement of the
# Bernoulli RBM
(X, y) = load_digits(args["disable_mnist"], args["additional-directories"])

# construct the training/testing split
(trainX, testX, trainY, testY) = train_test_split(X, y,
                                                  test_size=args["test"], random_state=42)

# check to see if a grid search should be done
mode = args["mode"]
if mode == "search":
    # perform a grid search on the 'C' parameter of Logistic
    # Regression
    print("SEARCHING LOGISTIC REGRESSION")
    params = {"C": [1.0, 10.0, 100.0]}
    start = time.time()
    gs = GridSearchCV(LogisticRegression(), params, n_jobs=-1, verbose=1)
    gs.fit(trainX, trainY)

    # print diagnostic information to the user and grab the
    # best model
    print(("done in %0.3fs" % (time.time() - start)))
    print(("best score: %0.3f" % (gs.best_score_)))
    print("LOGISTIC REGRESSION PARAMETERS")
    bestParams = gs.best_estimator_.get_params()

    # loop over the parameters and print each of them out
    # so they can be manually set
    for p in sorted(params.keys()):
        print(("\t %s: %f" % (p, bestParams[p])))

    # initialize the RBM + Logistic Regression pipeline
    rbm = BernoulliRBM()
    logistic = LogisticRegression()
    classifier = Pipeline([("rbm", rbm), ("logistic", logistic)])

    # perform a grid search on the learning rate, number of
    # iterations, and number of components on the RBM and
    # C for Logistic Regression
    print("SEARCHING RBM + LOGISTIC REGRESSION")
    params = {
        "rbm__learning_rate": [0.1, 0.01, 0.001],
        "rbm__n_iter": [20, 40, 80],
        "rbm__n_components": [50, 100, 200],
        "logistic__C": [1.0, 10.0, 100.0]}

    # perform a grid search over the parameter
    start = time.time()
    gs = GridSearchCV(classifier, params, n_jobs=-1, verbose=1)
    gs.fit(trainX, trainY)

    # print diagnostic information to the user and grab the
    # best model
    print(("\ndone in %0.3fs" % (time.time() - start)))
    print(("best score: %0.3f" % (gs.best_score_)))
    print("RBM + LOGISTIC REGRESSION PARAMETERS")
    bestParams = gs.best_estimator_.get_params()

    # loop over the parameters and print each of them out
    # so they can be manually set
    for p in sorted(params.keys()):
        print(("\t %s: %f" % (p, bestParams[p])))

    # show a reminder message
    print("\nIMPORTANT")
    print("Now that your parameters have been searched, manually set")
    print("them and re-run this script with --mode rbm")

# otherwise, use the manually specified parameters
elif mode == "log":
    # evaluate using Logistic Regression and only the raw pixel
    # features (these parameters were cross-validated)
    logistic = LogisticRegression(C=100.0)
    logistic.fit(trainX, trainY)
    print("LOGISTIC REGRESSION ON ORIGINAL DATASET")
    print((classification_report(testY, logistic.predict(testX))))

    try:
        joblib.dump(logistic, CLASSIFIER_FILE, compress=3)
    except exc:
        print("Logistic save failed")

elif mode == "rbm":
    # initialize the RBM + Logistic Regression classifier with
    # the cross-validated parameters
    rbm = BernoulliRBM(n_components=200, n_iter=20,
                       learning_rate=0.001, verbose=True)
    logistic = LogisticRegression(C=100.0)

    # train the classifier and show an evaluation report
    classifier = Pipeline([("rbm", rbm), ("logistic", logistic)])
    classifier.fit(trainX, trainY)
    print("RBM + LOGISTIC REGRESSION")
    print((classification_report(testY, classifier.predict(testX))))

    try:
        joblib.dump(classifier, CLASSIFIER_FILE, compress=3)
    except exc:
        print("Pipeline classifier save failed")
elif mode == "svc":
    # source: http://hanzratech.in/2015/02/24/handwritten-digit-recognition-using-opencv-sklearn-and-python.html
    clf = LinearSVC()
    clf.fit(trainX, trainY)
    joblib.dump(clf, CLASSIFIER_FILE, compress=3)
elif mode == "rfc":
    # https://github.com/snazrul1/PyRevolution/blob/master/Puzzles/Handwriting_Recognition.ipynb
    clf = ensemble.RandomForestClassifier()
    clf.fit(trainX, trainY)
    joblib.dump(clf, CLASSIFIER_FILE, compress=3)