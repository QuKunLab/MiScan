from keras.layers import Dense, ReLU, Softmax, LeakyReLU


def dense(units,
          activation=None,
          use_bias=True,
          kernel_initializer='glorot_uniform',
          bias_initializer='zeros',
          kernel_regularizer=None,
          bias_regularizer=None,
          activity_regularizer=None,
          kernel_constraint=None,
          bias_constraint=None,
          **kwargs):
    return Dense(
        units, activation=activation, use_bias=use_bias,
        kernel_initializer=kernel_initializer, bias_initializer=bias_initializer,
        kernel_regularizer=kernel_regularizer, bias_regularizer=bias_regularizer,
        kernel_constraint=kernel_constraint, bias_constraint=bias_constraint,
        activity_regularizer=activity_regularizer, **kwargs
    )


def activation(type='relu'):
    if type not in ['relu', 'softmax', 'leakyrelu']:
        raise ValueError('not support for : %s' % type)

    if type == 'relu':
        return ReLU()
    elif type == 'softmax':
        return Softmax()
    elif type == 'leakyrelu':
        return LeakyReLU()
