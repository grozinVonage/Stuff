
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os
import librosa
import numpy as np
from urban_sound_challenge import task_imp
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB


def generate_classification_results(y_test, res):
    report = str(accuracy_score(y_test, res))
    report += "\n"
    report += classification_report(y_test, res)
    report += "\n"
    report += str(confusion_matrix(y_test, res))
    report += "\n"
    return report


def random_forest(extract_features_function, number_of_features):
    print("Starting Random Forest...\n")

    print("Preparing the train data\n")
    x_train, y_train = get_data("data/Train/", extract_features_function, number_of_features, 'data/train_labels.csv')

    # TODO: Task 2 (b)
    # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn-ensemble-randomforestclassifier
    print("Classify\n")
    clf = RandomForestClassifier()
    clf.fit(x_train, y_train)

    print("Preparing the test data\n")
    x_test, y_test = get_data("data/Test/", extract_features_function, number_of_features, 'data/test_labels.csv')

    print('Accuracy: ', clf.score(x_test, y_test))
    print("Feature importance (by original order): " + str(clf.feature_importances_))
    print('stats matrix - \n{}'.format(generate_classification_results(y_test, clf.predict(x_test))))

    print("Compare to prediction by distribution:")
    dist_y = distribution_classification(y_test)
    print('Accuracy of labels according to distribution: ', clf.score(x_test, dist_y))
    print('stats matrix - \n{}'.format(generate_classification_results(y_test, dist_y)))


def get_data(data_dir, extract_features_function, number_of_features, labels_file):
    df_raw = pd.read_csv(labels_file, sep=',')

    for i in range(number_of_features):
        col_name = 'feature_{}'.format(str(i))
        df_raw[col_name] = np.nan

    for wav_file in os.listdir(data_dir):
        if wav_file.endswith(".wav"):
            data, sampling_rate = librosa.load(data_dir + wav_file)

            features_list = extract_features_function(data)
            for j in range(number_of_features):
                col_name = 'feature_{}'.format(str(j))
                df_raw.loc[df_raw.wav_name == int(wav_file.split('.')[0]), col_name] = features_list[j]

    df_raw.dropna(subset=['feature_{}'.format(str(n)) for n in range(number_of_features)], inplace=True)

    x = df_raw[['feature_{}'.format(str(n)) for n in range(number_of_features)]]
    y = df_raw['label']

    return x, y


def distribution_classification(y):
    audio_classes_dist = y.value_counts() / y.shape[0]
    return pd.Series((np.random.choice(task_imp.audio_classes, len(task_imp.audio_classes), 1,
                                       p=audio_classes_dist)[0] for _ in range(y.shape[0])))


def naive_bayes(extract_features_function, number_of_features):
    print("Starting Naive Bayes...\n")

    # Create a Gaussian Classifier
    gnb = GaussianNB()

    # Train the model using the training sets
    print("Preparing the train data\n")
    x_train, y_train = get_data("data/Train/", extract_features_function, number_of_features, 'data/train_labels.csv')
    gnb.fit(x_train, y_train)

    # Predict the response for test dataset
    print("Preparing the test data\n")
    x_test, y_test = get_data("data/Test/", extract_features_function, number_of_features, 'data/test_labels.csv')

    print("Predict")
    y_pred = gnb.predict(x_test)
    print('stats matrix - \n{}'.format(generate_classification_results(y_test, y_pred)))
