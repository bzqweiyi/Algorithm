from keras.layers import Input, Dense
from keras.models import Model

# this return a tensor
inputs = Input(shape=(784,))

# a layer instance is callable on a tensor, and returns a tensor
x = Dense(64, activation='relu')(inputs)
x = Dense(64, activation='relu')(x)
predictions = Dense(10, activation='softmax')(x)

# This creates a model that includes
# the Input layer and three Dense layers
model = Model(inputs=inputs, outputs=predictions)
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(data, labels) # start training

from keras.layers import TimeDistributed
input_sequences = Input(shape=(20, 784))
processed_sequences = TimeDistributed(model)(input_sequences)