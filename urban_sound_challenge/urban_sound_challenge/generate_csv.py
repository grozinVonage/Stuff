import pandas as pd
import os


def generate(wavs_dir_name, lables_file_name):

    df_raw = pd.read_csv('data/labels.csv', sep=',')
    df_raw['exists'] = False

    for wav_file in os.listdir(wavs_dir_name):

        if wav_file.endswith(".wav"):
            df_raw.loc[df_raw.wav_name == int(wav_file.split('.')[0]), 'exists'] = True

    df = df_raw[df_raw['exists'] == True][['wav_name', 'label']]
    df.to_csv(lables_file_name, index=False)


if __name__ == '__main__':
    generate('data/Train', 'data/train_labels.csv')
    generate('data/Test', 'data/test_labels.csv')

    # df1 = pd.read_csv('data/train_labels.csv', sep=',')
    # print(df1.shape)

    # df2 = pd.read_csv('data/test_labels.csv', sep=',')
    # print(df2.shape)
