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


def read_fastq_file_write_to_csv(filepath):
    """
        Read the fastaq file line by line and save the information to a new CSV file.
        The CSV file will have, on each line, the sequence ID and the actual sequence
    """
    file = open(filepath, "r")

    filename, ext = get_filename_and_extension_from_path(filepath)
    new_path = get_path_without_filename(filepath)
    new_path = new_path.replace("raw", "csv")
    try:
        os.makedirs(new_path)
    except FileExistsError:
        # directory already exists
        pass
    new_path = os.path.join(new_path, filename + ".csv")
    csv_file = open(new_path, "w")

    i = 0
    for line in file:
        print(i)
        i += 1
        if len(line) > 0 and line[0] == "@":
            previous_line = line
            aux = line.split(" ")
            if len(aux) > 1:
                identifier = aux[0]
        elif len(previous_line) > 0 and previous_line[0] == "@":
            sequence = line
            previous_line = ""
            # write to file
            csv_file.write(identifier + "," + sequence)
        else:
            continue

    file.close()
    csv_file.close()

if __name__ == "__main__":
    read_fastq_file_write_to_csv("data/raw/ancient/C58_3_1.fastq")


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