from Bio.Blast import NCBIWWW, NCBIXML
from dto.BlastData import BlastData

class Allignment:
    def __init__(self,seq):
        self.sequence=seq

    def useBLAST(self,filename):
        print("before")
        result_handle = NCBIWWW.qblast("blastn", "nt", self.sequence)
        print("after")
        with open(filename, 'w') as save_file:
            blast_results = result_handle.read()
            save_file.write(blast_results)

    def readBlast(self,filename):
        print("method")
        result = open(filename, "r")
        records = NCBIXML.parse(result)
        item = next(records)
        list=[]
        print("start")
        for alignment in item.alignments:
            for hsp in alignment.hsps:
                #if hsp.expect < 0.01:
                it=BlastData(alignment.title,str(alignment.length),str(hsp.score),str(hsp.gaps),str(hsp.expect),str(hsp.query[0:70]),str(hsp.match[0:70]),str(hsp.sbjct[0:70]))
            list.append(it)
        print(list)
        return list
def main():
    al=Allignment("AGGCAGAACTATTAAGCACTACTCGGGTATCTAATCCTGTTTGCTACCCACGCTTTCGCGCTTCAGCGTCAGTATCTGTCCAGTAAGCTGCCTTCCCCATCGGCTTTCCTACAAATATCTACGAATTTCACCTCTACACTTTTAGTTCCCCTTACCTCTCCAGTACTCTAGTTATACAGTTTCCAACGCAATACCTATTTTATCCCTTCATTTTCCCCTCCTACTTACCTCCCCACCTCGCCCCCCTTTTCCCCCACTTCCTCCCTTCCACCCCCTTTCCCTACTTTTTTCCCCCCCCTCCTTCCCCCATTTTCCCC")
    #al.useBLAST("results.xml")
    al.readBlast("results.xml")



if __name__ =="__main__":
    main()