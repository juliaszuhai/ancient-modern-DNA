import pandas as pd
import os
from config import *


def get_filename_and_extension_from_path(path):
    """
        Returns a tuple (filename, extension). If the file has no extension, the second part of the tuple will be the empty string.
    """
    filename = os.path.basename(path)
    l = filename.split(".")
    if len(l) == 2:
        return l[0], l[1]
    else:
        return l[0], ""

def get_path_without_filename(path):
    return os.path.dirname(path)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    
'''def read_data(path, normalize=None):
    """
        Reads data from CSV file and applies normalization, if necessary.
    """
    d = pd.read_csv(path, header=None)
    if normalize == 'min-max':
        aux = d.values
        min_max = sklearn.preprocessing.MinMaxScaler()
        d = pd.DataFrame(min_max.fit_transform(aux))
    elif normalize == 'std':
        d = (d - d.mean()) / d.std()
        d = d.fillna(0)
    return d.values

def get_train_test_data(dataset):
    train, test = sklearn.model_selection.train_test_split(dataset, test_size=0.1, random_state=42)
    return train, test

'''


'''if __name__ == "__main__":
    # read_fastq_file_write_to_csv("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\T1_1.fastq","D:\\Programming\\Bachelor's Thesis\\Test2\\data\\T1_1.csv")
    #d = read_data(os.path.join(DATA_PATH, "T1_1.fastq"))
    #print(d)'''
