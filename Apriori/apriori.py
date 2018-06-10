from numpy import *

# ����һ�������ݼ���Ϊʾ���Ͳ���
def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

# ��������C1��C1�Ǵ�СΪ1�����к�ѡ��ļ���
def createC1(dataSet):
    # ����һ�����б�C1�������������в��ظ�����ֵ
    C1 = []
    # �������ݼ������н��׼�¼
    for transaction in dataSet:
        # ��ÿһ����¼��������¼��ÿһ��
        for item in transaction:
            # ���ĳ����Ʒ��û����C1�г��֣�������ӵ�C1�С�
            # ע�ⲻ�Ǽ򵥵������Ʒ��Ŀ������ÿ�����ֻ��������Ʒ��ĵ�Ԫ���б�
            # ����Ϊ��ÿ����Ʒ��Ŀ����һ�����ϣ����㷨������������Ҫ�����ϲ�������Python�޷�������Ԫ�ؼ��ϣ����ֻ���õ�Ԫ���б�
            if not [item] in C1:
                C1.append([item])
    # ���Դ��б�������򣬽�����ÿ��Ԫ��ӳ�䵽frozenset����������frozenset���б�
    C1.sort()
    # ��C1�е�ÿһ���һ�����伯�ϡ�frozenset��ָ�����������ļ��ϣ����û����ɸı��
    return map(frozenset, C1)

def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData