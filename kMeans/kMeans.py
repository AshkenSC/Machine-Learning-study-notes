# ����numpy�⣬��Ҫʹ�����в��ֺ���
from numpy import *

# ���ı��ļ��洢�����ݵ��뵽�б��С��ı��ļ�ÿһ��Ϊtab�ָ��ĸ�����
# ����fileNameΪҪ������ļ���
def loadDataSet(fileName):
    # �½����б�dataMat�����ڴ洢�������������ݸ�ʽ������Ľ��
    dataMat = []
    # ����ΪfileName���ļ������������fr��
    # ����ֱ�Ӵ����ļ���Ҫ�����ȴ򿪺����һ��������
    # fr�洢�˴򿪵�δ������ı��ļ��������һ����ʽ���洢���б���
    fr = open(fileName)
    # ���б����򿪵��ļ�fr��readlines()������ȡfr�ļ���������
    for line in fr.readlines():
        # line.strip():ɾ����ǰ����β�Ŀհ��ַ���
        # line.strip.split('\t')��ɾ����β�հ��ַ��Ļ����ϣ�����tab�ָ��ַ�����\t��ʾtab�ַ�
        # ���������洢��curLine��
        curLine = line.strip().split('\t')
        # ����curLine�洢��ֻ�Ƿָ����ַ����б�ÿ��Ԫ�ػ�������ֵ��ʽ
        # ʹ��map(float, curLine)����ת��Ϊfloat�����͸�ʽ�����洢��fitLine��
        fltLine = map(float,curLine)
        # ��fitLine��Ϊ��Ԫ����ӵ�dataMat��
        dataMat.append(fltLine)
    # �����������ս��dataMat
    return dataMat

# ������������֮���ŷ�Ͼ��롣�������Ϊ�����б��ʽ�洢��������vecA��vecB
def distEclud(vecA, vecB):
    # ���ڲ㵽��㣺power(a,n)����a��n�η������a���б���ֱ����Ԫ��n�η�
    # sum(a)�����б�a��Ԫ�صĺͣ�sqrt(a)����a��ƽ����
    return sqrt(sum(power(vecA - vecB, 2)))

# Ϊ�������ݼ�����һ������k��������ĵļ��ϡ�������ı��������ݼ��߽���
# ���������ݼ�dataSet��������ĵ�����k
def randCent(dataSet, k):
    # ��ȡ���ݼ�dataSet�ڶ�ά�ĳ��ȡ�����һάΪ���������ڶ�άΪ����������
    n = shape(dataSet)[1]
    # TODO: centroids��ֵ����һ�����
    # zeros()����ʼ��һ��k*n��0����
    # mat()�����б�ת��Ϊ��������
    centroids = mat(zeros((k,n)))
    # ����������
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))#create mat to assign data points
                                      #to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):#for each data point assign it to the closest centroid
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment