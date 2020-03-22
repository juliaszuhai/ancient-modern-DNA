import pandas as pd
import os
from config import *
from representation.TfIdfStrategy import *
from globals import *
import representation.ExtractFeatureStrategy

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

    for line in file:
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

def create_tf_idf_file(list_of_files):
    """
    Starts from a list of files and creates a features file using the TF-IDF feature method.
    All files are considered when computing IDF.
    The last column will contain the label: 1 - ancient, 0 - modern.
    The new file is saved in processed_data/tf-idf_representation.csv
    """
    sequences = []
    labels = []

    for filename in list_of_files:
        file = open(filename, "r")
        for line in file:
            tokens = line.split(",")
            if len(tokens) != 2:
                continue
            sequence = tokens[1].strip("\n")
            sequences.append(sequence)
            if filename.find("ancient") >= 0:
                labels.append(1)
            else:
                labels.append(0)
        file.close()

    assert len(sequences) == len(labels)

    new_path = os.path.join(PROCESSED_DATA_FOLDER, "tf-idf/tf_idf_representation.csv")
    new_file = open(new_path, "w")
    all_combinations = ExtractFeatureStrategy.generate_possible_sequences(3)
    # remove single letters from the list (they do not bring relevant information in the context of tf-idf, as they occur in all sequences)
    all_combinations = all_combinations[4:]
    idf_map = get_idf_for_subsequences(all_combinations, sequences)
    size = len(sequences)
    for i in range(0, size):
        seq = sequences[i]
        features = get_tf_idf_for_sequence(seq, idf_map, len(sequences))
        l = list(features.values())
        if labels[i] == 1:
            l.append(1)
        else:
            l.append(0)

        aux = ','.join(str(x) for x in l)
        new_file.write(aux + "\n")

        if i % 100 == 0:
            print("Sequence: " + str(i) + "out of total: " + str(size))

    new_file.close()


if __name__ == "__main__":
    modern_file = os.path.join(PROCESSED_DATA_FOLDER, "csv/modern/T1_1.csv")
    ancient_file = os.path.join(PROCESSED_DATA_FOLDER, "csv/ancient/C132_1.csv")
    list_of_files = [ancient_file, modern_file]
    create_tf_idf_file(list_of_files)


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