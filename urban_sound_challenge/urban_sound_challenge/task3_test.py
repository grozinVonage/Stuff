import librosa as librosa
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics


def parser(line, files_prefix, file_name):
    X, sample_rate = librosa.load(files_prefix + file_name + '/{}.wav'.format(line.wav_name))
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    return [mfccs, line.label]


def generate_learn_population(df, files_prefix, file_name, lb=None):
    df = df.reset_index().drop(columns=['index'])
    df = df.apply(parser, args=[files_prefix, file_name], axis=1)
    df = df.to_frame().join(pd.DataFrame(df.values.tolist(), columns=['feature', 'label'])).drop(0, axis=1)
    # df.columns = ['feature', 'label']
    X = np.array(df.feature.tolist())
    y = np.array(df.label.tolist())
    if lb is None:
        lb = LabelEncoder()
    y = to_categorical(lb.fit_transform(y))
    return X, y, lb


def declare_model_architecture(num_labels):
    # build model
    model = Sequential()

    model.add(Dense(256, input_shape=(40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_labels))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
    return model


def do_it(files_prefix='data/'):
    df_train = pd.read_csv('data/train_dl.csv')

    size = df_train.shape[0]
    test_index = round(size*0.8)
    df_test = df_train[test_index:]
    df_train = df_train[:test_index]

    X, y, lb = generate_learn_population(df_train, files_prefix, 'Train_DL')
    X_val, y_val, _ = generate_learn_population(df_test, files_prefix, 'Train_DL', lb)

    num_labels = y.shape[1]

    # build model
    model = declare_model_architecture(num_labels)

    model.fit(X, y, batch_size=32, epochs=10, validation_data=(X_val, y_val))