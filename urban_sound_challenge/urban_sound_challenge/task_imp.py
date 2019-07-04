import librosa
import numpy as np
from urban_sound_challenge import task1_test
from urban_sound_challenge import task2_test
from urban_sound_challenge import task3_test


audio_classes =      ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren',  'street_music']
audio_classes_dist = [0.110394,           0.056302,   0.110396,           0.110396,   0.110396,   0.114811,        0.042318,   0.122907,     0.111684, 0.110396]


def do_it(wav_file):
    data, sampling_rate = librosa.load(wav_file)
    return classify_audio(data)


def classify_audio(wav_data):
    wav_features = extract_data_features(wav_data)
    classification = do_classification(wav_features)
    return classification


def extract_data_features(wav_data):
    # todo replace this with something meaningful
    return np.mean(wav_data), np.max(wav_data), np.median(wav_data), np.std(wav_data), 0


def do_classification(wav_features):
    # todo replace this with something meaningful with wav_features
    return np.random.choice(audio_classes, len(audio_classes), 1, p=audio_classes_dist)[0]


if __name__ == '__main__':
    # Use this function in order to explore the data and your predictions
    # prediction = do_it('data/Train/1.wav')
    # print("The prediction is: " + prediction)

    # TODO: Task 1
    # task1_test.get_accuracy(classify_audio)

    # TODO: Task 2 (a)
    number_of_features = 5
    #task2_test.random_forest(extract_data_features, number_of_features)
    # task2_test.naive_bayes(extract_data_features, number_of_features)

    # TODO: Task 3
    task3_test.do_it()

