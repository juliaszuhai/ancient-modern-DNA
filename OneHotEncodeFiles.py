from numpy import array
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np

def transform(sequence,seq_max):
    seq = split_sequence_into_words(sequence, 1)
    seq_maxx=split_sequence_into_words(seq_max,1)
    print(len(seq_maxx))
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(seq)
    onehot_encoder = OneHotEncoder(sparse=False, categories='auto')
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    onehot_encoded=np.array(onehot_encoded)
    onehot_encoded=np.pad(onehot_encoded, [(0,len(seq_maxx)-len(seq)), (0, 64-len(onehot_encoded[0]))], mode='constant')
    """
    for i in onehot_encoded:
        print (i)
    """
    return onehot_encoded


def writeToFile():
    listData=readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\ancient\\C51_1.csv")
    maxi=0
    for i in listData:
        if len(i)>maxi:
            maxi=len(i)
            seq_max=i
    for i in listData:
        encoded_seq=transform(i,seq_max)
        with open("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\\\C51_1_oneHot.csv", 'a') as outfile:
            for slice_2d in encoded_seq:
                for i in range(len(slice_2d) - 1):
                    outfile.write("%d," % slice_2d[i])
                outfile.write("%d\n" % slice_2d[len(slice_2d)-1])
                # np.savetxt(outfile, slice_2d, fmt='%-7.2f')
            outfile.write("\n")

def readFromFile(filename):
    f = open(filename, "r")
    list_data = []
    i=0
    line = f.readline().strip()
    while i<30000:
        attrs = line.split(",")
        list_data.append(attrs[1])
        line = f.readline().strip()
        i=i+1
    f.close()
    return list_data


def split_sequence_into_words(sequence, slide):
    words = []
    #print(sequence[0])
    for i in range(0, len(sequence) - 2, slide):
        str = sequence[i] + sequence[i + 1] + sequence[i + 2]
        #print(str)
        words.append(str)
    #print(len(words))
    return words


if __name__ == "__main__":
    writeToFile()