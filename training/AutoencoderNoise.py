from keras.layers import Input, Dense
from keras.models import Model
import os
from training.Method import Method
import numpy as np

class AutoEncoder(Method):

    def startTraining(self):
        data=super().readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_oneHot.csv")
        print(len(data))
        data = data + np.random.normal(0, 0.1, data.shape)
        model= super().encoder_decoder(data)
        self.fit(model,data)
        self.save()

    @classmethod
    def encoder(cls,data):
        print(data)
        inputs=Input(shape=(data[0].shape))
        encoded=Dense(30,activation='sigmoid')(inputs)
        encoded = Dense(10, activation='sigmoid')(encoded)
        encoded=Dense(2,activation='sigmoid')(encoded)
        model=Model(inputs,encoded)
        return model

    @classmethod
    def save(self,encode,decode,model):
        if not os.path.exists(r'./weights'):
            os.mkdir(r'./weights')
        else:
            encode.save(r'./weights/encoder_weights_noise.h5')
            decode.save(r'./weights/decoder_weights_noise.h5')
            model.save(r'./weights/model_weights_noise.h5')




