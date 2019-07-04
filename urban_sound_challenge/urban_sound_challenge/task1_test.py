import librosa
import os
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def generate_classification_results(y_test, res):
    report = str(accuracy_score(y_test, res))
    report += "\n"
    report += classification_report(y_test, res)
    report += "\n"
    report += str(confusion_matrix(y_test, res))
    report += "\n"
    return report


def classification_results(df):
    y_test = df['label'].copy()
    res = df['pred'].copy()
    print('stats matrix - \n{}'.format(generate_classification_results(y_test, res)))


def get_accuracy(f):
    test_dir = "data/Test/"

    df_raw = pd.read_csv('data/test_labels.csv', sep=',')
    df_raw['pred'] = ""

    for wav_file in os.listdir(test_dir):

        if wav_file.endswith(".wav"):
            data, sampling_rate = librosa.load(test_dir + wav_file)
            audio_type = f(data)
            df_raw.loc[df_raw.wav_name == int(wav_file.split('.')[0]), 'pred'] = audio_type

    classification_results(df_raw)
