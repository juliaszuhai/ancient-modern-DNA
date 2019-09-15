from sklearn.utils import shuffle
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Softmax, BatchNormalization, Flatten, Activation, Dropout
import matplotlib.pyplot as plt
import numpy
from keras.utils import np_utils

from representation.DataRepresentation import Context
from representation.OneHotStrategy import OneHotStrategy


class NeuralNetwork:
    def __init__(self):
        pass

    def readFromFile(self,filename):
        f = open(filename, "r")
        list_data = []
        line = f.readline().strip()
        list_of_lists = []
        while line != "end":
            list_data = []
            while line != "\n":
                attrs = line.split(",")
                attrs = list(map(float, attrs))
                attrs = numpy.array(attrs)
                list_data.append(attrs)
                line = f.readline()
                if line != "\n":
                    line.strip()
            line = f.readline()
            list_of_lists.append(list_data)
        f.close()
        return numpy.array(list_of_lists)


    def load_data(self,encoded_seqeunces, encoded_sequences2):
        X = []
        y = []

        for one_hot_key in encoded_seqeunces:
            X.append(one_hot_key)
            y.append(1)

        for key in encoded_sequences2:
            X.append(key)
            y.append(0)

        print('Complete!')
        return X, y


    def prepare_data_for_training(self,X, y, img_rows, img_cols):
        X = numpy.asarray(X, dtype='int32')
        y = numpy.asarray(y)
        print(X.shape[0])
        print(img_rows)
        print(img_cols)
        X = X.reshape(X.shape[0], img_rows, img_cols, 1)

        X, y = shuffle(X, y, random_state=7)  # randomly shuffles the data

        y = np_utils.to_categorical(y, 2)  # converts integer labels to one-hot vector
        return X, y


    def train(self):
        # fix random seed for reproducibility
        numpy.random.seed(7)

        data = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_oneHot.csv")
        data2 = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\ancient\\C51_1_oneHot.csv")
        X, Y = self.load_data(data, data2)

        no_rows = len(data[0])
        no_cols = len(data[0][0])
        print("rows:" + str(len(data)))
        print("cols:" + str(len(data[0])))

        X, Y = self.prepare_data_for_training(X, Y, no_rows, no_cols)

        # create model
        model = Sequential()
        model.add(BatchNormalization(input_shape=(no_rows, no_cols, 1)))

        model.add(Flatten())
        model.add(Dense(no_rows, activation='relu'))

        model.add(Dense(100))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(Dropout(0.5))

        model.add(Dense(2))
        model.add(Activation('softmax'))

        # Compile model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Fit the model
        model.summary()
        # plot_model(model, to_file="ann_plot.png", show_shapes=True, show_layer_names=True)
        file_path = "weights.best.hdf5"

        checkpoint = ModelCheckpoint(file_path, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

        history = model.fit(X, Y, callbacks=[checkpoint], validation_split=0.20, epochs=10, shuffle=True, batch_size=10,
                            verbose=1)

        # list all data in history
        print(history.history.keys())
        # summarize history for accuracy
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def test(self,seq):
        model = load_model("weights.best.hdf5")
        seq = numpy.expand_dims(seq, axis=2)
        seq = numpy.expand_dims(seq, axis=0)
        return model.predict_classes(seq)


if __name__ == "__main__":
    a=NeuralNetwork()
    a.test()
