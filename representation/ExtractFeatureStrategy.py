import itertools
from Bio.Seq import Seq
from config import *
import utils
from representation import RepresentationStrategy
import numpy as np

class ExtractFeaturesStrategy(RepresentationStrategy.RepresentationStrategy):

    def transform(self,seq):
        rez = []
        all_sequences = generate_possible_sequences(3)
        features = get_features_for_sequence(seq)
        for i in range(0, len(all_sequences) ):
            rez.append(features[all_sequences[i]])

        return np.array(rez)


def generate_possible_sequences(max_seq_length):
    """
        Generate all possible sequences based on the maximum sequence length value.
        If the maximum sequence length value is 1 we'll generate 4 different sequences: ['A', 'C', 'G', 'T']
        If the maximum sequence length value is 2 we'll generate 4 + 16 different sequences: ['A', 'C', 'G', 'T', 'AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT']
        If the value is 3 we'll have 4 + 16 + 64 different sequences and so on
    """
    seq_list = []
    for seq_length in range(1, max_seq_length + 1):
        for cartesian_product_item in itertools.product('ACGT', repeat=seq_length):
            seq_list.append(''.join(cartesian_product_item))
    return seq_list


def get_features_for_sequence(dna_seq):
    """
        For the given sequence, it returns as features the frequencies of occurrence (as percentages) for all combinations of 1, 2 and 3 consecutive
        nucleotides (letters).
        E.g. for sequence ACGGT, we have:
            - A: 1/5 = 0.2; C: 1/5 = 0.2; G: 2/5 = 0.4; T: 1/5 = 0.2 (we divide by 5 because there are 5 letters in the sequence)
            - AA: 0; AC: 1/4 = 0.25; AG: 0; AT: 0; CC: 0; CG = 1/4 = 0.25, etc (we divide by 4 because there are 4 overlapping combinations of 2 letters)
            - AAA: 0; AAC: 0; ... ACG: 1/3 = 0.33; ... CGG: 1/3, etc (we divide by 3 because there are 3 overlapping combinations of 3 letters)
            The feature map will be: ['A': 0.2, 'C': 0.2, 'G': 0.4, 'T': 0.2, 'AA': 0, 'AC': 0.25, 'AG': 0, 'AT': 0, ..., 'TTT': 0]
    """
    seq_list = generate_possible_sequences(3)
    seq = Seq(dna_seq)
    feature_map = {}

    for combination in seq_list:
        # We will count the overlapping values and divide them according to their length
        divide_number = 1
        if len(combination) == 1:
            divide_number = len(dna_seq)
        elif len(combination) == 2:
            divide_number = len(dna_seq) - 1
        elif len(combination) == 3:
            divide_number = len(dna_seq) - 2
        feature_map[combination] = seq.count_overlap(combination) / divide_number

    return feature_map


def read_fastq_file_write_to_csv(filepath):
        """
            Read the fastaq file line by line and save the information to a new CSV file.
            The CSV file will have, on each line, the sequence ID and the actual sequence
        """
        file = open(filepath, "r")

        filename, ext = utils.get_filename_and_extension_from_path(filepath)
        new_path = os.path.join(utils.get_path_without_filename(filepath), filename + ".csv")
        csv_file = open(new_path, "w")

        for line in file:
            if len(line) > 0 and line[0] == "@":
                previous_line = line
                aux = line.split(" ")
                if len(aux) > 1:
                      identifier = aux[0][:48]
            elif len(previous_line) > 0 and previous_line[0] == "@":
                sequence = "TCGACGTCGCGTAAGA"+line
                previous_line = ""
                # write to file
                csv_file.write(identifier + "," + sequence)
            else:
                continue

        file.close()
        csv_file.close()

def create_input_data(filepath):
        """
            Creates input data for a learning algorithm, using the data in the file given as parameter.
            The input file must be a CSV, with 2 columns: identifier, DNA sequence
            The function will extract features from each sequence, as specified in the function "get_features_for_sequence".
            A new CSV file will be created, with 85 columns: identifier, feature1, feature2, ... feature84.
        """
        file = open(filepath, "r")

        filename, ext = utils.get_filename_and_extension_from_path(filepath)
        new_path = os.path.join(utils.get_path_without_filename(filepath), filename + "_histogram.csv")
        features_file = open(new_path, "w")

        # write the header
    #     features_file.write(",")
        all_sequences = generate_possible_sequences(3)
        all_features={key: 0 for key in all_sequences}
    #     for i in range(0, len(all_sequences) - 1):
    #         features_file.write(all_sequences[i] + ",")
    #     features_file.write(all_sequences[-1] + "\n")

        # write contents
        for line in file:
            tokens = line.split(",")
            if len(tokens) != 2:
                continue
            #features_file.write(tokens[0])
            features = get_features_for_sequence(tokens[1])
            for f in all_features.keys():
                all_features[f]=all_features[f]+features[f]
        print(all_features)
        for i in range(0, len(all_sequences) - 1):
            features_file.write(str(all_features[all_sequences[i]]) + ",")
        features_file.write(str(all_features[all_sequences[-1]]) + "\n")
        file.close()
        features_file.close()



def main():
    #create_input_data("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1.csv")
    print(generate_possible_sequences(3))

if __name__=='__main__':
    main()



'''def validate_DNA_sequences(filename1,filename2):
    f = open(filename1, "r")
    g = open(filename2,"r")
    sequences1=[]
    sequences2=[]
    for line in f:
        attrs=line.split(",")
        sequences1.append(attrs[1])
    f.close()
    for line in g:
        attrs=line.split(",")
        for i in attrs[1]:
            if i=='A':
                sequences2.append('T')
            if i=='T':
                sequences2.append('A')
            if i=='C':
                sequences2.append('G')
            if i=='G':
                sequences2.append('C')
    g.close()
    if( len(sequences1)==len(sequences2)):
        print(len(sequences2))
        for i in range (0,len(sequences1)):
            if(sequences1[i]==sequences2[i]):
                print("yes")
'''

'''
#print(ae.data)
    labels=['A', 'C', 'G', 'T', 'AA', 'AC', 'AG', 'AT', 'CA', 'CC', 'CG', 'CT', 'GA', 'GC', 'GG', 'GT', 'TA', 'TC', 'TG', 'TT', 'AAA', 'AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG', 'ACT', 'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC', 'ATG', 'ATT', 'CAA', 'CAC', 'CAG', 'CAT', 'CCA', 'CCC', 'CCG', 'CCT', 'CGA', 'CGC', 'CGG', 'CGT', 'CTA', 'CTC', 'CTG', 'CTT', 'GAA', 'GAC', 'GAG', 'GAT', 'GCA', 'GCC', 'GCG', 'GCT', 'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT', 'TAA', 'TAC', 'TAG', 'TAT', 'TCA', 'TCC', 'TCG', 'TCT', 'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG', 'TTT']
    plt.figure()
    plt.bar(range(len(ae.data)), ae.data)
    plt.xticks(range(len(labels)), labels, size='xx-small', ma='left')
    plt.xlim((0,83))
    plt.xlabel('Features')
    plt.ylabel('Data Distribution')
    plt.show()
'''



