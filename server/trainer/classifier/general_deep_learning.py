from keras.models import Model, Sequential
from keras.layers import Input, Dense, Embedding, SpatialDropout1D, Dropout, add, concatenate, Flatten, Reshape, Concatenate, Conv2D, MaxPool2D
from keras.layers import CuDNNLSTM, Bidirectional, GlobalMaxPooling1D, GlobalAveragePooling1D, Conv1D, MaxPooling1D, LSTM
from keras.preprocessing import text, sequence
from keras.callbacks import LearningRateScheduler
from keras.losses import binary_crossentropy
from keras import backend as K
import pickle


EMBEDDING_FILES = [
    'embedding//glove.840B.300d//glove.840B.300d.txt',
    'embedding//wiki-news_api-300d-1M//wiki-news_api-300d-1M.vec'
]
NUM_MODELS = 2
BATCH_SIZE = 256
LSTM_UNITS = 128
DENSE_HIDDEN_UNITS = 4 * LSTM_UNITS
EPOCHS = 20
MAX_LEN = 500
TEXT_COLUMN = 'sentence'
TARGET_COLUMN = 'label'
CHARS_TO_REMOVE = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n“”’\'∞θ÷α•à−β∅³π‘₹´°£€\×™√²—'


def get_coefs(word, *arr):
    return word, np.asarray(arr, dtype='float32')


def load_embeddings(path):
    with open(path, encoding="utf8") as f:
        return dict(get_coefs(*line.strip().split(' ')) for line in f)


def build_matrix(word_index, path):
    embedding_index = load_embeddings(path)
    embedding_matrix = np.zeros((len(word_index) + 1, 300))
    for word, i in word_index.items():
        try:
            embedding_matrix[i] = embedding_index[word]
        except KeyError:
            pass
    return embedding_matrix

def preprocess(data):
    '''
    Credit goes to https://www.kaggle.com/gpreda/jigsaw-fast-compact-solution
    '''
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~`" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    def clean_special_chars(text, punct):
        for p in punct:
            text = text.replace(p, ' ')
        return text

    data = data.astype(str).apply(lambda x: clean_special_chars(x, punct))
    return data


def build_birectional_lstm_model(embedding_matrix):
    words = Input(shape=(None,))
    x = Embedding(*embedding_matrix.shape, weights=[embedding_matrix], trainable=False)(words)
    x = Bidirectional(CuDNNLSTM(LSTM_UNITS, return_sequences=True))(x)
    x = Bidirectional(CuDNNLSTM(LSTM_UNITS, return_sequences=True))(x)
    x = SpatialDropout1D(0.2)(x)
    hidden = concatenate([
        GlobalMaxPooling1D()(x),
        GlobalAveragePooling1D()(x),
    ])
    hidden = add([hidden, Dense(DENSE_HIDDEN_UNITS, activation='relu')(hidden)])
    hidden = add([hidden, Dense(DENSE_HIDDEN_UNITS, activation='relu')(hidden)])
    result = Dense(1, activation='sigmoid')(hidden)

    model = Model(inputs=words, outputs=result)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


# https://www.kaggle.com/yekenot/2dcnn-textclassifier
def model_simple_cnn_LSTM(embeddign_matrix):
    ## create model
    model_glove = Sequential()
    model_glove.add(Embedding(*embedding_matrix.shape, weights=[embedding_matrix], trainable=False))
    model_glove.add(SpatialDropout1D(0.2))
    model_glove.add(Conv1D(64, 5, activation='relu'))
    model_glove.add(MaxPooling1D(pool_size=4))
    #     model_glove.add(Bidirectional(CuDNNLSTM(128)))
    model_glove.add(Flatten())
    model_glove.add(Dense(1, activation='sigmoid'))
    model_glove.compile(loss='binary_crossentropy', optimizer='adam')
    return model_glove


def model_stacked_cnn(embedding_matrix):
    filter_sizes = [1, 2, 3, 5]
    num_filters = 36

    words = Input(shape=(None,))
    x = Embedding(*embedding_matrix.shape, weights=[embedding_matrix], trainable=False)(words)
    x = Reshape((maxlen, embed_size, 1))(x)

    maxpool_pool = []
    for i in range(len(filter_sizes)):
        conv = Conv2D(num_filters, kernel_size=(filter_sizes[i], embed_size),
                      kernel_initializer='he_normal', activation='elu')(x)
        maxpool_pool.append(MaxPool2D(pool_size=(maxlen - filter_sizes[i] + 1, 1))(conv))

    z = Concatenate(axis=1)(maxpool_pool)
    z = Flatten()(z)
    z = Dropout(0.2)(z)

    outp = Dense(1, activation="sigmoid")(z)

    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model