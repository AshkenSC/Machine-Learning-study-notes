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
    # ��ȡ���ݼ�dataSet�ڶ�ά�ĳ��ȡ�����һάΪ���������ڶ�άΪ�������ԣ�
    n = shape(dataSet)[1]
    # TODO: centroids��ֵ����һ�����
    # zeros((k, n))����ʼ��һ��1*k*n����άȫ0����ע��k,n�������������š������k*n��ά���󣬾���zeros(k,n)
    # mat()�����б�ת��Ϊnumpy�����ʽ������zeros�����ˡ����󡱣����洢���ʻ����б�
    centroids = mat(zeros((k,n)))
    # ����������
    for j in range(n):
        # minJ�洢��dataSet��j��Ԫ���е���Сֵ
        # dataSet[a:b, j]��ȡdataSet��a��b�еĵ�j��Ԫ�ء�a,b��д��ȡ��j������Ԫ�ء���min��ȡ��ЩԪ����Сֵ
        minJ = min(dataSet[:,j])
        #���������ƣ�max(dataSet[:,j]�õ���j�����ֵ�������minJ������õ�j��ȡֵ��Χ
        rangeJ = float(max(dataSet[:,j]) - minJ)
        # �ȿ��Ⱥ��ұߣ����ڶ������
        # random.rand(k,1)����һ��k��1�е�0-1��Χ������б��ٳ���rangeJ����Ϊ0-rangeJ��Χ�������
        # �ټ���minJ������minJ + rangeJ * random.rand(k,1)Ϊһ��k��1�еģ�ȡֵ��Χ��minJ��maxJ��������б�
        # �ٽ�����mat()�����õ�һ��1*k*1����ά����
        # �ɵ�ʽ���֪�������������Ϊ���ĵĵ�j��
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

# ���ĸ�������������ѡ�����ݼ��ʹص���Ŀ��������ѡ���������ʹ�����ʼ���ĵĺ���
def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    # ��ȡdataSet��һ��ά�ȵĴ�С����dataSet���ж������ݵ�
    m = shape(dataSet)[0]
    # cluster assignment���������洢ÿ����Ĵط�����
    # �������У�һ�м�¼������ֵ���ڶ��д洢������ǰ�㵽�����ĵľ��룩
    clusterAssment = mat(zeros((m,2)))
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
        #print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean
    return centroids, clusterAssment