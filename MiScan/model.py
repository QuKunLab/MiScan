from keras import Sequential
from keras.activations import softmax
from keras.layers import MaxoutDense, Dropout, Dense
from keras.optimizers import adam

from .utils import nb_dense, nb_hidden_units, cut_off
from .utils import nb_fea as nb_dim


def build_model(dim=nb_dim):
    """
    build MiScan Maxout model

    :param dim: feature num , 13885 in this case
    :return:
    """
    model = Sequential()
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense, input_dim=dim))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(MaxoutDense(nb_hidden_units, nb_feature=nb_dense))
    model.add(Dropout(cut_off))
    model.add(Dense(2, activation=softmax))

    model.compile(loss='categorical_crossentropy', optimizer=adam(lr=1e-3), metrics=['accuracy'])
    return model
