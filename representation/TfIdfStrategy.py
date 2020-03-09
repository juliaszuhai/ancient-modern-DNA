from Bio.Seq import Seq
import itertools
import math
from representation import ExtractFeatureStrategy
from representation import RepresentationStrategy
import numpy as np

class TfIdfStrategy(RepresentationStrategy.RepresentationStrategy):

    def __init__(self, sequences):
        """
        :param sequences: All sequences that are considered when computing the Inverse Document Frequency (IDF)
        """
        self._sequences = sequences

    def transform(self, seq):
        rez = []
        all_combinations = ExtractFeatureStrategy.generate_possible_sequences(3)
        # remove single letters from the list (they do not bring relevant information in the context of tf-idf, as they occur in all sequences)
        all_combinations = all_combinations[4:]
        features = get_tf_idf_for_sequence(seq, self._sequences)
        for i in range(0, len(all_combinations)):
            rez.append(features[all_combinations[i]])

        return np.array(rez)

def count_sequences_containing_subsequence(subsequence, sequences):
    result = 0
    for s in sequences:
        seq = Seq(s)
        count = seq.count_overlap(subsequence)
        if count > 0:
            result += 1
    return result

def get_tf_idf_for_sequence(dna_seq, sequences):
    seq_list = ExtractFeatureStrategy.generate_possible_sequences(3)
    # remove single letters from the list (they do not bring relevant information in the context of tf-idf, as they occur in all sequences)
    seq_list = seq_list[4:]
    seq = Seq(dna_seq)
    feature_map = {}

    for combination in seq_list:
        # We will count the overlapping values and divide them according to their length
        divide_number = 1
        if len(combination) == 2:
            divide_number = len(dna_seq) - 1
        elif len(combination) == 3:
            divide_number = len(dna_seq) - 2
        tf = seq.count_overlap(combination) / divide_number
        count = count_sequences_containing_subsequence(combination, sequences)
        if count == 0:
            idf = 0
        else:
            idf = math.log2(len(sequences) / count)
        feature_map[combination] = tf * idf

    return feature_map

if __name__ == "__main__":
    sequences = ["ACGGTAACGGTG", "TTGCCTGTGCATGA", "ACCGGTTCAACGTGCAAAACGCGCACCGC"]
    tf_idf = TfIdfStrategy(sequences)
    array = tf_idf.transform(sequences[0])
    print(array.shape)