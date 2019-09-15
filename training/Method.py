import abc
from keras.layers import Input, Dense, regularizers
from keras.models import Model
import os
import matplotlib.pyplot as plt
import numpy as nump
import json

class Method(metaclass=abc.ABCMeta):
    """
    Define the interface of objects the factory method creates.
    """

    @abc.abstractmethod
    def startTraining(self):
        pass

    @abc.abstractmethod
    def encoder(self,data):
        pass

    @abc.abstractmethod
    def save(self,encode,decode,model):
        pass

    @classmethod
    def readFromFile(cls,filename):
        f = open(filename, "r")
        list_data=[]
        line = f.readline().strip()
        while line!="":
            attrs = line.split(",")
            attrs= list(map(float, attrs))
            attrs=nump.array(attrs)
            list_data.append(attrs)
            line = f.readline().strip()
        f.close()
        return nump.array(list_data)

    @classmethod
    def decoder(cls,encoding_dim, data):
        inputs=Input(shape=(encoding_dim,))
        decoded=Dense(10)(inputs)
        decoded=Dense(30)(decoded)
        print(data[0].shape)
        decoded=Dense(84)(decoded)
        model=Model(inputs,decoded)
        return model

    @classmethod
    def encoder_decoder(cls, data):
        nump.random.seed(1)
        ec=cls.encoder(data)
        dc=cls.decoder(2, data)
        inputs=Input(shape=data[0].shape)
        ec_out=ec(inputs)
        dc_out=dc(ec_out)
        model=Model(inputs,dc_out)
        cls.model=model
        return model

    @classmethod
    def fit(cls, model, data,batch=2,epochs=100):
        model.compile(optimizer="adam",loss='mae',metrics=['accuracy'])
        history=model.fit(data,data,
                       epochs=epochs,
                       batch_size=batch,
                       validation_split=0.2,
                               verbose=2)

        with open('trainHistoryDict.json', 'w') as file_pi:
             json.dump(history.history, file_pi)
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['Loss', 'Val_Loss'], loc='upper left')
        plt.show()



