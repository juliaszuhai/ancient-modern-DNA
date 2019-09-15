import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd


class PrincipleComponentAnalysis():
    def startTraining(self):
        matr = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\ancient\\C51_1_features.csv", "ancient")
        target = matr[1]
        matrx = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_features.csv", "modern")
        target.extend(matrx[1])

        '''calling the PCA'''
        e = pd.DataFrame(target, columns=['target'])
        self.principleComponentAnalysis(matr[0] + matrx[0], e)

    def principleComponentAnalysis(self,data,target):
            pca = PCA(n_components=2)
            pc = pca.fit_transform(data)
            df = pd.DataFrame(data=pc,
                                 columns=['PC1', 'PC2'])
            finalDf = pd.concat([df, target[['target']]], axis=1)
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(1, 1, 1)
            ax.set_xlabel('PC2', fontsize=15)
            ax.set_ylabel('PC2', fontsize=15)
            ax.set_title('2 component PCA', fontsize=20)
            targets = ['ancient','modern']
            colors = ['r', 'g']
            for target, color in zip(targets, colors):
                indicesToKeep = finalDf['target'] == target
                ax.scatter(finalDf.loc[indicesToKeep, 'PC1']
                           , finalDf.loc[indicesToKeep, 'PC2']
                           , c=color
                           , s=30)
            ax.legend(targets)
            ax.grid()
            plt.show()

    def readFromFile(self,filename,type):
            f = open(filename, "r")
            list_data = []
            target= []
            i = 700
            line = f.readline().strip()
            while i < 760:
                attrs = line.split(",")
                attrs = list(map(float, attrs))
                list_data.append(attrs)
                line = f.readline().strip()
                target.append(type)
                i = i + 1
            f.close()
            print(len(list_data))
            return [list_data,target]


if __name__ == "__main__":
    pca=PrincipleComponentAnalysis()
    pca.startTraining();


