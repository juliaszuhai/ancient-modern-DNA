import math

from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt


class PredictAutoencoder:
    def __init__(self):
        pass

    def readFromFile(self,filename,i,j):
        f = open(filename, "r")
        list_data = []
        line = f.readline().strip()
        k=1
        while k<i:
            k = k + 1
            line = f.readline().strip()
        while i < j:
            attrs = line.split(",")
            attrs = list(map(float, attrs))
            list_data.append(attrs)
            line = f.readline().strip()
            i = i + 1
        f.close()
        return list_data

    def mean_list(self,list):
        s=0
        for i in list:
            s=s+i
        return s/len(list)

    def compute_centroids(self,x,a):
        list_x,list_y=zip(*x)
        list_a,list_b=zip(*a)
        mean_x=self.mean_list(list_x)
        mean_y = self.mean_list(list_y)
        mean_a = self.mean_list(list_a)
        mean_b = self.mean_list(list_b)
        return (mean_x,mean_y), (mean_a,mean_b)

    def compute_Distance(self,ref,point):
        return math.sqrt((point[0][0] - ref[0])**2 + (point[0][1] - ref[1])**2 )


    def calculate_points(self,data_seq):
        encoder = load_model(r'./weights/encoder_weights_sparse.h5')
        data_ancient = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\ancient\\C132_1_features.csv", 1,61)
        print(np.array(data_ancient).shape)
        x = encoder.predict(np.array(data_ancient))
        data_modern = self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_features.csv", 11, 71)
        a = encoder.predict(np.array(data_modern))
        points_ancient,points_modern=self.compute_centroids(x,a)
        data_seq=self.readFromFile("D:\\Programming\\Bachelor's Thesis\\Test2\\data\\modern\\T1_1_features.csv", 5, 6)
        print(np.array(data_seq).shape)
        data_seq = np.expand_dims(data_seq,axis=0)
        point=encoder.predict(np.array(data_seq))
        print(point)
        print(points_modern)
        print(points_ancient)
        plt.scatter(*zip(points_ancient),c='orange')
        plt.scatter(*zip(points_modern), c='black')
        plt.scatter(*zip(*x), s=19, label="ancient",marker='*')
        plt.scatter(*zip(*a), c='red', s=15, label="modern", marker='o')
        plt.xlim([0.02,0.024])
        plt.ylim([0.017,0.025])
        plt.scatter(*zip(*point), c='green')
        plt.legend()
        plt.show()
        distance_ancient= self.compute_Distance(points_ancient,point)
        print(distance_ancient)
        distance_modern= self.compute_Distance(points_modern,point)
        print(distance_modern)
        if distance_ancient > distance_modern:
            return "modern"
        else :
            return "ancient"


if __name__ =="__main__":
    p=PredictAutoencoder()
    print(p.calculate_points([0.29874213836477986,0.16352201257861634,0.29559748427672955,0.2389937106918239,0.09779179810725552,0.050473186119873815,0.08201892744479496,0.06624605678233439,0.050473186119873815,0.022082018927444796,0.05362776025236593,0.03785488958990536,0.07570977917981073,0.06309148264984227,0.07570977917981073,0.08201892744479496,0.07255520504731862,0.028391167192429023,0.08517350157728706,0.05362776025236593,0.02531645569620253,0.015822784810126583,0.03164556962025317,0.02531645569620253,0.006329113924050633,0.006329113924050633,0.022151898734177215,0.015822784810126583,0.022151898734177215,0.022151898734177215,0.012658227848101266,0.02531645569620253,0.012658227848101266,0.006329113924050633,0.028481012658227847,0.0189873417721519,0.015822784810126583,0.006329113924050633,0.028481012658227847,0.0,0.012658227848101266,0.0,0.006329113924050633,0.0031645569620253164,0.006329113924050633,0.00949367088607595,0.0189873417721519,0.0189873417721519,0.0189873417721519,0.0,0.015822784810126583,0.0031645569620253164,0.03481012658227848,0.012658227848101266,0.012658227848101266,0.012658227848101266,0.02531645569620253,0.00949367088607595,0.022151898734177215,0.006329113924050633,0.028481012658227847,0.015822784810126583,0.0189873417721519,0.012658227848101266,0.028481012658227847,0.012658227848101266,0.02531645569620253,0.015822784810126583,0.022151898734177215,0.015822784810126583,0.006329113924050633,0.028481012658227847,0.006329113924050633,0.006329113924050633,0.0031645569620253164,0.012658227848101266,0.0189873417721519,0.015822784810126583,0.02531645569620253,0.02531645569620253,0.012658227848101266,0.00949367088607595,0.015822784810126583,0.015822784810126583
]))

