from keras.layers import Input, Dense
from keras.models import Model
import os
from training.Method import Method


class AutoEncoder(Method):

    def startTraining(self):
        data=super().readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_features.csv")
        print(len(data))
        model= super().encoder_decoder(data)
        self.fit(model,data)
        self.save(self.encoder)

    @classmethod
    def encoder(cls,data):
        print(data)
        inputs=Input(shape=(data[0].shape))
        encoded=Dense(30,activation='sigmoid')(inputs)
        encoded = Dense(10, activation='sigmoid')(encoded)
        encoded=Dense(2,activation='sigmoid')(encoded)
        cls.encoder=Model(inputs,encoded)
        return cls.encoder

    @classmethod
    def save(cls,encode):
        if not os.path.exists(r'./weights'):
            os.mkdir(r'./weights')
        else:
            encode.save(r'./weights/encoder_weights.h5')
            #decode.save(r'./weights/decoder_weights.h5')
            #model.save(r'./weights/model_weights_oneHot.h5')


    '''def add_noise(self):
       self.data= self.dataRead+ nump.random.normal(0, 0.1, self.dataRead.shape)
'''





