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

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids