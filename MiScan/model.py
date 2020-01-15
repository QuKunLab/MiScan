from keras import Model
from keras.layers import Dropout, Input
from keras.optimizers import adam

from .layers import dense, activation


def build_dense_model(input_dim=13885,
                      lr=1e-6,
                      dropout=0.25,
                      acti='leakyrelu'
                      ):
    input_x = Input(shape=(input_dim,), name="input", dtype='float32')
    x = dense(256)(input_x)
    x = activation(type=acti)(x)
    x = Dropout(dropout)(x)

    x = dense(128)(x)
    x = activation(type=acti)(x)
    x = Dropout(dropout)(x)

    x = dense(64)(x)
    x = activation(type=acti)(x)
    x = Dropout(dropout)(x)

    last = dense(2, activation='softmax')(x)
    model = Model(inputs=input_x, outputs=last)
    model.compile(loss='categorical_crossentropy', optimizer=adam(lr=lr), metrics=['accuracy'])
    return model
