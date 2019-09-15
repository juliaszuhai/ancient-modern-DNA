from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from representation import RepresentationStrategy
import numpy as np


class OneHotStrategy(RepresentationStrategy.RepresentationStrategy):

    def transform(self,sequence):
        seq = self.split_sequence_into_words(sequence, 1)
        label_encoder = LabelEncoder()
        integer_encoded = label_encoder.fit_transform(seq)
        onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
        integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
        onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
        onehot_encoded = np.array(onehot_encoded)
        onehot_encoded = np.pad(onehot_encoded, [(0, 315 - len(seq)), (0, 64 - len(onehot_encoded[0]))],
                                mode='constant')
        print("ok")
        print(onehot_encoded)
        return onehot_encoded



    def split_sequence_into_words(self,sequence, slide):
        words=[]
        #print(sequence[0])
        for i in range(0,len(sequence)-2,slide):
            str=sequence[i]+sequence[i+1]+sequence[i+2]
            #print(str)
            words.append(str)
        return words



