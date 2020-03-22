import math
from Bio.Seq import Seq
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
        idf_map = get_idf_for_subsequences(all_combinations, self._sequences)
        features = get_tf_idf_for_sequence(seq, idf_map, len(self._sequences))
        rez = list(features.values())

        return np.array(rez)

def count_sequences_containing_subsequence(subsequence, sequences):
    """
    From a list of sequences (e.g. an entire corpus), it counts how many times the subsequence occurs.
    """
    result = 0
    for s in sequences:
        seq = Seq(s)
        count = seq.count_overlap(subsequence)
        if count > 0:
            result += 1
    return result

def get_idf_for_subsequences(list_of_subsequences, sequences):
    """
        For a list of given subsequences (n-grams of leters), it builds a dictionary which memorizes how many sequences
        (documents) contain each given subsequence
    """
    result = {}
    i = 0
    for subsequence in list_of_subsequences:
        result[subsequence] = count_sequences_containing_subsequence(subsequence, sequences)
        i += 1
        print("Subsequence: " + subsequence)
    return result

def get_tf_idf_for_sequence(dna_seq, idf_map, size):
    """
    :param dna_seq: the current sequence
    :param idf_map: a dictionary which was previously populated, containing the IDF for each subsequence (combination: AA, AC, ... TTT),
                    computed for the entire corpus
    :param size: the total number of sequences
    :return:
    """
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
        idf = idf_map[combination]
        if idf != 0:
            idf = math.log2(size / idf)
        feature_map[combination] = tf * idf

    return feature_map

if __name__ == "__main__":
    sequences = ["ACGGTAACGGTG", "TTGCCTGTGCATGA", "ACCGGTTCAACGTGCAAAACGCGCACCGC"]
    tf_idf = TfIdfStrategy(sequences)
    array = tf_idf.transform(sequences[0])
    print(array)