from keras.layers import Input, Dense, regularizers
from keras.models import Model
import os
from training.Method import Method


class AutoEncoderSparse(Method):

    def startTraining(self):
        data=super().readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_features.csv")
        print(len(data))
        # ae.add_noise()
        model= super().encoder_decoder(data)
        self.fit(model,data)
        #self.save()

#,activity_regularizer=regularizers.l1(10e-5)
    def encoder(self,data,encoding_dim=2):
        inputs=Input(shape=(data[0].shape))
        encoded=Dense(30,activation='sigmoid',activity_regularizer=regularizers.l1(10e-5))(inputs)
        encoded = Dense(10, activation='sigmoid',activity_regularizer=regularizers.l1(10e-5))(encoded)
        encoded=Dense(encoding_dim,activation='sigmoid',activity_regularizer=regularizers.l1(10e-5))(encoded)
        model=Model(inputs,encoded)
        return model


    def save(self,encode,decode,model):
        if not os.path.exists(r'./weights'):
            os.mkdir(r'./weights')
        else:
            encode.save(r'./weights/encoder_weights_sparse.h5')
            decode.save(r'./weights/decoder_weights_sparse.h5')
            model.save(r'./weights/model_weights_sparse.h5')


    '''def add_noise(self):
       self.data= self.dataRead+ nump.random.normal(0, 0.1, self.dataRead.shape)
'''





